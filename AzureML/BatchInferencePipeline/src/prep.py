""" Step 1 - prepare dataset for training """

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

    input_data = run.input_datasets['input_data1'].to_pandas_dataframe()

####################################################################################
# FUNCTIONS
####################################################################################
def parse_args():
    """Parse pipeline arguments         
    
    Return: 
        args: parsed pipeline attributes [object]

    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--input-data", type=str, dest='dest_input_data1', help='raw dataset1')

    args = parser.parse_args()

    return args

####################################################################################
# INIT
####################################################################################
if __name__ == "__main__":
    
    run = Run.get_context()