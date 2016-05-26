
from resource_management import *


class QWServiceCheck(Script):

    def service_check(self, env):
        print "Execute QW Service Check..."

if __name__ == "__main__":
    QWServiceCheck().execute()
