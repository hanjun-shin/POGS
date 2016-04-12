#!/usr/bin/env python
"""
This is the current standard pipeline for HiC data processing


"""

import alab.matrix
import alab.files
import numpy as np
import sys
import argparse

__author__  = "Nan Hua"
__credits__ = ["Nan Hua","Ke Gong","Harianto Tjong", "Hanjun Shin"]

__license__ = "GPL"
__version__ = "0.0.1"
__email__   = "nhua@usc.edu"

#matrixfile = "GSE63525_GM12878_combined_100kb_raw.hdf5"
#domainfile = 'gm12878.100k.Ke.removepeaks.2320.ind'
#outputfile = "GSE63525_GM12878_100kb_krnorm_rmDiag_TadLevel.hdf5"
	
def main(matrixfile, domainfile, outputfile):
	#load matrix in to memory along with idx info, genome version, and resolution of the matrix
	m = alab.matrix.contactmatrix(matrixfile)

	#if you want to remove diagonal
	#use:
	m.removeDiagonal()

	#remove low coverage bins the lowest 1%
	m.removePoorRegions(cutoff=1)
	#bins that with high binomial split correlations are remained

	#identify Inter-chromosome contact outliers, run 100 iterations
	cutoff = m.identifyInterOutliersCutoff(N=100)
	#print cutoff

	#smooth inter-chromosome contact outliers using power law smoothing
	#default settings 
	#w=3,s=3,p=3
	m.smoothInterContactByCutoff(cutoff)

	#normalize the matrix using krnorm
	m.krnorm()
	#m.save(outputfile)
	#m.plot('heatmap_GSE63525_GM12878_100kb_krnorm.png')

	#format:
	#matrixfile = "GSE63525_GM12878_100kb_krnorm_rmDiag.hdf5"
	#domainfile = 'gm12878.100k.Ke.removepeaks.2320.ind'
	#outputfile = "GSE63525_GM12878_100kb_krnorm_rmDiag_TadLevel.hdf5"

	#load matrix in to memory along with idx info, genome version, and resolution of the matrix
	#m = alab.matrix.contactmatrix(matrixfile)

	#removeDiagonals 
	#m.removeDiagonal()

	#GenomeWide smoothing
	#default setting: w=3,s=3,p=3,z=5
	m.smoothGenomeWideHighValue(w=5,s=1,p=1,z=5)
	#m.save('GSE63525_GM12878_100kb_rmDiag.smoothedGenomeWide.hdf5') Hanjun
	#m.makeIntraMatrix('chr1').plot('chr1_smoothed.png') Hanjun
	
	#load domain list information, skip the header and use 
	#column 1 (chromosome); 
	#column 2 (start site); 
	#column 3 (end site)
	#column 0 (suppose to be value for bedgraph file, here we use bead id)
	#column 6 (flag)
	#topdom header is as follows: bead_ID CHR from.coord to.coord from.bin to.bin chrbin.from chrbin.to tag"
	domain = alab.files.bedgraph(domainfile,usecols=(1,2,3,0,6),skip_header=1)

	#assign the matrix with the domain info
	#use pattern to filter the domain list flags, pattern="domain" will ignore all regions that don't contain "domain" flag 
	m.assignDomain(domain,pattern="")


	#generate domain level matrix, using top 10% of the domain contact
	newmatrix = m.iterativeFmaxScaling(23.4)
	#newmatrix.plot('heatmap_GSE63525_GM12878_100kb_rmDiag_TadLevel_median.png',log=False) Hanjun
	newmatrix.save(outputfile)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="buildTADMap.py")
	parser.add_argument('--matrixfile', type=str, required=True)  #raw matrix file
	parser.add_argument('--domainfile', type=str, required=True)  #domain file
	parser.add_argument('--outputfile', type=str, required=True)  #output file
		
	args = parser.parse_args()
   
	main(args.matrixfile, args.domainfile, args.outputfile)
