import sys, os
from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger
from qw import qw
from qw_service import qw_service

class Master(Script):

    def install(self, env):
        # self.install_packages(env)
        self.configure(env)
        print "Install QW My Master"

    def configure(self, env):
        import params
        env.set_params(params)
        qw(type = 'master')
        print "Configure QW My Master"

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        qw_service(action = 'start', component = 'master')

        daemon_cmd = "{0} start".format(params.qw_bin)
        print daemon_cmd
        Execute(daemon_cmd,
                user='root'
        )
        print "Start QW My Master"

    def stop(self, env):
        qw_service(action = 'stop', component = 'master')
        print "Stop QW My Master"

    def status(self, env):
        import os.path
        import params
        if not os.path.isfile(os.path.join(params.qw_master_pid_dir, "qw_master.pid")):
            raise ComponentIsNotRunning()
        print "QW Master Status..."

    def uninstall(self, env):
        print "Uninstall QW My Master"
        Toolkit.uninstall_service("qw")

    def getmem(self, env):
        import os
        print 'Execute this coustom command to get mem info on this host'
        os.system("free")

if __name__ == "__main__":
    Master().execute()