""" Step 3 - score the model """

####################################################################################
# IMPORTS
####################################################################################
import argparse
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
    
    # your code here

####################################################################################
# FUNCTIONS
####################################################################################
def parse_args():
    """Parse pipeline arguments         
    
    Return: 
        args: parsed pipeline attributes [object]

    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--shared-dir", type=str, dest='shared-dir', required=True)

    args = parser.parse_args()

    return args

####################################################################################
# INIT
####################################################################################
if __name__ == "__main__":
    
    args = parse_args()

    main(args)