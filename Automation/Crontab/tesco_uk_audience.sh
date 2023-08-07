#!/bin/bash
export PATH="/sbin:/bin:/dhcommon/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/texlive/2018/bin/x86_64-linux:/dhcommon/oracle/product/11.2.0/client_1/bin:/nfs/science/shared/bin:/vampiriser/vampiriser/bin:/home/offcpg/.local/bin:/home/offcpg/bin:/
home/srv_unica_comms/bin:/nfs/science/tesco_uk/OFFSITE/jiraScripts/"

source $HOME/.bash_profile

echo "Script starting" >> ~/tesco_uk_audience.log
# Generate Digital Offsite audience config files
/nfs/science/tesco_uk/OFFSITE/jiraScripts/audience/prod/app.py >> ~/tesco_uk_audience.log 2>&1
echo "Script ended" >> ~/tesco_uk_audience.log
