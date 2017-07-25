import sys
import os
import stat
import json
import hashlib
import sqlite3
import shutil
import time
from time import localtime
import mwUserUtil
from mwConstant import __COPY__, __CACHESIZE__, __CACHEPATH__, __RENAME__

userUtil = mwUserUtil.mwUserUtil()

class mwFileUtil():
    CLASS_TAG = ''
    
    def __init__(self):
	self.CLASS_TAG = "mwFileUtil.class"

    def mwSplitFile(self, fromfile, todir, chunksize = 81920):
	if not os.path.exists(todir):
	    os.mkdir(todir)
        else:
	    for fname in os.listdir(todir):
	        os.remove(os.path.join(todir, fname))
        partnum = 0
        try:
            inputfile = open(fromfile, 'rb')
        except:
    	    print("open file failed")
        while True:
	    try:
	        chunk = inputfile.read(chunksize)
	    except:
	        print("read failed")
	    if not chunk:
	        break
	    partnum += 1
	    t = '%.4f' %time.time()
	    filename = os.path.join(todir, ("part%d"%(partnum)+self.mwGetFileMD5(fromfile)+"."+fromfile.split(".")[-1])) 
	    fileobj = open(filename, 'wb')
	    fileobj.write(chunk)
	    fileobj.close()
        inputfile.close()
	return partnum

    def mwJoinFile(self, fromdir, filename, todir):
	if not os.path.exists(todir):
	    os.mkdir(todir)
        if not os.path.exists(fromdir):
	    print("No such firectory")
	    return

        outfile = open(os.path.join(todir, filename), 'wb')
        files = os.listdir(fromdir)
        files.sort()
        for filepart in files:
	    filepath = os.path.join(fromdir, filepart)
	    infile = open(filepath, 'rb')
	    data = infile.read()
	    outfile.write(data)
	    infile.close()
        outfile.close()
	
    def mwGetFileAttr(self, filepath, userid, token):
	req_url = '''curl -k "https://192.168.7.62:443/v1/AUTH_'''
	req_attr = '''?op=GETFILEATTR&version=LATEST"'''
	req = req_url + userid + filepath + req_attr + ''' -H "X-Auth-Token:''' + token + '''"'''
	data = os.popen(req)
	data = data.read()
	
	etag = ''
	size_bytes = ''
        if data:
            tmp_result = json.loads(data)
            if("ETag" in tmp_result and "Content-Length" in tmp_result):
                etag = tmp_result["ETag"]
                size_bytes = tmp_result["Content-Length"]
            else:
                return tmp_result["msg"]
	#example of a file attribute
	#file1 = '''{"path":"/segments/part1.docx","etag":"a5d24786392184cc2f38f3da511a430e","size_bytes":81920},'''
	result = '''{"path":"''' + filepath + '''","etag":"''' + etag + '''","size_bytes":''' + size_bytes + "}"
	return result 

    def mwGetFileMD5(self, path):
	mfile = open(path, 'rb')
	mfile_content = mfile.read()
	mfile.close()
	return hashlib.md5(mfile_content).hexdigest()

    def mwUploadCache(self, rq):
	#print("-----mwUploadCache-----")
	result = False
	#get upload file path from request
	path_start = rq.find('-T')
        path_end = rq.find('"http',path_start,-1)
        path = rq[path_start+3:path_end-1]
	#check if the file had a copy in cache by MD5
	user_id = userUtil.mwGetUseridByReq(rq)
	MD5 = self.mwGetFileMD5(path)
	cx = sqlite3.connect('/var/log/mwcache.db')
	spath_result = cx.execute("select server_path from user where user_id = '" + user_id + "' and MD5 = '" + MD5 + "';")
	for row in spath_result: 
	    if(row[0]): 
		#print("-----has cache-----")
		result = True
		#if the file had a copy in cache 
		#update the fileCache with user_id, file_name, the use_times + 1, modified_time; 
		file_name = path.split('/')[-1]
		use_times = 0
		use_times_result = cx.execute("select use_time from fileCache where MD5 = '" + MD5 + "';")
		for times in use_times_result:
		    use_times = times[0] + 1
		tm = time.strftime('%Y-%m-%d %H:%M:%S', localtime())
		cx.execute("update fileCache set user_id = '" + user_id + "', use_time = %d"%use_times + ", modified_time = '" + tm + "' where MD5 = '" + MD5 + "';")
		cx.commit()
		cx.close()
		#if the file had a copy in cache 
		#call the copy API instead of calling upload API to save both I/O and calculate operation at middleware side
		userid = userUtil.mwGetUseridByReq(rq)
		#get src_path of the file
		src_path = row[0]
		token = userUtil.mwGetTokenByReq(rq)
		#get des_path
		path_start = rq.find(userid)
		path_end = rq.find("?", path_start)
		des_path = rq[path_start + len(userid): path_end]
		#create a copy request
		cp_req = __COPY__.replace("#userid#", userid)
		cp_req = cp_req.replace("#src_path#", src_path)
		cp_req = cp_req.replace("#token#", token)
		cp_req = cp_req.replace("#des_path#", des_path)
		data = os.popen(cp_req)
		data = data.read()
		return data
	    else:
		pass
	#if the loop ended and can not find a MD5 equals the file MD5, it means there is no file in the cache
	#so put the file into cache and record in the database if does not surpass the max capacity  of the cache  
	#if the file exists in the cache then set has_cache = true 
	has_cache = False
	MD5_result = cx.execute("select MD5 from fileCache where MD5 = '" + MD5 + "';")
	for MD5s in MD5_result:
	    if(MD5s[0]):
		has_cache = True
	    else:
		pass
	#else get the cache size and compare to the max size
	cache_size = 0
	file_size_result = cx.execute("select length from fileCache;")
	for fsize in file_size_result:
	    cache_size += fsize[0]
	cache_size += os.path.getsize(path)
	if(cache_size > __CACHESIZE__):
	#if surpass the max size, replace cache file with LRU strategy
	    #print("surpass max size!")
	    self.doLRU(rq, cx, path, MD5)
	else:
	    #put the file into cache and record in the database
	    #put into cache
	    cache = sys.path[0] + "/mwcache/cache"
	    if not os.path.exists(cache):
	    	os.makedirs(cache)
	    	os.chmod(cache, stat.S_IRWXU)
	    shutil.copy(path, cache)
	    #record in the database
	    user_id = userUtil.mwGetUseridByReq(rq)
	    file_name = path.split('/')[-1]
	    length = os.path.getsize(path)
	    MD5 = self.mwGetFileMD5(path)
	    path_start = rq.find(user_id)
	    path_end = rq.find("?", path_start)
	    server_path = rq[path_start + len(user_id): path_end]
	    use_times = 1
	    tm = time.strftime('%Y-%m-%d %H:%M:%S', localtime())
	    if(has_cache):
		pass
	    else:
	        cx.execute("insert into fileCache values('" + user_id + "', '" + file_name + "', %d"%length + ", '" + MD5 + "', %d"%use_times + ", '" + tm + "');")
	    #insert into table user to record the server path.
	    cx.execute("insert into user values('" + user_id + "', '" + MD5 + "', '" + server_path + "');")
	cx.commit()
	cx.close()
	return result
	
    def mwDownloadCache(self, rq):
	#print("-----mwDownloadCache-----")
	result = False
	#get download file MD5 by sending a get file_attr request
	filepath = userUtil.mwGetFilePathByReq(rq)
	user_id = userUtil.mwGetUseridByReq(rq)
	token = userUtil.mwGetTokenByReq(rq)
	file_attr = self.mwGetFileAttr(filepath, user_id, token)
	MD5_start = file_attr.find('''etag":"''')
	MD5_end = file_attr.find('''",''', MD5_start)
     	MD5 = file_attr[MD5_start + len('''etag":"'''):MD5_end]
	#check if the file had a copy in cache by MD5
	cx = sqlite3.connect('/var/log/mwcache.db')
	fname_result = cx.execute("select file_name from fileCache where MD5 = '" + MD5 + "';")
	for fname in fname_result:
	    if(fname[0]):
		result = True
		#if the download file had a copy in cache, copy the cache file to the destination
		cache_path = sys.path[0] + "/mwcache/cache" + "/" + fname[0]
	    	if not os.path.exists(cache_path):
		    os.makedirs(cache_path)
	    	    os.chmod(cache_path, stat.S_IRWXU)
		des_start = rq.find('-o')
        	destination = rq[des_start+3:]
		shutil.copy(cache_path, destination)
		#update the fileCache
		use_times_result = cx.execute("select use_time from fileCache where MD5 = '" + MD5 + "';")
		for times in use_times_result:
		    use_times = times[0]
		use_times += 1
		tm = time.strftime('%Y-%m-%d %H:%M:%S', localtime())
		cx.execute("update fileCache set user_id = '" + user_id + "', use_time = %d"%use_times + ", modified_time = '" + tm + "' where MD5 = '" + MD5 + "';")
		cx.commit()
		return "There is a copy locally and copy it to the download path!"
	    else:
		pass
	cx.close()
        return result

    def doLRU(self, rq, cx, path, MD5):
	#set init use_time = 1
	use_time = 1
	#query use_time of the temp file and add 1 if exists
	ftemp_result = cx.execute("select * from fileTemp where MD5 = '" + MD5 + "';")
	for ftemp in ftemp_result:
	    if(ftemp[1]):
		use_time = ftemp[1] + 1
	    else:
		pass
	#do LRU logic
	total_length = 0
	flength = os.path.getsize(path)
	fcache_result = cx.execute("select * from fileCache where use_time <= %d"%use_time + " order by use_time, modified_time;")
	for fcache in fcache_result:
	    total_length = total_length + fcache[2]
	    cx.execute("delete from fileCache where MD5 = '" + fcache[3] + "';")
	    os.remove(sys.path[0] + "/mwcache/cache/" + fcache[1])
	    if(total_length < flength):
		continue
	    else:
		cx.execute("delete from fileTemp where MD5 = '" + MD5 + "';")
		user_id = userUtil.mwGetUseridByReq(rq)
	    	file_name = path.split('/')[-1]
	    	tm = time.strftime('%Y-%m-%d %H:%M:%S', localtime())
		path_start = rq.find(user_id)
	    	path_end = rq.find("?", path_start)
	   	server_path = rq[path_start + len(user_id): path_end]
		cx.execute("insert into fileCache values('" + user_id + "', '" + file_name + "', %d"%flength + ", '" + MD5 + "', %d"%use_time + ", '" + tm + "');")
		cx.execute("insert into user values('" + user_id + "', '" + MD5 + "', '" + server_path + "');")		
		shutil.copy(path, sys.path[0] + "/mwcache/cache/" + file_name)
		return True;
	#if there are no file which use_time is less than temp file, put the temp file into fileTemp
	if(use_time == 1):
	    cx.execute("insert into fileTemp values('"+ MD5 + "', 1)")
	else:
	    cx.execute("update fileTemp set use_time = %d"%use_time + " where MD5 = '" + MD5 + "';")
