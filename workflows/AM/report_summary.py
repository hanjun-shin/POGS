#!/usr/bin/env python

# Copyright (C) 2015 University of Southern California and
#                          Nan Hua
# 
# Authors: Nan Hua
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import argparse
from alab.analysis import structuresummary
from subprocess import call
#from __future__ import print_function
__author__  = "Nan Hua"
__credits__ = ["Hanjun Shin"]

__license__ = "GPL"
__version__ = "0.0.1"
__email__   = "nhua@usc.edu"
  
if __name__=='__main__':
	parser = argparse.ArgumentParser(description="report_summary.py")
	parser.add_argument('-s', '--struct_dir', type=str, required=True)  #probility matrix file in contactmatrix format
	parser.add_argument('-p', '--prob', type=str, required=True)    #last frequency
	parser.add_argument('-n', '--nstruct', type=int, required=True) #current freq
	parser.add_argument('-o', '--output_dir', type=str, required=True) #current freq
	
	args = parser.parse_args()
	##################################################
	#summary
	##################################################
	#call(["mkdir", "-p", "%s/summary" % args.output_dir])
	s = structuresummary(target=args.struct_dir, usegrp=args.prob, nstruct=int(args.nstruct) )
	#s.save('%s/summary/summary.hss' % args.output_dir)
    
	##################################################
    #violations
	##################################################
	call(["mkdir", "-p", "%s/violations" % args.output_dir])
	#with open("%s/violations/violations.txt" % args.output_dir, 'w') as file:
	#	file.write('Violation Ratio: %i' % int(s.totalViolations.mean())/int(s.totalRestraints.mean()))
		#print 'Violation Ratio:',s.totalViolations.mean()/s.totalRestraints.mean()
    
	##################################################
    #heatmap
	##################################################
	call(["mkdir", "-p", "%s/heatmap" % args.output_dir])
	m = s.getContactMap()
	m.plot('%s/heatmap/heatmap.pdf' % args.output_dir, format='pdf')
	
	##################################################
	#IntraMatrix
	##################################################
	chrList = ['chr%i' % i for i in range(1,23)]
	chrList.append('chrX')
	
	call(["mkdir", "-p", "%s/intraMatrix" % args.output_dir])
	for chr in chrList:
		m.makeIntraMatrix(chr).plot('%s/intraMatrix/%s_intraMatrix.pdf' % (args.output_dir, chr), format='pdf')
    
	###################################################
    #radial position
	###################################################
    #rp = s.getBeadRadialPosition(beads=range(len(s.idx)*2))
    
    
    
    
