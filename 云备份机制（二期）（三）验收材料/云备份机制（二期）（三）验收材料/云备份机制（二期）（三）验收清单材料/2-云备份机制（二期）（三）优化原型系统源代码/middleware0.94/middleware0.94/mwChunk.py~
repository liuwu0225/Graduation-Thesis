import os
import mwUserUtil
import mwFileUtil
import mwController

fileUtil = mwFileUtil.mwFileUtil()
userUtil = mwUserUtil.mwUserUtil()

class mwChunk():
    CLASS_TAG = ''

    def __init__(self):
	self.CLASS_TAG = "mwChunk.class"

    ###chunk upload for big file
    def chunkupload(self, rq, path, chunksize):
	#create a temp file for storing chunk files
	userid = userUtil.mwGetUseridByReq(rq)
	#tempfile = "/home/herh/lw/uploadtemp/temp-" + userid
	tempfile = sys.path[0] + "/mwcache/uploadtemp/temp-" + userid
	if not os.path.exists(tempfile):
	    os.mkdirs(tempfile)
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
	for filepart in files:
	    #replace the file path being uploaded with the file chunk path
	    newpath = os.path.join(tempfile, filepart)
 	    if(flag == 0):
	        rq = rq.replace(path,newpath)
	 	rq = rq.replace(path.split("/")[-1] + "?op","/" + filepart + "?op")
		flag += 1 
	    else:
		rq = rq.replace(temppath, newpath)
		rq = rq.replace(tempfilename + '?op',filepart + '?op')
            result = mwController.Controller.upload(rq)
	    temppath = newpath
	    tempfilename = filepart
	    chunk_file_path.append(userUtil.mwGetFilePathByReq(rq))
	    
	#create a join request and join the chunks in the server side
	join_req = '''curl -k -i -X PUT -d '['''
	join_userid = ''']' "https://192.168.7.62:443/v1/AUTH_'''
	join_token = '''?multipart-manifest=put&overwrite=false" -H "X-Auth-Token:'''
	join_end = '''" -H "X-Static-Large-Object: true"'''
	#userid = userUtil.mwGetUseridByReq(rq)
	token = userUtil.mwGetTokenByReq(rq)
	for fpath in chunk_file_path:
	    chunk_file_attr.append(fileUtil.mwGetFileAttr(fpath, userid, token))
	for fattr in chunk_file_attr:
	    join_req += fattr + ","
	#delete the last ","
	join_req = join_req[:-1]
	join_req += join_userid + userid + join_token + token + join_end
	print("------join_req-------")
	print(join_req)	
	data = os.popen(cp_req)
	data = data.read()
	return data

    #chunk download for big file
    def chunkdownload(self, rq, path, flen, chunksize):
	#create a temp file based on userid to save chunk files, if the temp file exists, remove all the files
	userid = userUtil.mwGetUseridByReq(rq)
	downloadtemp = "/home/herh/lw/downloadtemp/temp-" + userid
	if not os.path.exists(downloadtemp):
	    os.mkdir(downloadtemp)
	else:
	    for fname in os.listdir(downloadtemp):
	        os.remove(os.path.join(downloadtemp, fname))
	
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
	    chunkpath = downloadtemp +"/" + path.split('/')[-1]+ "-part%d"%i + ".tmp"
	    if(i<=1):     
	        rq = rq.replace(path, chunkpath)
	    else:
		rq = rq.replace(temppath, chunkpath)
	    i += 1
	    offset += chunksize
	    temppath = chunkpath
	    result = mwController.Cntroller.download(rq,chunkpath)
	#join chunk files
	#if the file exists, this join operation will overwrite the old file
	filename = path.split('/')[-1]
	todir = path.replace('/' + filename, '')
	fileUtil.mwJoinFile(downloadtemp, filename, todir)
    	return result
