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

import commands
from resource_management import *
from resource_management.core.logger import Logger

class utils:

  def exe(self, cmd):
    Logger.info("exec command: {0}".format(cmd))

    (status, output) = commands.getstatusoutput(cmd)
    if (status != 0):
      Logger.error("command exec error, return code = {0}".format(status))
      Logger.error(output)
     # raise Fail()

    Logger.info(output)
    return output


  def exe1(self, cmd):
    Logger.info("exec command: {0}".format(cmd))

    (status, output) = commands.getstatusoutput(cmd)
    Logger.info(output)
    return output


  def kill_process(self, keyword):
    Logger.info("kill process by: {0}".format(keyword))
    cmd = "ps aux | grep -E '" + keyword + "' | grep -v grep | awk '{print $2}'"
    result = self.exe(cmd)
    if result != None:
      pids = result.split()
      for pid in pids:
        self.exe("kill -9 " + pid)


  # check process by key word
  def check_process(self, keyword):
    Logger.info("check process by: {0}".format(keyword))
    cmd = "ps aux | grep -E '" + keyword + "' | grep -v grep | cat"
    result = self.exe(cmd)
    if (result == ""):
      Logger.error("process not exist".format(keyword))
      raise ComponentIsNotRunning()

  # check process with "xxx status" and key word
  def check_postgre_running(self, statusCmd):
    Logger.info("check service by: {0}".format(statusCmd))
    cmd = "{0} | grep -E 'is running'".format(statusCmd)
    result = self.exe1(cmd)
    if (result != ""):
      Logger.error("service not exist")
      raise ComponentIsNotRunning()

  # check url
  def check_url(self, url):
    Logger.info("check url: {0}".format(url))
    cmd = "curl -I \"" + url + "\" 2> /dev/null | awk 'NR==1{print}' | awk '{print $2}'"
    result = self.exe(cmd)
    if (result != "200"):
      Logger.error("service not exist")
      raise ComponentIsNotRunning()

if __name__ == "__main__":
    pass
