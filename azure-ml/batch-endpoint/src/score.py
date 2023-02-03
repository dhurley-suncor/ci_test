""" Step 3 - score the model """

####################################################################################
# IMPORTS
####################################################################################
import argparse
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

    # load registered model from registry
    model = Model.get(
        model_name=args.model_name,
        workspace=ws
    )

    ##### your code here

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
    parser.add_argument("--shared-dir", type=str, dest='shared-dir', required=True)
    parser.add_argument("--model_name", type=str, dest='model_name', required=True)

    args = parser.parse_args()

    return args

####################################################################################
# INIT
####################################################################################
if __name__ == "__main__":
    
    args = parse_args()

    main(args)
