''' Create managed online endpoint and deploy '''

####################################################################################
# IMPORTS
####################################################################################
import datetime
import json
from azure.ai.ml import MLClient
from azure.ai.ml.entities import ManagedOnlineEndpoint, ManagedOnlineDeployment, Model, Environment, CodeConfiguration
from azure.identity import DefaultAzureCredential
import argparse

####################################################################################
# MAIN
####################################################################################
def main(args):

    # parse configurations
    with open(args.config_file, 'r') as f:
        configs=json.load(f)

    ml_client = MLClient(
        DefaultAzureCredential(), 
        subscription_id=configs['subscription_id'],
        resource_group_name=configs['resource_group'],
        workspace_name=configs['workspace_name']
    )

    # get locally saved model
    model_filepath = "./src/linear_regression_model.pkl"
    model = Model(path=model_filepath)

    # create conda environment using yml file and base image
    env = Environment(
        conda_file="./src/conda.yml",
        image="mcr.microsoft.com/azureml/openmpi3.1.2-ubuntu18.04:20210727.v1",
    )

    # create a unique endpoint name with current datetime to avoid conflicts - must be unique across Azure
    online_endpoint_name = "endpoint-" + datetime.datetime.now().strftime("%m%d%H%M%f")

    # create an online endpoint
    endpoint = ManagedOnlineEndpoint(
        name=online_endpoint_name,
        description="linear_regression_endpoint",
        auth_mode="key"
    )

    print('creating endpoint')
    endpoint = ml_client.begin_create_or_update(endpoint)
    while not endpoint.done():
        print(endpoint.status())
    
    print(endpoint.status())
    # create deployment definition
    name_of_deployment = "linear-regression-test"
    model_deployment = ManagedOnlineDeployment(
        name=name_of_deployment,
        endpoint_name=online_endpoint_name,
        model=model,
        environment=env,
        code_configuration=CodeConfiguration(
            code="./src", scoring_script="score.py"
        ),
        instance_type="Standard_F2s_v2",
        instance_count=1,
    )

    # deploy endpoint
    ml_client.begin_create_or_update(model_deployment)

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
