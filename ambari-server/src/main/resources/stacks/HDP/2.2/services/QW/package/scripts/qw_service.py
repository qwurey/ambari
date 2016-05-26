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

Ambari Agent

"""

from resource_management import *

def qw_service(action, component):
    import os
    import params
    if action == 'start':
        if component == 'master':
            pid_file = os.path.join(params.qw_master_pid_dir, "qw_master.pid")
            if pid_file and os.path.isfile(pid_file):
                return
            # create a master pid dir
            Directory(params.qw_master_pid_dir,
                      owner='root',
                      group='root',
                      recursive=True
                      )
            File(os.path.join(params.qw_master_pid_dir, "qw_master.pid"),
                 owner='root',
                 group='root',
                 content="333"
                 )
        elif component == 'slave':
            pid_file = os.path.join(params.qw_slave_pid_dir, "qw_slave.pid")
            if pid_file and os.path.isfile(pid_file):
                return
            # create a master pid dir
            Directory(params.qw_slave_pid_dir,
                      owner='root',
                      group='root',
                      recursive=True
                      )
            File(os.path.join(params.qw_slave_pid_dir, "qw_slave.pid"),
                 owner='root',
                 group='root',
                 content="3333"
                 )
    elif action == 'stop':
        if component == 'master':
            os.remove(os.path.join(params.qw_master_pid_dir, "qw_master.pid"))
        elif component == 'slave':
            os.remove(os.path.join(params.qw_slave_pid_dir, "qw_slave.pid"))
