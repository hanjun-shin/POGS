###### build_domain_contact_map.py ######
#!/usr/bin/env python
"""
Pipeline description documentation.


BuildTADMapFlow Arguments:
	Required Arguments:
		-c, --sys_config    
		-m, --matrixFile   
		-d, --domainFile
		-o, --outputFile
		
	Optional Arguments:
		--flag	  <UNDECIDED>
"""
import argparse
import sys
import os
import json

from pyflow import WorkflowRunner
from workflows.utils.args import add_pyflow_args
from workflows.utils.args import default_pyflow_args
from workflows.utils.args import extend_pyflow_docstring

#from workflows.utils.sys_utils import ensure_file_exists
#from workflows.config import SiteConfig

__version__ = "0.0.1"

class BuildTADMapFlow(WorkflowRunner):
	def __init__(self, input_config):
		self.input_config = input_config
			  
# input validation
		#ensure_file_exists(self.bam)

	def workflow(self):
		if type(self.input_config) == str :
			if not (os.path.exists(self.input_config) and os.access(self.input_config, os.R_OK) ):
				raise Exception('Cannot Find or Access input_config file %s' % self.input_config)
			with open(self.input_config, 'r') as data_file: 
				self.input_config = json.load(data_file)
		
		if not self.input_config.has_key('source_dir') :
			raise Exception('%s : Input config error, it does not have source_dir' % os.path.name(__file__))		
					
		if not self.input_config.has_key('input') :
			raise Exception('%s : Input config error, it does not have input' % os.path.name(__file__))
		else :
			if not self.input_config['input'].has_key('contact_map_file') :
				raise Exception('%s : Input config error, it does not have contact_map_file' % os.path.name(__file__))
			if not self.input_config['input'].has_key('TAD_file') :
				raise Exception('%s : Input config error, it does not have TAD_file' % os.path.name(__file__))
				
		if not self.input_config.has_key('modeling_parameters') :
			raise Exception('%s : Input config error, it does not have modeling_parameters' % os.path.name(__file__))
		else :
			if not self.input_config['modeling_parameters'].has_key('probMat') :
				raise Exception('%s : Input config error, it does not have probMat' % os.path.name(__file__))
		
		if not self.input_config.has_key('system') :
			raise Exception('%s : Input config error, it does not have system ' % os.path.name(__file__))
		else :
			if not self.input_config['system'].has_key('basic_core') :
				raise Exception('%s : Input config error, it does not have basic_core' % os.path.name(__file__))
			if not self.input_config['system'].has_key('max_memMB') :
				raise Exception('%s : Input config error, it does not have max_memMB' % os.path.name(__file__))
		
		source = '%s/buildTADMap.py' % self.input_config['source_dir']
		matrixFile = self.input_config['input']['contact_map_file']
		domainFile = self.input_config['input']['TAD_file']
		outputFile = self.input_config['modeling_parameters']['probMat']
		nCores = self.input_config['system']['basic_core']
		memMb = self.input_config['system']['max_memMB']
				
		args = [
			'python',
			source, 
			'--matrixfile', matrixFile, 
			'--domainfile', domainFile,
			'--outputfile', outputFile
			]
		
		task_label = "buildTADMap_flow"
		self.addTask(label=task_label, command=' '.join(args), nCores=nCores, memMb=memMb, retryMax=3, retryWait=2, retryWindow=0, retryMode="all")		
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser(usage=extend_pyflow_docstring(__doc__))
	parser.add_argument('-i', '--input_config', type=str, required=True)
	#parser.add_argument('-m', '--matrixFile', type=str, required=True)
	#parser.add_argument('-d', '--domainFile', type=str, required=True)
	#parser.add_argument('-o', '--outputFile', type=str, required=True)

	#parser.add_argument('--flag', default=False, action="store_true")
	add_pyflow_args(parser)
	args = parser.parse_args()

	buildTADMapFlow_wf = BuildTADMapFlow(
			input_config = args.input_config
			)

	sys.exit(buildTADMapFlow_wf.run(**default_pyflow_args(args)))