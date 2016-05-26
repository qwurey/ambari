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

config = Script.get_config()

# qw-env.xml
qw_master_home = config['configurations']['qw-env']['qw_master_home']
# pid
qw_master_pid_dir = config['configurations']['qw-env']['qw_master_pid_dir']
qw_slave_pid_dir = config['configurations']['qw-env']['qw_slave_pid_dir']
# qw_master_pid_file = format("{qw_master_pid_dir}/qw_master.pid")
# qw_slave_pid_file = format("{qw_slave_pid_dir}/qw_slave.pid")

qw_user = config['configurations']['qw-env']['qw_user']
user_group = config['configurations']['cluster-env']['user_group']

# qw-site.xml
qw_server_address = config['configurations']['qw-site']['qw.server.address']
qw_server_web_url = config['configurations']['qw-site']['qw.server.web.url']

# qw-env.sh
qw_env_sh_template = config['configurations']['qw-env']['content']

# custom
qw_config_dir = "/etc/tbds/qw"
qw_log_dir = "/var/log/tbds/qw"
qw_data_dir = "/data/tbds/qw"
qw_bin = '/etc/tbds/qw/qw-env.sh'


