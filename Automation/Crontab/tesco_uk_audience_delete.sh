#!/bin/bash
export PATH="/sbin:/bin:/dhcommon/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/texlive/2018/bin/x86_64-linux:/dhcommon/oracle/product/11.2.0/client_1/bin:/nfs/science/shared/bin:/vampiriser/vampiriser/bin:/home/offcpg/.local/bin:/home/offcpg/bin:/
home/srv_unica_comms/bin:/nfs/science/tesco_uk/OFFSITE/FB"

source $HOME/.bash_profile

echo $(date -u)  "Script starting" >> ~/tesco_uk_audience_delete.log
# Start deleting audiences created more than 90 days ago
python3 /nfs/science/tesco_uk/OFFSITE/FB/delete_custom_aud_UK_90.py >> ~/tesco_uk_audience_delete.log 2>&1
echo $(date -u)  "Script ended" >> ~/tesco_uk_audience_delete.log
