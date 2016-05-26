from resource_management.libraries.script import Script
from resource_management.libraries.functions.default import default
# server configurations
config = Script.get_config()

pg_init_path = "/usr/pgsql-9.3/bin/"
pgxx_install_path =  default("/configurations/postgresql-main-env/postgresql.install.path","/data/postgre/data")
pgxx_log_path =  default("/configurations/postgresql-main-env/postgresql.log.path","/data/postgre/log")
pgxx_user =  default("/configurations/postgresql-main-env/postgresql.user","postgres")
pg_status_command = pg_init_path + "pg_ctl  -D "+ pgxx_install_path +"  -l " + pgxx_log_path + "/logfile status"
pg_status = "su  - " + pgxx_user + " -c '" + pg_status_command +"'"
