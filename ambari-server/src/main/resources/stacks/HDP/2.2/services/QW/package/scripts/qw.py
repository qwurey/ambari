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
import os

from resource_management import *
import sys


def qw(type = None):
    import params

    # create a log dir
    Directory(params.qw_log_dir,
              owner='root',
              group='root',
              recursive=True
              )

    # create a data dir
    Directory(params.qw_data_dir,
              owner='root',
              group='root',
              recursive=True
              )

    # create a etc dir
    Directory(params.qw_config_dir,
              owner='root',
              group='root',
              recursive=True
              )

    XmlConfig("qw-env.xml",
              conf_dir=params.qw_config_dir,
              configurations=params.config['configurations']['qw-env'],
              configuration_attributes=params.config['configuration_attributes']['qw-env'],
              owner='root',
              group='root'
              )
    print "qw-env.xml configurations", params.config['configurations']['qw-env']
    print "qw-env.xml configuration_attributes", params.config['configuration_attributes']['qw-env']

    XmlConfig("qw-site.xml",
              conf_dir=params.qw_config_dir,
              configurations=params.config['configurations']['qw-site'],
              configuration_attributes=params.config['configuration_attributes']['qw-site'],
              owner='root',
              group='root'
              )

    File(format("{qw_config_dir}/qw-env.sh"),
        owner='root',
        group = 'root',
        mode=0777,
        content=InlineTemplate(params.qw_env_sh_template)
    )

    print "This is ", type, " to create log dir && data dir && etc dir && .sh"
    # create etc dir
    # Directory(params.qw_config_dir,
    #           owner=params.qw_user,
    #           recursive=True,
    #           )

