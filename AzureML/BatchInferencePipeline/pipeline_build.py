''' Assemble batch inference pipeline steps and publish as endpoint '''

####################################################################################
# IMPORTS
####################################################################################
import azureml.core
import os
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
def main():

    # setup configuration object to attach compute and environment for pipeline
    aml_run_config = RunConfiguration()

    # create workspace object to interact from compute cluster to AML workspace
    msi_auth = MsiAuthentication()
    ws = Workspace(subscription_id="ef8e1d90-7e58-45fc-a7e5-e608efc32cf1",
                    resource_group="iaasbxarmrgp003",
                    workspace_name="iaasbxarmmlwuw2033",
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
    step1_output_dir = PipelineData('datadir', is_directory=True)
    step2_output_dir = PipelineData('datadir', is_directory=True)

    # Step 1 - prep.py
    step1 = PythonScriptStep(
        source_directory='./src',
        script_name='prep.py',
        runconfig=aml_run_config,
        arguments=[
            '--input-data', input_dataset.as_named_input('input_data'),
            '--shared-dir', step1_output_dir
            ],
        outputs=[step1_output_dir],
        allow_reuse=False)

    # Step 2 - train.py
    step2 = PythonScriptStep(
        source_directory='./src',
        script_name='train.py',
        runconfig=aml_run_config,
        inputs=[step1_output_dir],
        arguments=[
            '--shared-dir', step2_output_dir,
            ],
        outputs=[step2_output_dir],
        allow_reuse=False)

    # Step 3 - score.py
    step3 = PythonScriptStep(
        source_directory='./src',
        script_name='score.py',
        runconfig=aml_run_config,
        inputs=[step2_output_dir],
        arguments=[
            '--shared-dir', step2_output_dir,
            ],
        allow_reuse=False)

    # assemble pipeline steps
    step_sequence = StepSequence(steps=[step1, step2, step3])
    pipeline = Pipeline(workspace=ws, steps=step_sequence)

    # publish assembled pipeline as endpoint
    pipeline_endpoint_name = 'training'
    try:
        pipeline_endpoint_by_name = PipelineEndpoint.get(workspace=ws, name=pipeline_endpoint_name)
        timenow = datetime.now().strftime('%m-%d-%Y-%H-%M')
        pipeline_name = pipeline_endpoint_name + '-' + timenow + "-pipeline"
        published_pipeline = pipeline.publish(
            name=pipeline_name, 
            description='training pipeline endpoint')
        pipeline_endpoint_by_name.add_default(published_pipeline)
    except:
        pipeline_endpoint = PipelineEndpoint.publish(
            workspace=ws, 
            name=pipeline_endpoint_name,
            pipeline=pipeline, 
            description='training pipeline endpoint')

####################################################################################
# INIT
####################################################################################
if __name__ == "__main__":

    # run main function
    main()
