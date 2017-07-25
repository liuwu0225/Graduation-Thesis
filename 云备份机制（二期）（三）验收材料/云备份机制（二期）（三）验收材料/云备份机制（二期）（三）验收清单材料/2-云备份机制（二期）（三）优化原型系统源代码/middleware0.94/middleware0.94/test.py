import os
from ctypes import *
import mwEncrypter
import sqlite3
import chardet
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

req = '''-k -X DELETE "https://192.168.7.62:443/v1/AUTH_kaeyika163com/cache1/test.docx?op=DELETE&ftype=f&cover=" -H "X-Auth-Token:u3v0cBsajphPKuPYqDMqW2DF07L6WxiMyuFKq9od"'''

enreq = mwEncrypter.sAES_str_encrypt(req, "aaa")
uuid = '++++++++++++++++++++'
t = '45646541321'
userid = 'kaeyika163com'

sql_connection = sqlite3.connect('/home/herh/lw/mwlog.db',isolation_level=None)
sql_connection.execute('''create table if not exists Log(request text not null, uuid char[33] not null,state char[20] not null,time char[20] not null,userid varchar[100] not null,result text not null);''')

try:
    sql_connection.execute("insert into Log values(?,?,?,?,?,?);", (buffer(enreq), uuid, "unfinished", t, userid, ""))
    #sql_connection.execute("insert into Log values('"+enreq+ "','" + uuid + "','unfinished','" + t + "','"+userid+"','');")
    print("insert successed") 
    #sql_cursor = sql_connection.cursor()
    reqs = sql_connection.execute("select request from Log;")
    for mreq in reqs:
        myreq = mreq[0]
        print(myreq)
        dereq = mwEncrypter.sAES_str_decrypt(myreq, "u3v0cBsajphPKuPYqDMqW2DF07L6WxiMyuFKq9od")
        print(dereq)
        break
except Exception,e:
    print("insert failed")  
    print Exception,":",e                        
