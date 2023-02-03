#!/bin/bash
PUBLIC_IP_ADDR=`curl ifconfig.me`
echo "Public IP address of Github runner - $PUBLIC_IP_ADDR"
echo "Removing IP - $PUBLIC_IP_ADDR"
az storage account network-rule remove --account-name $1 --subscription $2 --resource-group $3 --ip-address $PUBLIC_IP_ADDR >/dev/null
        
