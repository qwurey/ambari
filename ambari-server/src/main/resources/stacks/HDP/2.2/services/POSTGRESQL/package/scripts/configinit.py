#!/usr/bin/env python

from resource_management import *
import sys
import os
import re

class configinit(Script):

  def create_pg_dba(self,env):
	Logger.info("create a dba user for pg")
#	os.system('useradd postgre')

  def get_avilable_dir(self,env):
	Logger.info("get avilable dir for pg data")
	
  def update_pg(self, env):
	import params
	Logger.info("update config -- on (dir) :")
	Logger.info(params.pgxx_install_path)
	Logger.info("create postgresql.conf  --")
	File(os.path.join(params.pgxx_install_path,'postgresql.conf'),
         mode=0644,
         content=Template("pg.postgre.j2")
         )

	Logger.info("create pg_hba.conf")
	File(os.path.join(params.pgxx_install_path,'pg_hba.conf'),
         mode=0644,
         content=Template("pg.hba.j2")
         )


if __name__ == "__main__":
  pass
  
  
