import sqlite3
import time
import os

class mwDao():
    CLASS_TAG = ''
    
    def __init__(self):
	self.CLASS_TAG = "mwDao.class"

    def save(self, db, sqlString, params):
        try:
	    sql_conn = sqlite3.connect(db, isolation_level=None)
	    sql_conn.execute(sqlString, params)
	    sql_conn.commit()
	    sql_conn.close()
        except Exception,e:
	    print Exception,":",e
    '''
    def update(self, sqlString):

    def delete(self, sqlString):
    '''
    def find(self, db, sqlString, params):
	info = []
	try:
	    sql_conn = sqlite3.connect(db, isolation_level=None)
	    rst = sql_conn.execute(sqlString, params)
	    for row in rst:
	    	if(row):
		    info.append(row)
	    sql_conn.close()
	    return info    
        except Exception,e:
	    print Exception,":",e
    

    
