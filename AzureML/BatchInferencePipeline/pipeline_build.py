''' Assemble batch inference pipeline steps and publish as endpoint '''

####################################################################################
# IMPORTS
####################################################################################
from azureml.core import Workspace

####################################################################################
# MAIN
####################################################################################
def main():

    # PIPELINE ARTIFACTS
    msi_auth = MsiAuthentication()

    ws = Workspace(subscription_id="d54f5885-394a-4860-84b9-d3c6dc20f130",
                    resource_group="iaadevarmrgp002",
                    workspace_name="iaadevarmmlwuw2002",
                    auth=msi_auth
                    )

####################################################################################
# PIPELINE STEPS
####################################################################################


# Step 1 - prep.py
step_preprocess = PythonScriptStep(
    name='preprocess input data',
    source_directory='src',
    script_name='prep.py',
    arguments=[
        '--input-data', input_data_vrpt_IMDM_Incident.as_named_input('input_data1'),
                                    '--input-data2', input_data_qut_pipesql.as_named_input('input_data2'),
                                    '--output-data', data_intermediary_folder1],
                        outputs=[data_intermediary_folder1],
                        runconfig=pipeline_run_config_small,
                        allow_reuse=allow_reuse_for_all)