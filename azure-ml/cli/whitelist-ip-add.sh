#!/bin/bash
PUBLIC_IP_ADDR=`curl ifconfig.me`
echo "Public IP address of Github runner - $PUBLIC_IP_ADDR"
echo "Whitelisting IP - $PUBLIC_IP_ADDR"
az storage account network-rule add --account-name $1 --subscription $2 --resource-group $3 --ip-address $PUBLIC_IP_ADDR >/dev/null

# sleep for the firewall to get updated.
sleep 90
