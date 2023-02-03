# Github Action - Build and Publish Batch Pipeline Endpoint AzureML

## Description
This sample GitHub action is to build and publish a AzureML pipeline as a batch endpoint.

## Overview
![image](https://user-images.githubusercontent.com/83986810/213018946-89dc6e58-5bef-4104-bb53-173babf3f019.png)
Detailed step-by-step of action workflow:
1. checkout the associated branch
2. login to Azure using the CLI and Service Principal credential stored in Git Secrets
4. Whitelist IP to the AzureML default storage account
3. Install the AzureML CLI extension and set the default workspace
4. Trigger a build of the AzureML pipeline and publish as an endpoint
5. Remove whitelisted IP from storage account

## Usage
### Pre-requisite
- AzureML workspace
- Service Principal used by GitHub actions to access Azure resources. Needs contributor permission on AzureML resource and blob data contribuor access to storage account associated with AzureML.
- Existing cpu cluster in AzureML workspace with system assigned managed identity and vnet/subnet (permission and network and firewall have to be in place)
- Existing registered environment in AzureML workspace
- AzureML pipeline code and build script

Below is an example of how the code for an AzureML pipeline might look. The only assumption for this action is that a `pipeline-build.py` file exists somewhere so that the `pipeline.yml` which is triggered by the action can find it.

**Example AzureML pipeline code file structure:**
- `pipeline.yml`: provided here but assumes that it is in same folder as `pipeline-build.py`
- `pipeline-build.py`: this assembles the pipeline steps and does the publish action (see [MLOps](https://github.com/SEAdvancedAnalyticsOrg/MachineLearningOps) repository for example)
- `src/`: contains all the python files for each step of the pipeline

### Step 1: Create GitHub Actions Secret using Service Principal Credential for Azure resources
GitHub Actions Secret should look like below. 

```
{
    "clientId": "<GUID>",
    "clientSecret": "<GUID>",
    "subscriptionId": "<GUID>",
    "tenantId": "<GUID>",
}
```
### Step 2: Modify branch specific workflow inputs and secret name
For example, change the inputs and secret name in `aml-build-batch-endpoint-DEV.yml`

### Step 3: Give cpu cluster managed identity permission
Needs contributor permission on AzureML resource and blob data contribuor access to storage account associated with AzureML.

### Step 4: Add vnet/subnet associated with cpu cluster to firewall of storage account

### Step 5: Modify pipeline.yml
`pipeline.yml` triggers the AzureML pipeline build script. Modify the compute cluster name, environment name, and name and path to `pipeline-build.py`

## Reference

[AA MLOps Repository](https://github.com/SEAdvancedAnalyticsOrg/MachineLearningOps)

[Use GitHub Actions with Azure Machine Learning](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-github-actions-machine-learning?tabs=userlevel)

[AzureML GitHub Action Example Repository](https://github.com/azure/azureml-examples)

