#!/bin/bash
export PATH="/sbin:/bin:/dhcommon/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/texlive/2018/bin/x86_64-linux:/dhcommon/oracle/product/11.2.0/client_1/bin:/nfs/science/shared/bin:/vampiriser/vampiriser/bin:/home/offcpg/.local/bin:/home/offcpg/bin:/
home/srv_unica_comms/bin:/nfs/science/tesco_uk/OFFSITE/jiraScripts/:/nfs/science/tesco_uk/OFFSITE/AudienceTest/Version/"

source $HOME/.bash_profile

echo $(date -u)  "Script starting" >> ~/tesco_uk_liveramp_audience.log
# Start Liveramp audience upload
python3 /nfs/science/tesco_uk/OFFSITE/AudienceTest/Version/split_prep_all.py --liveramp >> ~/tesco_uk_liveramp_audience.log 2>&1
echo $(date -u)  "Script ended" >> ~/tesco_uk_liveramp_audience.log
