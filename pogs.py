###### ModelingPipeline.PY ######
#
"""
Pipeline description documentation.

GeneratePopulationOfGenomeStructure Arguments:
    Required Arguments:
        -i, --input_config    Path to intput configure file
"""
import argparse
import sys
import os
import os.path
import json
from subprocess import call

from pyflow import WorkflowRunner
#from workflows.define_domain import DefineDomainFlow
from workflows.build_TAD_map_flow import BuildTADMapFlow
from workflows.modeling_structure_flow import ModelingStructureFlow
from workflows.report_flow import ReportFlow

from workflows.utils.args import add_pyflow_args
from workflows.utils.args import default_pyflow_args
from workflows.utils.args import extend_pyflow_docstring
#from workflows.utils import ensure_file_exists

__version__ = "0.0.1"

class GeneratePopulationOfGenomeStructure(WorkflowRunner):
	def __init__(self, input_config) : #, contactMap, domainFile, output_dir, freq_list, nstruct):
		self.input_config = input_config
		
# input validation
        #ensure_file_exists(self.input_config)
		#ensure_file_exists(self.system_config)

	def workflow(self):
		if type(self.input_config) == str :
			if not (os.path.exists(self.input_config) and os.access(self.input_config, os.R_OK) ):
				raise Exception('Cannot Find or Access input_config file %s' % self.input_config)
			with open(self.input_config, 'r') as data_file: 
				self.input_config = json.load(data_file)
				
		###############################################################
		# BuildTADMapFlow
		###############################################################
		build_task_config = self.input_config
		call(["mkdir", "-p", "%s/probMat" % build_task_config['output_dir']])
		probMat = '%s/probMat/probMat.hdf5.hmat' % build_task_config['output_dir']
		build_task_config['modeling_parameters'].update({'probMat' : probMat})
				
		build_TAD_map_wf = BuildTADMapFlow( build_task_config )
			
		build_TAD_map_task = "build_TAD_map_task"
		self.addWorkflowTask(build_TAD_map_task, build_TAD_map_wf, dependencies=None)
		
		###############################################################
		# ModelingStructureFlow
		###############################################################
		modeling_task_config = build_task_config
		
		# modeling_structure_wf = ModelingStructureFlow(
			# sys_config = self.sys_config,
			# input = probMat,
			# output_dir = self.output_dir,
			# freq_list =  self.freq_list,
			# nstruct = self.nstruct
			# )
		modeling_structure_wf = ModelingStructureFlow(modeling_task_config)
		modeling_structure_task = "modeling_structure_task"
		self.addWorkflowTask(modeling_structure_task, modeling_structure_wf, dependencies=build_TAD_map_task)
		
		###############################################################
		# ReportFlow
		###############################################################
		
		report_task_config = modeling_task_config
		
		report_wf = ReportFlow(report_task_config)
		report_task = "report_task"
		self.addWorkflowTask(report_task, report_wf, dependencies=modeling_structure_task)
						
        #if self.flag:
        #    args.append('--flag')

        #self.addTask('task_id', ' '.join(args))
		
if __name__ == "__main__":
	parser = argparse.ArgumentParser(usage=extend_pyflow_docstring(__doc__))
	parser.add_argument('-i', '--input_config', type=str, required=True)
	#parser.add_argument('-c', '--sys_config', type=str, required=True)
	#parser.add_argument('-m', '--contactMap', type=str, required=True)
	#parser.add_argument('-d', '--domainFile', type=str, required=True)
	#parser.add_argument('-o', '--output_dir', type=str, required=True)
#    parser.add_argument('-s', '--system_config', default=True, action="store_true")
	add_pyflow_args(parser)
	args = parser.parse_args()

	GeneratePopulationOfGenomeStructure_wf = GeneratePopulationOfGenomeStructure(args.input_config)

	sys.exit(GeneratePopulationOfGenomeStructure_wf.run(**default_pyflow_args(args)))