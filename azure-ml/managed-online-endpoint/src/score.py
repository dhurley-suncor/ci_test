#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################
# Created By  : David Hurley
# Created Date: August 12, 2022
# Objective: scoring script for model
##############################################
import json
import numpy as np
import os
import joblib

def init():
    """Initialized functon before any other function call
    Returns:
        pkl file loaded into a model object
    """
    global model
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    # For multiple models, it points to the folder containing all deployed models (./azureml-models)
    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'linear_regression_model.pkl')
    model = joblib.load(model_path)

def run(raw_data):
    """Make a prediction with model object
    Args:
        raw_data: json input to predict on
    Returns:
        list of predictions
    """
    data = np.array(json.loads(raw_data)['data'])
    # make prediction
    y_hat = model.predict(data)
    # you can return any data type as long as it is JSON-serializable
    return y_hat.tolist()