#!/usr/bin/env python
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

import sys
import os
import commands
from configinit import configinit


from resource_management import *
from resource_management.core.logger import Logger
from utils import utils



class PgMaster(Script):
    def install(self, env):

        Logger.info("install Pg")
        excludePackage = ['pgxzm-center']
        self.install_packages(env,excludePackage)

        import params
        Logger.info("create  user and passwd")

        Logger.info("create  install dir")

        Logger.info(params.pgxx_install_path)
        utils().exe(params.create_install_dir)
        utils().exe(params.chown_install_dir)
        Logger.info("create log dir")
        Logger.info(params.pgxx_log_path)
        utils().exe(params.create_log_dir)
        utils().exe(params.chown_log_dir)
        Logger.info("process initdb")
        utils().exe(params.pg_init_db)
        Logger.info("update configure parameters")
        self.configure(env)
        self.start(env)
        self.createdbsuperuser()

        change_passwd_cmd = format("psql -h {pg_host_name} -p {pgxx_postgre_port} -U postgres -c \"ALTER USER postgres WITH PASSWORD '{pgxx_db_passwd}';\"")
        print 'alter postgres password:{0}'.format(change_passwd_cmd)
        utils().exe(change_passwd_cmd)

        create_demo_table_cmd = format("psql -h {pg_host_name} -p {pgxx_postgre_port} -U postgres -d postgres -c \"create table demo (time varchar(255),pv integer);\"")
        print 'create demo table:{0}'.format(create_demo_table_cmd)
        utils().exe(create_demo_table_cmd)

        create_demo_table_cmd = format("psql -h {pg_host_name} -p {pgxx_postgre_port} -U postgres -d postgres -c \"create table demo1 (method varchar(255),count integer);\"")
        print 'create demo table:{0}'.format(create_demo_table_cmd)
        utils().exe(create_demo_table_cmd)

        Links(params.new_postgresql_install_path, params.postgresql_install_path)

    def uninstall(self, env):
        Toolkit.uninstall_service("postgresql")

    def createdbsuperuser(self):
        Logger.info("create super user for postgresql --")
        create_superuser_command = format("{create_superuser_command}")
        utils().exe(create_superuser_command)

        Logger.info("change password for superuser")
        change_passwd_command = format("psql -h {pg_host_name} -p {pgxx_postgre_port} -U {pgxx_db_user}  "
                                       "-c \"ALTER USER postgres WITH PASSWORD '{pgxx_db_passwd}';\"")
        utils().exe(change_passwd_command)

    def start(self, env):
        Logger.info("start the pg")
        import params
        env.set_params(params)

        self.configure(env)
        utils().exe(params.pg_start)

        Links(params.new_postgresql_data_path, params.postgresql_data_path)
        Links(params.new_postgresql_log_path, params.postgresql_log_path)

    def stop(self, env):
        Logger.info("Stop the pg")
        import params
        env.set_params(params)
        utils().exe(params.pg_stop)

    def configure(self, env):
        import params
        env.set_params(params)
        Logger.info("update pg configs")
        configinit().update_pg(env)

    def status(self, env):
        Logger.info("check pg server running status---")
        import status_params
        cmd = "{0} | grep -E '{1}'".format(status_params.pg_status, "PID")
        Logger.info("check command: {0}".format(status_params.pg_status))
        output = Toolkit.exe(cmd)
        if output == "":
            Logger.error("command {0} not running".format(status_params.pg_status))
            raise ComponentIsNotRunning()

if __name__ == "__main__":
    PgMaster().execute()

