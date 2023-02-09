''' Assemble batch inference pipeline steps and publish as endpoint '''

####################################################################################
# IMPORTS
####################################################################################
import azureml.core
import os
import argparse
import json
from azureml.core import Workspace, Dataset, Environment 
from azureml.core.compute import AmlCompute
from azureml.pipeline.core import Pipeline, StepSequence, PipelineEndpoint, PipelineData
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.steps import PythonScriptStep
from datetime import datetime
from azureml.core.authentication import MsiAuthentication

####################################################################################
# MAIN
####################################################################################
def main(args):

    # setup configuration object to attach compute and environment for pipeline
    aml_run_config = RunConfiguration()

    # parse configurations
    with open(args.config_file, 'r') as f:
        configs=json.load(f)

    msi_auth = MsiAuthentication()

    ws = Workspace(subscription_id=configs['subscription_id'],
                    resource_group=configs['resource_group'],
                    workspace_name=configs['workspace_name'],
                    auth=msi_auth
                    )

    # load registered dataset
    input_dataset = Dataset.get_by_name(ws, name='input-data')

    # add compute cluster and environment to run configuration
    aml_compute = AmlCompute(ws, 'cpu-cluster')
    aml_env = Environment.get(ws, 'AML-batch-inference-env')

    aml_run_config.target = aml_compute
    aml_run_config.environment = aml_env

    # create shared folder to pass data between pipeline steps
    shared_pipeline_dir = PipelineData('datadir', is_directory=True)

    # Step 1 - prep.py
    step1 = PythonScriptStep(
        source_directory='./src',
        script_name='prep.py',
        runconfig=aml_run_config,
        arguments=[
            '--input_data', input_dataset.as_named_input('input_data'),
            '--shared_dir', shared_pipeline_dir
            ],
        outputs=[shared_pipeline_dir],
        allow_reuse=False)

    # Step 2 - train.py
    step2 = PythonScriptStep(
        source_directory='./src',
        script_name='train.py',
        runconfig=aml_run_config,
        inputs=[shared_pipeline_dir],
        arguments=[
            '--shared_dir', shared_pipeline_dir,
            '--model_name', 'NAME-IN-REGISTRY'
            ],
        allow_reuse=False)

    # Step 3 - score.py
    step3 = PythonScriptStep(
        source_directory='./src',
        script_name='score.py',
        runconfig=aml_run_config,
        inputs=[shared_pipeline_dir],
        arguments=[
            '--shared_dir', shared_pipeline_dir,
            '--model_name', 'NAME-IN-REGISTRY'
            ],
        allow_reuse=False)

    # assemble pipeline steps
    step_sequence = StepSequence(steps=[step1, step2, step3])
    pipeline = Pipeline(workspace=ws, steps=step_sequence)

    # publish assembled pipeline as endpoint
    pipeline_endpoint_name = 'NAME-OF-PUBLISHED-ENDPOINT'
    try:
        pipeline_endpoint_by_name = PipelineEndpoint.get(workspace=ws, name=pipeline_endpoint_name)
        timenow = datetime.now().strftime('%m-%d-%Y-%H-%M')
        pipeline_name = pipeline_endpoint_name + '-' + timenow + "-pipeline"
        published_pipeline = pipeline.publish(
            name=pipeline_name, 
            description='XXX')
        pipeline_endpoint_by_name.add_default(published_pipeline)
    except:
        pipeline_endpoint = PipelineEndpoint.publish(
            workspace=ws, 
            name=pipeline_endpoint_name,
            pipeline=pipeline, 
            description='XXX')

###################################################
# FUNCTIONS
###################################################
def parse_args():
    """ Parse pipeline arguments 
    
        Return: 
            - args[dict]
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--config_file", type=str)

    args = parser.parse_args()

    print('Pipeline arguments successfully parsed')

    return args

####################################################################################
# INIT
####################################################################################
if __name__ == "__main__":

    # parse args
    args = parse_args()

    # run main function
    main(args)
