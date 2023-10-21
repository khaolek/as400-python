# -*- coding: utf-8 -*-
from itoolkit import *
from itoolkit.transport import DatabaseTransport
import pyodbc

conn = pyodbc.connect("DSN=TPIFILES_DEV;uid=quser;pwd=quser")
itransport = DatabaseTransport(conn)
itool = iToolKit()

itool.add(iCmd5250('wrkactjob', 'WRKACTJOB'))
itool.call(itransport)
wrkactjob = itool.dict_out('wrkactjob')

#print(wrkactjob)
for key, value in wrkactjob.items():
	print(f"key > {key}")
	print(f"value > {value}")
