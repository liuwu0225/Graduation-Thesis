import os
import json
import sqlite3
import mwDao
import mwEncrypter
from mwConstant import __VERIFY_TOKEN__, __LOGIN__

class mwUserUtil():
    CLASS_TAG = ''
    
    def __init__(self):
	self.CLASS_TAG = "mwUserUtil.class"

    def mwGetUseridByReq(self, req):
	id_start = req.find("AUTH_")
	if(id_start == -1):
	    return
	id_end = req.find("/", id_start)
	user_id = req[id_start + 5:id_end]
	return user_id

    def mwGetTokenByReq(self, req):
	token_start = req.find('X-Auth-Token:')
	if(token_start == -1):
	    return
        token_end = req.find('"',token_start,-1)
        token = req[token_start+13:token_end]
	return token

    def mwGetFilePathByReq(self, req):
	tag = req.find('AUTH_')
	filepath_start = req.find("/", tag)
	filepath_end = req.find("?", filepath_start)
	filepath = req[filepath_start:filepath_end]
	return filepath

    def mwGetDirByReq(self, req):
	path = self.mwGetFilePathByReq(req)
	fname = path.split("/")[-1]
	directory = path.replace("/"+fname, "")
	return directory

    def mwGetFileNameByReq(self, req):
	path = self.mwGetFilePathByReq(req)
	return path.split("/")[-1]

    def mwCheckToken(self, token):
	req = __VERIFY_TOKEN__.replace("#token#", token);
	data = os.popen(req)
    	data = data.read()
	if(data.find('"status": "0"')!=-1):
	    return True
	else:
	    #print("----the token is expired---")
	    return False

    def mwSaveUserInfo(self, req):
	#create a table to save user info
	cx = sqlite3.connect('/var/log/mwcache.db',isolation_level=None)
	cx.execute('''create table if not exists userInfo(
			user_id varchar[100] not null, 
			password varchar[100] not null);''')
	cx.commit()
	cx.close()
	#parse and save user info
	info_start = req.find('{')
	info_end = req.find('}')
	myinfo = json.loads(req[info_start:info_end+1])
	userid = myinfo["email"].replace("@", "").replace(".", "")
	password = myinfo["password"]
	dao = mwDao.mwDao()
	sqlString = "select * from userInfo where user_id = ?"
	userinfo = dao.find('/var/log/mwcache.db', sqlString, (buffer(mwEncrypter.sAES_str_encrypt(userid, userid)),))
	if(len(userinfo)>0):
	    pass
	else:
	    sqlString = "insert into userInfo values(?,?)"
	    enID = mwEncrypter.sAES_str_encrypt(userid, userid)
	    enPWD = mwEncrypter.sAES_str_encrypt(password, userid)
	    dao.save('/var/log/mwcache.db', sqlString, (buffer(enID), buffer(enPWD)))

    def mwRefreshToken(self, userid):
	dao = mwDao.mwDao()
	sqlString = "select * from userInfo where user_id = ?;"
	enID = mwEncrypter.sAES_str_encrypt(userid, userid)
	userinfo = dao.find('/var/log/mwcache.db', sqlString, (buffer(enID),))
	row =  userinfo[0]
	if(row!=None):
	    userid = mwEncrypter.sAES_str_decrypt(row[0], userid)
	    password = mwEncrypter.sAES_str_decrypt(row[1], userid)
	    #print("id and pwd = " +  userid + "," + password) 
	    req = __LOGIN__.replace("#email#", userid).replace("#password#", password)	
	    data = os.popen(req)
    	    data = data.read()
	    rstjson = json.loads(data)
	    newToken = rstjson["access_token"]
	    return newToken
	return None
	
