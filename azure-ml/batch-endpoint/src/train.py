""" Step 2 - conduct model training trigger workflow """

####################################################################################
# IMPORTS
####################################################################################
import argparse
import pandas as pd
import os
from azureml.core import Run, Model

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

    # load output data from previous step as input
    input_dataframe = pd.read_csv(
        os.path.join(args.shared_dir, 'prep_output.csv')
        )
    
    ##### your code here

    # once model is trained and saved in shared directory
    # then register in aml registry - below assumes model 
    # is saved as models/model.pkl
    model = Model.register(
        model_path=os.path.join(args.shared_dir, 'models/model.pkl'),
        model_name=args.model_name,
        workspace=ws
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

    # pass shared directory filepath for moving data between pipeline steps
    parser.add_argument("--shared_dir", type=str, dest='shared_dir', required=True)
    parser.add_argument("--model_name", type=str, dest='model_name', required=True)

    args = parser.parse_args()

    return args

####################################################################################
# INIT
####################################################################################
if __name__ == "__main__":
    
    args = parse_args()

    main(args)
