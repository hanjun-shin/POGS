###### modeling_structure.py ######
#!/usr/bin/env python
"""
Pipeline description documentation.

ModelingStructureFlow Arguments:
	Required Arguments:
		-i, --input_config 
"""
import argparse
import sys
import os
from subprocess import call
import json

from pyflow import WorkflowRunner
#from pyflow import lister

from workflows.utils.args import add_pyflow_args
from workflows.utils.args import default_pyflow_args
from workflows.utils.args import extend_pyflow_docstring
from workflows.modeling.Astep_flow import AStepFlow
from workflows.modeling.Mstep_flow import MStepFlow

#from workflows.utils.sys_utils import ensure_file_exists
#from workflows.config import SiteConfig

__version__ = "0.0.1"

class ModelingStructureFlow(WorkflowRunner):
	def __init__(self, input_config):#sys_config, input, output_dir, freq_list, nstruct):
		self.input_config = input_config
		# self.sys_config = sys_config
		# self.input = input
		# self.output_dir = output_dir
		# self.freq_list = freq_list.strip('[|]').split(',')
		# self.nstruct = nstruct
		
	# input validation
		#ensure_file_exists(self.bam)

	def workflow(self):
		if type(self.input_config) == str :
			if not (os.path.exists(self.input_config) and os.access(self.input_config, os.R_OK) ):
				raise Exception('Cannot Find or Access input_config file %s' % self.input_config)
			with open(self.input_config, 'r') as data_file: 
				self.input_config = json.load(data_file)
		
		if not self.input_config.has_key('source_dir') :
			raise Exception('Input config error, it does not have source_dir ')		
					
		if not self.input_config.has_key('modeling_parameters') :
			raise Exception('%s : Input config error, it does not have modeling_parameters' % os.path.name(__file__))
		else :
			if not self.input_config['modeling_parameters'].has_key('probMat') :
				raise Exception('%s : Input config error, it does not have probMat' % os.path.name(__file__))
			if not self.input_config['modeling_parameters'].has_key('probability_list') :
				raise Exception('%s : Input config error, it does not have probability_list' % os.path.name(__file__))
			if not self.input_config['modeling_parameters'].has_key('num_of_structures') :
				raise Exception('%s : Input config error, it does not have num_of_structures' % os.path.name(__file__))
				
		input = self.input_config['modeling_parameters']['probMat']
		freq_list = self.input_config['modeling_parameters']['probability_list']
		nstruct = self.input_config['modeling_parameters']['num_of_structures']
		last_freq = 'p100'
		last_actDist = None
			
		struct_dir = "%s/structure" % self.input_config['output_dir']
		actDist_dir = "%s/actDist" % self.input_config['output_dir']
		
		call(["mkdir", "-p", struct_dir])
		call(["mkdir", "-p", actDist_dir])
		
		astep_task = None
		for freq in freq_list:
			freq = freq.strip()
			
			m_task_config = self.input_config
			m_task_config['modeling_parameters'].update({'struct_dir' : struct_dir})
			m_task_config['modeling_parameters'].update({'freq' : freq})
			m_task_config['modeling_parameters'].update({'last_freq' : last_freq})
			m_task_config['modeling_parameters'].update({'last_actDist' : last_actDist})
							
			# mstep_wf = MStepFlow(
				# self.sys_config,
				# self.input, 
				# struct_dir,
				# self.nstruct,
				# freq,
				# last_freq,
				# last_actDist
				# )
		
			mstep_wf = MStepFlow(m_task_config)
			mstep_task = "m_%s_to_%s" % (last_freq, freq)
			self.addWorkflowTask(mstep_task, mstep_wf, dependencies=astep_task)
			
			#if last_freq == 'p100':
			#	self.addWorkflowTask(mstep_task, mstep_wf, None)
			#else : self.addWorkflowTask(mstep_task, mstep_wf, dependencies=astep_task)
		
			a_task_config = m_task_config
			a_task_config['modeling_parameters'].update({'actDist_dir' : actDist_dir})
			
			actDist = "%s/from.%s.to.%s.actDist" % (actDist_dir, last_freq, freq)
			a_task_config['modeling_parameters'].update({'actDist' : actDist})
						
			# astep_wf = AStepFlow(
				# self.sys_config,
				# self.input,
				# struct_dir,
				# actDist,
				# last_freq,
				# freq,
				# self.nstruct,
				# last_actDist
				# )
			astep_wf = AStepFlow(a_task_config)
			astep_task = "a_%s_to_%s" % (last_freq, freq)
			self.addWorkflowTask(astep_task, astep_wf, dependencies=mstep_task)
			
			last_actDist = actDist
			last_freq = freq
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser(usage=extend_pyflow_docstring(__doc__))
	parser.add_argument('-i', '--input_config', type=str, required=True)
	# parser.add_argument('-i', '--input', type=str, required=True)
	# parser.add_argument('-o', '--output_dir', type=str, required=True)
	# parser.add_argument('-f', '--freq_list', type=str, required=True)
	# parser.add_argument('-n', '--nstruct', type=str, required=True)
	# parser.add_argument('--flag', default=False, action="store_true")
	add_pyflow_args(parser)
	args = parser.parse_args()
	
	modeling_structure_wf = ModelingStructureFlow(args.input_config)
	# modeling_structure_wf = ModelingStructureFlow(
			# args.sys_config,
			# args.input,
			# args.output_dir,
			# args.freq_list,
			# args.nstruct
			# )

	sys.exit(modeling_structure_wf.run(**default_pyflow_args(args)))