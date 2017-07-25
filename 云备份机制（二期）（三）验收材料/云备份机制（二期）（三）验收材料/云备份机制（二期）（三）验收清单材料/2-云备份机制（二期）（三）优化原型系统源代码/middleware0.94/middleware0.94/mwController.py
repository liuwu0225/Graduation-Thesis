from ctypes import *
import mwParser
import os
import mwCompresser
import hashlib
import mwEncrypter
import commands
import sys
import sqlite3
import json
import mwFileUtil
import mwUserUtil
import time
import stat
from time import localtime
#import mwChunk
from mwConstant import __CHUNKSIZE__, __JOIN__, __DELETE__, __SEGMENT__

fileUtil = mwFileUtil.mwFileUtil()
userUtil = mwUserUtil.mwUserUtil()
#mwchunk = mwChunk.mwChunk()

class Controller():
    request = ''
    uuid = ''

    def __init__(self,r,u):
        self.request = r
        self.uuid = u 

    def get_token(self):
        token_start = self.request.find('X-Auth-Token:')
        token_end = self.request.find('"',token_start,-1)
        token = self.request[token_start+13:token_end]
        access_token = '{"access_token": "' + token + '"}'
        return access_token

    ###request:to parse the request
    def req(self,rq):
        #parse request
        parser = mwParser.Parser(self.request)
        n = parser.parse()
        result = ''
	#if the request is related to UPLOAD or DOWNLOAD, doing cache analysis
	
	if((n.find('ENCRYPT')==-1 and n.find('COMPRESS')==-1 and n.find('ENCRYPT_COMPRESS')==-1) and (n.find('UPLOAD')!=-1 or n.find('DOWNLOAD')!=-1)):
	    result = self.doCache(rq, n)
	    if(result):
		#print("has cache and copy......")
		result = 'uuid = ' + self.uuid + '\n' + 'mwresult = ' + result +  '\r\n'
		return result
	    else:
		#print("no cache and go on......")
		pass
	else:
	    pass

	if(n == 'GETREQUEST'):
	    #init result
	    result = ''
	    request_json = {'status': '0', 'msg': ''}
	    info = []
	    #get recent
	    index = rq.find("recent=")
	    index_end = rq.find('"', index)
	    recent = int(rq[index + len("recent="):index_end])
	    #get request order by time
	    connect=sqlite3.connect('/var/log/mwlog.db',isolation_level=None)
	    mcursor = connect.cursor()
	    userid = userUtil.mwGetUseridByReq(rq)[:userUtil.mwGetUseridByReq(rq).find('?')]
	    rows = mcursor.execute("select * from Log where userid = '" + userid + "' order by time desc limit %d;"%(recent + 1))
	    #use a number to identify a request
	    number = 0
	    for data in rows:
		number = number + 1
		if(number == 1):
		    continue
		info_element = {}
		info_element["number"] = number - 1
		#get and format the request
	        mrequest = data[0]
		decode_request = mwEncrypter.sAES_str_decrypt(mrequest, "u3v0cBsajphPKuPYqDMqW2DF07L6WxiMyuFKq9od")
	        decode_request = decode_request.replace('\n', '|')
	        decode_request = decode_request.replace('\r|', '')
	        decode_request = decode_request.replace('"', "'")
	        info_element["request"] = decode_request
	        #get state
	        info_element["state"] = data[2]
	        #get and format time
	        timeArray = time.localtime(float(data[3]))
	        mtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
	        info_element["time"] = mtime
    	        #get and format the result
	        mresult = data[5]
	        decode_result = mwEncrypter.sAES_str_decrypt(mresult, "u3v0cBsajphPKuPYqDMqW2DF07L6WxiMyuFKq9od")
	        decode_result = decode_result.replace('\n', '|')
	        decode_result = decode_result.replace('\r|', '')
	        decode_result = decode_result.replace('"', "'")
	        info_element["result"] = decode_result
	        info.append(info_element)
	    connect.close()
	    request_json["info"] = info
	    request_json_dump = json.dumps(request_json)
	    result = 'uuid = ' + self.uuid + '\n' + 'mwresult = ' + request_json_dump +  '\r\n'
	    return result

	if(n == 'WITHDRAWREQUEST'):
	    #init result
	    result = ''
	    request_json = {'status': '0', 'msg': ''}
	    info = []
	    muuid = []
	    #get recent
	    index = rq.find("recent=")
	    index_end = rq.find('"', index)
	    recent = int(rq[index + len("recent="):index_end])
	    #get request order by time
	    connect=sqlite3.connect('/var/log/mwlog.db',isolation_level=None)
	    mcursor = connect.cursor()
	    userid = userUtil.mwGetUseridByReq(rq)[:userUtil.mwGetUseridByReq(rq).find('?')]
	    rows = mcursor.execute("select * from Log where userid = '" + userid + "' and state = 'unfinished' order by time desc limit %d;"%(recent + 1))
	    #use a number to identify a request
	    number = 0
	    for data in rows:
		number = number + 1
		if(number == 1):
		    continue
		info_element = {}
		info_element["number"] = number - 1
		#get and format the request
	        mrequest = data[0]
		decode_request = mwEncrypter.sAES_str_decrypt(mrequest, data[1])
	        decode_request = decode_request.replace('\n', '|')
	        decode_request = decode_request.replace('\r|', '')
	        decode_request = decode_request.replace('"', "'")
	        info_element["request"] = decode_request
		#get uuid
		muuid.append(data[1])
	        #get state
	        info_element["state"] = data[2]
	        #get and format time
	        timeArray = time.localtime(float(data[3]))
	        mtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
	        info_element["time"] = mtime
    	        #get and format the result
	        mresult = data[5]
	        decode_result = mwEncrypter.sAES_str_decrypt(mresult, data[1])
	        decode_result = decode_result.replace('\n', '|')
	        decode_result = decode_result.replace('\r|', '')
	        decode_result = decode_result.replace('"', "'")
	        info_element["result"] = decode_result
	        info.append(info_element)
	    request_json["info"] = info
	    request_json_dump = json.dumps(request_json["info"], sort_keys = True, indent = 4, separators=(',',':'))
	    print(request_json_dump)
	    withdraw_number = 0
	    withdraw_uuid = ''
	    if(len(muuid) < 1):
		result = 'uuid = ' + self.uuid + '\n' + 'mwresult = ' + json.dumps({"status": "0", "msg": "no request can be withdrew!"}) +  '\r\n'
		return result

	    while(True):
	    	withdraw_number = int(raw_input("Please the number of unfinished request <INT>:"))
		if(withdraw_number > len(muuid)):
		    print("Input number is too big, please input again!")
		else:
	    	    withdraw_uuid = muuid[withdraw_number - 1]
		    break
	    try:
		mcursor.execute("delete from Log where userid = '" + userid + "' and uuid = '" + withdraw_uuid + "';")
		result = 'uuid = ' + self.uuid + '\n' + 'mwresult = ' + json.dumps({"status": "0", "msg": "delete successed!"}) +  '\r\n'
	    except:
		result = 'uuid = ' + self.uuid + '\n' + 'mwresult = ' + json.dumps({"status": "-1", "msg": "delete failed!"}) +  '\r\n'
	    return result

        if (n == 'COMPRESSENCRYPTUPLOAD'):
            #upload:compress and encrypt
            #get path
            path_start = rq.find('-T')
            path_end = rq.find('"http',path_start,-1)
            path = rq[path_start+3:path_end-1]
            if (not os.path.exists(path)):
                result = "No such file."
            else:
                #compress
                compress_path = '/tmp/' + self.uuid + '.zip'
                compresser = mwCompresser.Compresser()
                c_result = compresser.compress_file(path,compress_path)
                if(c_result == 'compress success.'):
                    #encrypt
                    encrypt_path = '/tmp/' + self.uuid + '.en'
                    dll = CDLL("/usr/lib/libsecrypto.so")
                    access_token = self.get_token()
                    e_result = mwEncrypter.sAES_encrypt(compress_path,encrypt_path,dll,access_token)
                    if(e_result == 'encrypt success.'):
                        #upload
                        #encrypt_path replace path
			'''
			rq = rq.replace(path,encrypt_path)
			uploadName = userUtil.mwGetFilePathByReq(rq).split("/")[-1]
			rq = rq.replace(uploadName, encrypt_path.split("/")[-1])
			filesize = os.path.getsize(encrypt_path)
			chunksize = __CHUNKSIZE__
			if(filesize > chunksize):
			    result = self.chunkupload(rq, encrypt_path, chunksize)
			else:
			'''
		        rq = rq.replace(path,'"' + encrypt_path + '"')
			#print(rq)
		        result = self.upload(rq)
                        #rq = rq.replace(path,encrypt_path)
                        #result = self.upload(rq)
                    else:
                        #encrypt error
                        result = e_result
                else:
                    result = c_result

        elif(n == 'ENCRYPTUPLOAD'):
            #get path
            path_start = rq.find('-T')
            path_end = rq.find('"http',path_start,-1)
            path = rq[path_start+3:path_end-1]
            if (not os.path.exists(path)):
                result = "No such file."
            else:
                #encrypt
                encrypt_path = '/tmp/' + self.uuid + '.en'
                dll = CDLL("/usr/lib/libsecrypto.so")
                access_token = self.get_token()
                e_result = mwEncrypter.sAES_encrypt(path,encrypt_path,dll,access_token)
                if(e_result == 'encrypt success.'):				
                    #upload
		    '''
		    rq = rq.replace(path,encrypt_path)
		    uploadName = userUtil.mwGetFilePathByReq(rq).split("/")[-1]
		    rq = rq.replace(uploadName, encrypt_path.split("/")[-1])
		    filesize = os.path.getsize(encrypt_path)
		    chunksize = __CHUNKSIZE__
		    if(filesize > chunksize):
			result = self.chunkupload(rq, encrypt_path, chunksize)
		    else:
		    '''
		    rq = rq.replace(path,'"' + encrypt_path + '"')
		    #print(rq)
		    result = self.upload(rq)
                    #rq = rq.replace(path,encrypt_path)
                    #result = self.upload(rq)
                else:
                    result = e_result

        elif(n == 'COMPRESSUPLOAD'):
            #upload:compress and encrypt
            #get path
            path_start = rq.find('-T')
            path_end = rq.find('"http',path_start,-1)
            path = rq[path_start+3:path_end-1]
            if (not os.path.exists(path)):
                result = "No such file."
            else:
                #compress	
                compress_path = '/tmp/' + self.uuid + '.zip'
                compresser = mwCompresser.Compresser()
                c_result = compresser.compress_file(path,compress_path)
                if(c_result == 'compress success.'):
                    #upload
                    #compress_path replace path
		    '''
		    rq = rq.replace(path,compress_path)
		    uploadName = userUtil.mwGetFilePathByReq(rq).split("/")[-1]
		    rq = rq.replace(uploadName, compress_path.split("/")[-1])
		    filesize = os.path.getsize(compress_path)
		    chunksize = __CHUNKSIZE__
		    if(filesize > chunksize):
			result = self.chunkupload(rq, compress_path, chunksize)
		    else:
		    '''
		    rq = rq.replace(path,'"' + compress_path + '"')
		    #print(rq)
		    result = self.upload(rq)
                    #rq = rq.replace(path,compress_path)
                    #result = self.upload(rq)
                else:
                    result = c_result

        elif(n == 'UPLOAD'):
            path_start = rq.find('-T')
            path_end = rq.find('"http',path_start,-1)
            path = rq[path_start+3:path_end-1]
            if (not os.path.exists(path)):
                result = "No such file."
            else:
		filesize = os.path.getsize(path)
		chunksize = __CHUNKSIZE__
		if(filesize > chunksize):
		    result = self.chunkupload(rq, path, chunksize)
		else:
                    rq = rq.replace(path,'"' + path + '"')
		    #print(rq)
                    result = self.upload(rq)

        elif(n == 'DECRYPTDECOMPRESSDOWNLOAD'):
            #download:decrypt and decompress
            path_start = rq.find('-o')
            path = rq[path_start+3:]
            #download	    
            decrypt_path = '/tmp/' + self.uuid + '.de'    
            rq = rq.replace(path,decrypt_path)
	    filesize = self.getUploadFileLength(rq)
	    if(filesize == -1):
		return'uuid = ' + self.uuid + '\n' + 'mwresult = ' + json.dumps({"status": "-1", "msg": "no such file"}) +  '\r\n'
	    chunksize = __CHUNKSIZE__
	    if(filesize>chunksize):
		result = self.chunkdownload(rq, decrypt_path, filesize, chunksize)
	    else: 
                result = self.download(rq,path)
            #result = self.download(rq,path)
            #download success
            if(result.find('download success.') != -1):
                #decrypt
                decompress_path = '/tmp/' + self.uuid + '.zip'
                dll = CDLL("/usr/lib/libsecrypto.so")
                access_token = self.get_token()
                e_result = mwEncrypter.sAES_decrypt(decrypt_path,decompress_path,dll,access_token)
                if(e_result == 'decrypt success.'):		
                    #decompress	    
                    compresser = mwCompresser.Compresser()
                    c_result = compresser.decompress_file(decompress_path,path)
                    if(c_result == 'decompress success.'):
                        pass
                    else:
                        result = c_result
                else:
                    result = e_result
            else:
                pass

        elif(n == 'DECRYPTDOWNLOAD'):
            #download:decrypt
            path_start = rq.find('-o')
            path = rq[path_start+3:]
            #download
            decrypt_path = '/tmp/' + self.uuid + '.de'
            rq = rq.replace(path,decrypt_path)
	    filesize = self.getUploadFileLength(rq);
	    if(filesize == -1):
		return'uuid = ' + self.uuid + '\n' + 'mwresult = ' + json.dumps({"status": "-1", "msg": "no such file"}) +  '\r\n'
	    chunksize = __CHUNKSIZE__
	    if(filesize>chunksize):
		result = self.chunkdownload(rq, decrypt_path, filesize, chunksize)
	    else: 
                result = self.download(rq,path)
            #result = self.download(rq,path)
            #download success
            if(result.find('download success.') != -1):
                #decrypt
                dll = CDLL("/usr/lib/libsecrypto.so")
                access_token = self.get_token()
                e_result = mwEncrypter.sAES_decrypt(decrypt_path,path,dll,access_token)
                if(e_result == 'decrypt success.'):
                    pass
                else:
                    result = e_result
            else:
                pass

        elif(n == 'DECOMPRESSDOWNLOAD'):
            #download:decrypt and decompress
            path_start = rq.find('-o')
            path = rq[path_start+3:]
            #download	    
            decompress_path = '/tmp/' + self.uuid + '.zip'    
            rq = rq.replace(path,decompress_path)
	    filesize = self.getUploadFileLength(rq);
	    if(filesize == -1):
		return'uuid = ' + self.uuid + '\n' + 'mwresult = ' + json.dumps({"status": "-1", "msg": "no such file"}) +  '\r\n'
	    chunksize = __CHUNKSIZE__
	    if(filesize>chunksize):
		result = self.chunkdownload(rq, decompress_path, filesize, chunksize)
	    else: 
                result = self.download(rq,path)
            #result = self.download(rq,path)
            if(result.find('download success.') != -1):
                #decompress	    
                compresser = mwCompresser.Compresser()
                c_result = compresser.decompress_file(decompress_path,path)
                if(c_result == 'decompress success.'):
                    pass
                else:
                    result = c_result
            else:
                pass

        elif(n == 'DOWNLOAD'):
            #download
            path_start = rq.find('-o')
            path = rq[path_start+3:]	
	    chunksize = __CHUNKSIZE__
	    src_path = userUtil.mwGetFilePathByReq(rq)
	    userid = userUtil.mwGetUseridByReq(rq)
	    token = userUtil.mwGetTokenByReq(rq)
	    #get the file length, and decide to download the file directly or chunkdownload
	    file_attr = fileUtil.mwGetFileAttr(src_path, userid, token)
	    if(file_attr=="not found"):
		return'uuid = ' + self.uuid + '\n' + 'mwresult = ' + json.dumps({"status": "-1", "msg": "no such file"}) +  '\r\n'
	    flen_start = file_attr.find("""bytes":""")
	    flen_end = file_attr.find("}", flen_start)
     	    flen = file_attr[flen_start + len("""bytes":"""):flen_end]
	    flen = int(flen)
	    if(flen > chunksize):
		#result = mwchunk.chunkdownload(rq, path, flen, chunksize)
		result = self.chunkdownload(rq, path, flen, chunksize)
	    else: 
                result = self.download(rq,path)

        else:
            #transfer
            result = self.transfer(rq)

        result = 'uuid = ' + self.uuid + '\n' + 'mwresult = ' + result +  '\r\n'
	#result = 'uuid = ' + self.uuid + '\n' + 'mwresult = ' + result
        return result

    ###upload:call uploader module
    def upload(self,rq):
        #generate log
        #logpath = hashlib.md5(self.request).hexdigest()	
        logpath = '/tmp/' + self.uuid + '.log'    #record log to get information
        #curl
        upload_req = 'curl ' + rq + ' 2>&1 | tee ' + logpath
        #get return
        result = commands.getoutput(upload_req)
        result_start = result.find('{')
        if(result_start != -1):
            result = result[result_start:]
        else:
            result = 'upload failed.' 
        return result

    ###download:call downloader module
    def download(self,rq,path):
        #generate log
        #logpath = hashlib.md5(self.request).hexdigest()	
        logpath = '/tmp/' + self.uuid + '.log'    #record log to get information
        #curl
        download_req = 'curl ' + rq + ' 2>&1 | tee ' + logpath
        path_start = rq.find('-o')
        download_path = rq[path_start+3:]
        if download_path.find(" ") != -1:
            download_req = download_req.replace(download_path,"'" + download_path + "'")
        os.system(download_req)
        if (not os.path.exists(download_path)):
            result = path + ' download failed.'
        else:
            result = path + ' download success.'          
        return result

    ###transfer
    def transfer(self,rq):
        #curl
        transfer_req = 'curl ' + rq
        result = os.popen(transfer_req) 
        result = result.read()
	#if the rq is related to delete a file or rename a file  
	#we must update the user table, or the data is not consistent with the server
	cx = sqlite3.connect('/var/log/mwcache.db')
	userid = userUtil.mwGetUseridByReq(rq)
	fpath = userUtil.mwGetFilePathByReq(rq)
	if(rq.find('op=DELETE')!=-1):
	    cx.execute("delete from user where user_id = '" + userid + "' and server_path = '" + fpath + "';")
	if(rq.find('op=RENAME')!=-1):
	    newpath_start = rq.find("destination=")
	    newpath_end = rq.find("&", newpath_start)
	    newpath = rq[newpath_start + len("destination="):newpath_end]
	    cx.execute("update user set server_path = '" + newpath + "' where user_id = '" + userid + "' and server_path = '" + fpath + "';")
	if(rq.find('op=MOVE')!=-1 and rq.find('op=MOVERECYCLE')==-1):
	    newpath_start = rq.find("Destination:")
	    newpath_end = rq.find('"', newpath_start)
	    newpath = rq[newpath_start + len("Destination:"):newpath_end]
	    cx.execute("update user set server_path = '" + newpath + "' where user_id = '" + userid + "' and server_path = '" + fpath + "';")
	cx.commit()
	cx.close()
        return result

    ###chunk upload for big file
    def chunkupload(self, rq, path, chunksize):
	result = ''
	rqStamp = rq
	userid = userUtil.mwGetUseridByReq(rq)
	MD5 = fileUtil.mwGetFileMD5(path)
	token = userUtil.mwGetTokenByReq(rq)
	#create a table to save breakpoint if not exists
	breakpoint = 0
	cx = sqlite3.connect('/var/log/mwcache.db',isolation_level=None)
	cx.execute('''create table if not exists breakpoint(
	    	user_id varchar[100] not null, 
		MD5 varchar[100] not null,
		server_path varchar[100] not null,
		point int not null default 0,
		flag bit not null default 0);''')
	point_result = cx.execute("select * from breakpoint where user_id = '" + userid + "' and MD5 = '" + MD5 + "' and flag = 1")
	for point in point_result:
	    if(point[3]):
		breakpoint = point[3]
	#create a temp file for storing chunk files
	tempfile = sys.path[0] + "/mwcache/uploadtemp/temp-" + userid
	if not os.path.exists(tempfile):
	    os.makedirs(tempfile)
	    os.chmod(tempfile, stat.S_IRWXU)
	else:
	    for fname in os.listdir(tempfile):
	        os.remove(os.path.join(tempfile, fname))
	#Split the big file and upload chunks seperately
	fileUtil.mwSplitFile(path, tempfile, chunksize)
	files = os.listdir(tempfile)
	files.sort()
	chunk_file_path = []
	chunk_file_attr = []
	flag = 0
	temppath = ''
	tempfilename = ''
	#upload file parts to segments  
	rq = rq.replace(userUtil.mwGetDirByReq(rq), "/segments")
	start = rq.find("overwrite")
	end = rq.find("&", start)
	rq = rq.replace(rq[start:end], "overwrite=true")
	for filepart in files:
	    #skip parts which have uploaded before
	    if(breakpoint>0):
	        breakpoint = breakpoint - 1
	  	chunk_file_path.append("/segments/" + filepart)
	    	continue
	    newpath = os.path.join(tempfile, filepart)
	    #replace the file path being upload with the file chunk path 
 	    if(flag == 0):
	        rq = rq.replace(path,newpath)
	    	rq = rq.replace(userUtil.mwGetFileNameByReq(rq) + "?op",  filepart + "?op")
	    	flag += 1 
	    else:
	    	rq = rq.replace(temppath, newpath)
	    	rq = rq.replace(tempfilename + '?op',filepart + '?op')
            try:
	    	result = self.upload(rq)
	    	temppath = newpath
	     	tempfilename = filepart
	     	chunk_file_path.append(userUtil.mwGetFilePathByReq(rq))
	    except:
		point = int(filepart[4]) - 1
		server_path = userUtil.mwGetFilePathByReq(rqStamp)
		cx.execute("insert into breakpoint values(?,?,?,?,?)", (userid, MD5, server_path, point, 1))
	#create a join request and join the chunks in the server side
	#cx.execute("delete from breakpoint where MD5 = '" + MD5 + "';")
	file_attr = ''
	for fpath in chunk_file_path:
	    chunk_file_attr.append(fileUtil.mwGetFileAttr(fpath, userid, token))
	for fattr in chunk_file_attr:
	    file_attr += fattr + ","
	#delete the last ","
	file_attr = file_attr[:-1]
	join_req = __JOIN__.replace("#file_attr#", file_attr)
	join_req = join_req.replace("#token#", token)
	join_req = join_req.replace("#userid#", userid)
	join_req = join_req.replace("#path#", userUtil.mwGetFilePathByReq(rqStamp))
	#print(join_req)
	data = os.popen(join_req)
	data = data.read()
	#delete temp file in the server side
	'''
	if(data.find("\"status\": \"0\"")!=-1):
	    fname = userUtil.mwGetFilePathByReq(rqStamp).split("/")[-1]
	    dpath = userUtil.mwGetFilePathByReq(rqStamp).replace(fname, "")
	    del_req = __DELETE__.replace("#userid#", userid).replace("#token#", token)
	    for filepart in files:
	        del_req = del_req.replace("#file_path#", dpath+filepart)
	        data = os.popen(del_req)
	        data = data.read()
	        del_req = del_req.replace(dpath+filepart, "#file_path#")
	'''
	cx.commit()
	cx.close()
	return result

    #chunk download for big file
    def chunkdownload(self, rq, path, flen, chunksize):
	#create a temp file based on userid to save chunk files, if the temp file exists, remove all files
	userid = userUtil.mwGetUseridByReq(rq)
	tempfile = sys.path[0] + "/mwcache/downloadtemp/temp-" + userid
	if not os.path.exists(tempfile):
	    os.makedirs(tempfile)
	    os.chmod(tempfile, stat.S_IRWXU)
	else:
	    for fname in os.listdir(tempfile):
	        os.remove(os.path.join(tempfile, fname))
	#variables used for chunk download
	result = ''
	temppath = ''
	i = 1
	offset = 0
	while(flen-offset >0 ):
	    #replace length
	    len_start = rq.find("length")
	    len_end = rq.find("&", len_start)
	    prelen = rq[len_start:len_end]
	    if(flen-offset >= chunksize):
		rq = rq.replace(prelen, "length=%d"%chunksize)
	    else:
		rq = rq.replace(prelen, "length=%d"%(flen-offset))
	    #replace offset
	    offset_start = rq.find("offset")
	    offset_end = rq.find("&", offset_start)
	    preoffset = rq[offset_start:offset_end]
	    rq = rq.replace(preoffset, 'offset=%d'%offset)
	    #replace path
	    chunkpath = tempfile +"/" + path.split('/')[-1]+ "-part%d"%i + ".tmp"
	    if(i<=1):     
	        rq = rq.replace(path, chunkpath)
	    else:
		rq = rq.replace(temppath, chunkpath)
	    i += 1
	    offset += chunksize
	    temppath = chunkpath
	    result = self.download(rq,chunkpath)
	#join chunk files
	#if the file exists, this join operation will overwrite the old file
	filename = path.split('/')[-1]
	todir = path.replace('/' + filename, '')
	fileUtil.mwJoinFile(tempfile, filename, todir)
    	return result

    def doCache(self, rq, n):
	result = ''
	#create and connect a table if not exists to record cache files
	cx = sqlite3.connect('/var/log/mwcache.db',isolation_level=None)
	cx.execute('''create table if not exists fileCache(
			user_id varchar[100] not null, 
			file_name varchar[100] not null,
			length bigint not null,
			MD5 varchar[100] not null,
			use_time int not null,
			modified_time varchar[100] not null);''')
	#create a table to record use_time while the the cache is full
	cx.execute('''create table if not exists fileTemp(
			MD5 varchar[100] not null,
			use_time int default 0);''')
	#create a table to record the server_path for every user sperately
	cx.execute('''create table if not exists user(
			user_id varchar[100] not null, 
			MD5 varchar[100] not null,
			server_path varchar[100] not null);''')
	#if the request is related to UPLOAD
	if(n.find('UPLOAD')!=-1):
	    result = fileUtil.mwUploadCache(rq)
	#if the request is related to DOWNLOAD
	elif(n.find('DOWNLOAD')!=-1):
	    result = fileUtil.mwDownloadCache(rq)
	else:
	    result = False
	return result
	
    def getUploadFileLength(self, rq):	
	src_path = userUtil.mwGetFilePathByReq(rq)
	userid = userUtil.mwGetUseridByReq(rq)
	token = userUtil.mwGetTokenByReq(rq)
	#get the file length, and decide to download the file directly or chunkdownload
	file_attr = fileUtil.mwGetFileAttr(src_path, userid, token)
	if(file_attr=="not found"):
	    return -1
	flen_start = file_attr.find("""bytes":""")
	flen_end = file_attr.find("}", flen_start)
     	flen = file_attr[flen_start + len("""bytes":"""):flen_end]
	flen = int(flen)
	return flen; 
	    
	





