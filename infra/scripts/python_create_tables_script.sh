#!/bin/bash
echo "started the script"


# Variables

baseUrl="$1"
resourceGroup="$2"
key_vault_name="$3"
postgres_server_name="$4"
host_name="$5"
database_name="$6"
admin_principal_name="$7"
identity_name="$8"  # managed identity user name. Wil use this to connect to the postgres server 
requirementFile="requirements.txt"
requirementFileUrl=${baseUrl}"infra/scripts/data_scripts/requirements_create_tables.txt"

echo "Script Started"

# Get the public IP address of the machine running the script
publicIp=$(curl -s https://api.ipify.org)

# Use Azure CLI to add the public IP to the PostgreSQL firewall rule
az postgres flexible-server firewall-rule create --resource-group $resourceGroup --name $postgres_server_name --rule-name "AllowScriptIp" --start-ip-address "$publicIp" --end-ip-address "$publicIp"

curl --output "psql_create_tables_script.py" ${baseUrl}"infra/scripts/data_scripts/psql_create_tables_script.py"

# Download the requirement file
curl --output "$requirementFile" "$requirementFileUrl"

echo "Download completed"


# Install the required packages
pip install --no-cache-dir -r requirements.txt

# execute python code
python psql_create_tables_script.py --key_vault_name ${key_vault_name} --host_name ${host_name} --admin_principal_name ${admin_principal_name} --database_name ${database_name} --identity_name ${identity_name}
