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

import socket

from resource_management.libraries.functions.flume_agent_helper import find_expected_agent_names
from resource_management.libraries.functions.flume_agent_helper import get_flume_status

RESULT_CODE_OK = 'OK'
RESULT_CODE_CRITICAL = 'CRITICAL'
RESULT_CODE_UNKNOWN = 'UNKNOWN'

# QW_CONF_DIR_KEY = '{{flume-env/flume_conf_dir}}'
QW_CONF_DIR_KEY = '/etc/tbds/qw'
QW_SLAVE_RUN_DIR = '/var/run/qw/slave'

def get_tokens():
    """
    Returns a tuple of tokens in the format {{site/property}} that will be used
    to build the dictionary passed into execute
    """
    return (QW_CONF_DIR_KEY,)


def execute(parameters=None, host_name=None):
    """
    Returns a tuple containing the result code and a pre-formatted result label

    Keyword arguments:
    parameters (dictionary): a mapping of parameter key to value
    host_name (string): the name of this host where the alert is running
    """

    if parameters is None:
        return (RESULT_CODE_UNKNOWN, ['There were no parameters supplied to the script.'])

    qw_conf_directory = None
    if QW_CONF_DIR_KEY in parameters:
        qw_conf_directory = parameters[QW_CONF_DIR_KEY]

    if qw_conf_directory is None:
        return (RESULT_CODE_UNKNOWN, ['The QW configuration directory is a required parameter.'])

    if host_name is None:
        host_name = socket.getfqdn()

    # processes = get_flume_status(qw_conf_directory, QW_MASTER_RUN_DIR)
    # expected_agents = find_expected_agent_names(qw_conf_directory)

    alert_label = ''
    alert_state = RESULT_CODE_OK


    return (alert_state, [alert_label])