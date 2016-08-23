###### modeling_structure.py ######
#!/usr/bin/env python
"""
Pipeline description documentation.

ModelingStructureFlow Arguments:
	Required Arguments:
		-c, --sys_config 
		-i, --input    		<UNDECIDED>
		-o, --output_dir    <UNDECIDED>
		-f, --freq_list	Frequency List
		-n, --nstruct 
		
	Optional Arguments:
		--flag	  <UNDECIDED>
"""
import argparse
import sys
import os
from subprocess import call
import json

from pyflow import WorkflowRunner
from pyflow import lister

from workflows.utils.args import add_pyflow_args
from workflows.utils.args import default_pyflow_args
from workflows.utils.args import extend_pyflow_docstring
from workflows.modeling.Astep_flow import AStepFlow
from workflows.modeling.Mstep_flow import MStepFlow

#from workflows.utils.sys_utils import ensure_file_exists
#from workflows.config import SiteConfig

__version__ = "0.0.1"

class ModelingStructureFlow(WorkflowRunner):
	def __init__(self, sys_config, input, output_dir, freq_list, nstruct):
		self.sys_config = sys_config
		self.input = input
		self.output_dir = output_dir
		self.freq_list = freq_list.strip('[|]').split(',')
		self.nstruct = nstruct
		
	# input validation
		#ensure_file_exists(self.bam)

	def workflow(self):
		last_freq = 'p100'
		last_actDist = None
		astep_task = None
		
		call(["mkdir", "-p", "%s/actDist" % self.output_dir])
		call(["mkdir", "-p", "%s/structure" % self.output_dir])
				
		for freq in self.freq_list:
			freq = freq.strip()
			struct_dir = "%s/structure" % self.output_dir
				
			mstep_wf = MStepFlow(
				self.sys_config,
				self.input, 
				struct_dir,
				self.nstruct,
				freq,
				last_freq,
				last_actDist
				)
		
			mstep_task = "m_%s_to_%s" % (last_freq, freq)
			
			self.addWorkflowTask(mstep_task, mstep_wf, dependencies=astep_task)
			
			#if last_freq == 'p100':
			#	self.addWorkflowTask(mstep_task, mstep_wf, None)
			#else : self.addWorkflowTask(mstep_task, mstep_wf, dependencies=astep_task)
		
			actDist = "%s/actDist/from.%s.to.%s.actDist" % (self.output_dir, last_freq, freq)
			astep_wf = AStepFlow(
				self.sys_config,
				self.input,
				struct_dir,
				actDist,
				last_freq,
				freq,
				self.nstruct,
				last_actDist
				)
				
			astep_task = "a_%s_to_%s" % (last_freq, freq)
			self.addWorkflowTask(astep_task, astep_wf, dependencies=mstep_task)
			
			last_actDist = actDist
			last_freq = freq
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser(usage=extend_pyflow_docstring(__doc__))
	parser.add_argument('-c', '--sys_config', type=str, required=True)
	parser.add_argument('-i', '--input', type=str, required=True)
	parser.add_argument('-o', '--output_dir', type=str, required=True)
	parser.add_argument('-f', '--freq_list', type=str, required=True)
	parser.add_argument('-n', '--nstruct', type=str, required=True)
	parser.add_argument('--flag', default=False, action="store_true")
	add_pyflow_args(parser)
	args = parser.parse_args()
	
	modeling_structure_wf = ModelingStructureFlow(
			args.sys_config,
			args.input,
			args.output_dir,
			args.freq_list,
			args.nstruct
			)

	sys.exit(modeling_structure_wf.run(**default_pyflow_args(args)))