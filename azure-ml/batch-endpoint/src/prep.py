""" Step 1 - prepare dataset for training trigger workflow """

####################################################################################
# IMPORTS
####################################################################################
import argparse
import pandas as pd
import os
from azureml.core import Run

####################################################################################
# MAIN
####################################################################################
def main(args):
    """Execute all logic

    Args:
        args: pipeline attributes [object]

    """
    run = Run.get_context()

    # connect to workspace
    ws = run.experiment.workspace

    # pointer to registered dataset as defined in pipeline_build.py
    input_dataframe = run.input_datasets['input_data'].to_pandas_dataframe()

    ##### your code here

    output_dataframe = input_dataframe # placeholder

    if not os.path.exists(args.shared_dir):
        os.makedirs(args.shared_dir)

    # save output of this step as csv to load in next step
    output_dataframe.to_csv(
        os.path.join(args.shared_dir, 'prep_output.csv'), 
        index=False
        )

####################################################################################
# FUNCTIONS
####################################################################################
def parse_args():
    """Parse pipeline arguments         
    
    Return: 
        args: parsed pipeline attributes [object]

    """

    parser = argparse.ArgumentParser()

    # pass input data name to the pipeline
    parser.add_argument("--input_data", type=str, dest='input_data', required=True)
    
    # pass shared directory filepath for moving data between pipeline steps
    parser.add_argument("--shared_dir", type=str, dest='shared_dir', required=True)

    args = parser.parse_args()

    return args

####################################################################################
# INIT
####################################################################################
if __name__ == "__main__":
    
    args = parse_args()

    main(args)
