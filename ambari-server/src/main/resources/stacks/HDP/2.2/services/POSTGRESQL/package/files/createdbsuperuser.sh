#!/bin/bash

# createdbsuperuser.sh pgxx_postgre_port pgxx_user   'CREATE ROLE  pgxx_db_user SUPERUSER;'
echo "create a new super user for postgresql ,then start the createdbsuperuser.sh --"
echo $1
pgxx_postgre_port_=$1
echo $2
pgxx_user_=$2
echo $3
pgxx_db_user_=$3
echo $4
pgxx_params1=$4
echo $5
pgxx_params2=$5
#  'CREATE ROLE  pgxx_db_user  SUPERUSER;'

create_user_command="${pgxx_db_user_} ${pgxx_params1} ${pgxx_params2} ${pgxx_user_}"
echo $create_user_command
$create_user_command
# sudo -u postgres createuser --superuser dbuser
# sudo -u postgres createdb -O dbuser exampledb
# exe_command="psql -p $pgxx_postgre_port_ -U $pgxx_user_  -d $pgxx_user_  -c '${command_}' "
# exe_command="sudo -u postgres createuser --superuser  $pgxx_user_"
# echo "  create spueruser command exe : ${exe_command} "
# $exe_command
# exe_command_createdb="sudo -u postgres createdb -O dbuser exampledb"
# echo "  create example db command exe : ${exe_command_createdb} "
# $exe_command_createdb
