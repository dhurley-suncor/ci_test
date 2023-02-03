#!/bin/bash
# <az_ml_install>
az extension add -n ml -y
# </az_ml_install>

# <set_variables>
GROUP=$1
LOCATION=$2
WORKSPACE=$3
# </set_variables>

# <az_configure_defaults>
az configure --defaults group=$GROUP workspace=$WORKSPACE location=$LOCATION
# </az_configure_defaults>