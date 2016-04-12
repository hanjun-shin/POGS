###### report.py ######
#!/usr/bin/env python
"""
Pipeline description documentation.

ReportFlow Arguments:
	Required Arguments:
		-c, --sys_config    <UNDECIDED>
		-s, --struct_dir   <UNDECIDED>
		-p, --prob   <UNDECIDED>
		-n, --nstruct   <UNDECIDED>
		-o, --output_dir   <UNDECIDED>
	Optional Arguments:
		--flag	  <UNDECIDED>
"""
import argparse
import sys
import os
import json
from subprocess import call

from pyflow import WorkflowRunner
from workflows.utils.args import add_pyflow_args
from workflows.utils.args import default_pyflow_args
from workflows.utils.args import extend_pyflow_docstring

#from workflows.utils.sys_utils import ensure_file_exists
#from workflows.config import SiteConfig

__version__ = "0.0.1"

class ReportFlow(WorkflowRunner):
	def __init__(self, input_config):#sys_config, struct_dir, prob, nstruct, output_dir):
		self.input_config = input_config
		# self.struct_dir = struct_dir,
		# self.prob = prob,
		# self.nstruct = nstruct,
		# self.output = output_dir
			  
# input validation
		#ensure_file_exists(self.bam)

	def workflow(self):
		if type(self.input_config) == str :
			if not (os.path.exists(self.input_config) and os.access(self.input_config, os.R_OK) ):
				raise Exception('Cannot Find or Access input_config file %s' % self.input_config)
			with open(self.input_config, 'r') as data_file: 
				self.input_config = json.load(data_file)
		
		if not self.input_config.has_key('source_dir') :
			raise Exception('%s : Input config error, it does not have source_dir ' % os.path.name(__file__))		
					
		if not self.input_config.has_key('modeling_parameters') :
			raise Exception('%s : Input config error, it does not have modeling_parameters' % os.path.name(__file__))
		else :
			if not self.input_config['modeling_parameters'].has_key('probMat') :
				raise Exception('%s : Input config error, it does not have probMat' % os.path.name(__file__))
			if not self.input_config['modeling_parameters'].has_key('num_of_structures') :
				raise Exception('%s : Input config error, it does not have num_of_structures' % os.path.name(__file__))
			if not self.input_config['modeling_parameters'].has_key('probability_list') :
				raise Exception('%s : Input config error, it does not have probability_list' % os.path.name(__file__))
			
		if not self.input_config.has_key('output_dir') :
			raise Exception('%s : Input config error, it does not have output_dir' % os.path.name(__file__))
			
		if not self.input_config.has_key('system') :
			raise Exception('%s : Input config error, it does not have system ' % os.path.name(__file__))
		else :
			if not self.input_config['system'].has_key('basic_core') :
				raise Exception('%s : Input config error, it does not have max_core' % os.path.name(__file__))
			if not self.input_config['system'].has_key('max_memMB') :
				raise Exception('%s : Input config error, it does not have max_memMB' % os.path.name(__file__))
				
		report_src = '%s/report_summary.py' % self.input_config['source_dir']
		struct_dir = '%s/structure' % self.input_config['output_dir']
		prob = self.input_config['modeling_parameters']['probability_list'][-1]
		nstruct = self.input_config['modeling_parameters']['num_of_structures']
		output_dir = '%s/report' % self.input_config['output_dir']
		call(["mkdir", "-p", output_dir])
		nCores = self.input_config['system']['basic_core']
		memMb = self.input_config['system']['max_memMB']
		
		args = ['python',
			report_src, 
			'--struct_dir', struct_dir, 
			'--prob', prob,
			'--nstruct', str(nstruct),
			'--output_dir', output_dir]
		
		print args
		task_label = "report_flow"
		self.addTask(label=task_label, command=' '.join(args), nCores=1, memMb=100000, retryMax=3, retryWait=2, retryWindow=0, retryMode="all")	
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser(usage=extend_pyflow_docstring(__doc__))
	parser.add_argument('-i', '--input_config', type=str, required=True)
	# parser.add_argument('-c', '--sys_config', type=str, required=True)
	# parser.add_argument('-s', '--struct_dir', type=str, required=True)
	# parser.add_argument('-p', '--prob', type=str, required=True)
	# parser.add_argument('-n', '--nstruct', type=str, required=True)
	# parser.add_argument('-o', '--output_dir', type=str, required=True)
	# parser.add_argument('--flag', default=False, action="store_true")
	
	add_pyflow_args(parser)
	args = parser.parse_args()

	# report_wf = ReportFlow(
			# args.sys_config,
			# args.struct_dir,
			# args.prob,
			# args.nstruct,
			# args.output_dir
			# )
	report_wf = ReportFlow(args.input_config)
	
	sys.exit(report_wf.run(**default_pyflow_args(args)))