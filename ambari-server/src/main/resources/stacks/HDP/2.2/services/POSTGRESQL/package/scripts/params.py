"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from resource_management import *
#new add for  main

pgxx_user =  default("/configurations/postgresql-main-env/postgresql.user","postgres")
pgxx_install_path =  default("/configurations/postgresql-main-env/postgresql.install.path","/data/postgre/data")
pgxx_log_path =  default("/configurations/postgresql-main-env/postgresql.log.path","/data/postgre/log")

pgxx_db_user = default("/configurations/postgresql-main-env/postgresql.superuser","postgres")
pgxx_db_passwd = default("/configurations/postgresql-main-env/superuser.passwd","postgres")


# mkdir /usr/local/pgsql/data
# root# chown postgres /usr/local/pgsql/data
#root# su postgres
#postgres$ initdb -D /usr/local/pgsql/data

create_install_dir = " mkdir -p " + pgxx_install_path
chown_install_dir = " chown -R "+pgxx_user+ " " +pgxx_install_path

create_log_dir = " mkdir -p " + pgxx_log_path
chown_log_dir = " chown -R "+ pgxx_user+ " " +pgxx_log_path

#new add for hba
pgxx_hba_local =  default("/configurations/postgresql-hba-env/postgresql.hba.local","local	all	        all		                        trust")
pgxx_hba_ipv4 =  default("/configurations/postgresql-hba-env/postgresql.hba.ipv4","host    all         all         0.0.0.0/0         trust")
pgxx_hba_ipv6 =  default("/configurations/postgresql-hba-env/postgresql.hba.ipv6","host    all         all         ::1/128               trust")

#new add for postgre
pgxx_postgre_max_connections =  default("/configurations/postgresql-postgre-env/postgresql.postgre.max_connections",100)
pgxx_postgre_shared_buffers =  default("/configurations/postgresql-postgre-env/postgresql.postgre.shared_buffers",32)
pgxx_postgre_port = default("/configurations/postgresql-postgre-env/postgresql.postgre.port",5432)
pgxx_postgre_listen_addresses = default("/configurations/postgresql-postgre-env/postgresql.postgre.listen_addresses","*")


# create
pg_host_name = default("hostname", "localhost")
create_superuser_command = "su  - " + pgxx_user + " -c '" + "/usr/pgsql-9.3/bin/createuser -h {0} -p {1} --login --createdb  -s ".format(pg_host_name, pgxx_postgre_port) + pgxx_db_user + "'"
# Pg
#/etc/init.d/postgresql-9.3 start
# pg_ctl -D /data/postgre/data -l logfile start
#pg_init_db = "su postgres ; initdb -D /data/postgre/data"
pg_init_path = "/usr/pgsql-9.3/bin/"
pg_init_db_command = pg_init_path + "initdb -D "+pgxx_install_path
pg_init_db = "su  - " + pgxx_user + " -c '" + pg_init_db_command +"'"
#pg_init_db = "service postgresql-9.3 initdb"
#pg_start = "su postgres -c 'service postgresql start'"
#  pg_ctl -D /data/postgre/data -l logfile start
pg_start_command = pg_init_path + "pg_ctl  -D "+ pgxx_install_path +" -l " + pgxx_log_path + "/logfile start"
pg_start = "su  - " + pgxx_user + " -c '" + pg_start_command +"'"
#pg_start = "service  postgresql-9.3 start"
#pg_cofig_check = "chkconfig postgresql-9.3 on"
#pg_stop = "su postgres -c 'service postgresql stop'"
pg_stop_command = pg_init_path + "pg_ctl  -D "+ pgxx_install_path +" -l " + pgxx_log_path + "/logfile stop"
pg_stop = "su  - " + pgxx_user + " -c '" + pg_stop_command +"'"
#pg_stop = "service  postgresql-9.3 stop"
#pg_status = "su postgres -c 'service postgresql status'"
#pg_status = "service postgresql status"
pg_status_command = pg_init_path + "pg_ctl  -D "+ pgxx_install_path +"  -l " + pgxx_log_path + "/logfile status"
pg_status = "su  - " + pgxx_user + " -c '" + pg_status_command +"'"
#pg_status = "service  postgresql-9.3 status"
#pg_restart = "su postgres -c 'service postgresql restart'"
#pg_restart = "service postgresql restart"
pg_restart_command = pg_init_path + "pg_ctl  -D "+ pgxx_install_path +" -l " + pgxx_log_path + "/logfile restart"
pg_restart =  "su  - " + pgxx_user + " -c '" + pg_restart_command +"'"
#pg_restart = "service  postgresql-9.3 restart"

# refractor service path

postgresql_install_path = "/usr/pgsql-9.3"
postgresql_data_path =  default("/configurations/postgresql-main-env/postgresql.install.path","/data/postgre/data")
postgresql_log_path =  default("/configurations/postgresql-main-env/postgresql.log.path","/data/postgre/log")


new_postgresql_install_path = "/opt/tbds/postgresql"
new_postgresql_data_path = "/data/tbds/postgresql"
new_postgresql_log_path = "/var/log/tbds/postgresql"
