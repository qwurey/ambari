import sys, os
from resource_management import *
from resource_management.core.exceptions import ComponentIsNotRunning
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger
from qw import qw
from qw_service import qw_service

class Slave(Script):

    def install(self, env):
        self.configure(env)
        print "Install QW My Slave"

    def configure(self, env):
        import params
        env.set_params(params)
        qw(type='slave')
        print "Configure QW My Slave"

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        qw_service(action = 'start', component = 'slave')
        print "Start QW My Slave"

    def stop(self, env):
        qw_service(action = 'stop', component = 'slave')
        print "Stop QW My Slave"

    def status(self, env):
        import os.path
        import params
        if not os.path.isfile(os.path.join(params.qw_slave_pid_dir, "qw_slave.pid")):
            raise ComponentIsNotRunning()
        print "QW Slave Status..."

    def uninstall(self, env):
        Toolkit.uninstall_service("qw")
        print "Uninstall QW My Slave"

    def iostat(self, env):
        import os
        os.system("iostat")

if __name__ == "__main__":
    Slave().execute()