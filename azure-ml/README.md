# Github Action - Azure ML

## Description
Sample Github Actions for doing ci/cd in Azure ML

## Overview
##### Batch Pipeline Endpoint
Action to assemble Azure ML pipeline and publish pipeline endpoint which can then be triggered by an orchestrator such as Azure Data Factory or Azure Synapse.
![image](https://user-images.githubusercontent.com/83986810/217064665-ca4290d2-8851-4433-8ba7-798ba9752487.png)

##### Managed Online Endpoint
Action to create and deploy an Azure ML managed online endpoint.

## Usage
### Prerequisites
- Github repository and codebase
- Azure ML workspace
- Service Principal used by GitHub actions to access Azure resources. Needs contributor permission on Azure ML resource and blob data contributor access to default storage account for Azure ML workspace.
- Existing compute cluster in Azure ML workspace. If Azure ML needs to access data in a storage account behind a firewall the compute cluster needs system assigned managed identity and a vnet/subnet attached. Permission, network, firewall must be in place in the latter case. 
- Existing registered environment in Azure ML workspace. This is required to run any jobs on an Azure ML compute cluster.
- Code for Azure ML batch inference pipeline

### Step 1: Create GitHub Actions Secret using Service Principal Credential
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

