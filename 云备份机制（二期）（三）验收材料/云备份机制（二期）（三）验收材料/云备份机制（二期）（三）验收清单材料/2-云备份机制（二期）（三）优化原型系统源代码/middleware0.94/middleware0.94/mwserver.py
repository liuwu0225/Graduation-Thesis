#!/usr/bin/python

import socket, select
import mwDaemon
import mwController 
import mwEncrypter
import mwUserUtil
import mwFirefoxHelper
import mwDao
import hashlib
import threading
import sqlite3
import time
import os
from Queue import Queue

firefoxHelper = mwFirefoxHelper.mwFirefoxHelper()
userUtil = mwUserUtil.mwUserUtil()
dao = mwDao.mwDao() 

#initial port and buffer
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
PORT = 10000
current_time = ''
FromFirefox = False

global mwhandlequeue
mwhandlequeue = Queue()     #mwhandlequeue-request from client

mwrecoveryqueue = Queue()  

class Mwhandlethread(threading.Thread):     #mwhandle thread
    def run(self):
        connect=sqlite3.connect('/var/log/mwlog.db',isolation_level=None)
        while True:
            for i in range(1):
                if mwhandlequeue.qsize() < 1:
                    pass
                else:
                    clientreq = mwhandlequeue.get()
                    #compute uuid 
                    uuid = hashlib.md5(clientreq).hexdigest()
                    #get mwreq
                    mwreq_start = clientreq.find('\nrequest = ')
                    mwreq = clientreq[mwreq_start+11:-2]
                    msg = self.name + 'have handle '+ mwreq
                    #print msg
                    #handle request
                    controller = mwController.Controller(mwreq,uuid)
                    mwresult = controller.req(mwreq)
		    #print(mwresult)
                    #update db
		    enres = mwEncrypter.sAES_str_encrypt(mwresult, uuid)
                    while (1):
                        try:
			    connect.execute("update Log set state=?,result=? where uuid=?;", ("not return", buffer(enres), uuid))
                        except Exception,e:
			    print Exception,":",e
                            break
                        break
                    #return to client
                    userid = getUserId(clientreq)
                    #print userid
                    client_socket = soc_uuid_dict.get(userid)
		    if(FromFirefox):
			client_socket = soc_uuid_dict.get("fx_"+userid)
                    if (client_socket==None):
                        continue 
                    try:
			if(FromFirefox):
			    start = mwresult.find("mwresult = ")
			    end = mwresult.find("}")
			    mwresult = mwresult[start+len("mwresult = "):end+len("}")]
			    offset = 0
			    while(offset<len(mwresult)):
				res_start = offset
				if((len(mwresult)-offset)>=125):
				    res_end = offset+125
				    client_socket.send('%c%c%s' % (0x81, res_end-res_start, mwresult[res_start:res_end]))
				else:
				    res_end = len(mwresult)
				    client_socket.send('%c%c%s' % (0x81, res_end-res_start+1, mwresult[res_start:res_end]+"#"))
				offset = res_end
			else:
                            client_socket.sendall(mwresult)
                    except:
                        soc_uuid_dict[userid]=None
                        continue
                    while (1):
                        try:
                            connect.execute("update Log set state='finished' where uuid='"+uuid+"';")
                        except:
                            time.sleep(0.01)
                            continue
                        break
                    Remove(uuid)
                    #time.sleep(1)

#remove the scrath file
def Remove(uuid):
    path='/tmp/'+uuid
    if (os.path.exists(path+'.en')):
        os.remove(path+'.en')
    if (os.path.exists(path+'.de')):
        os.remove(path+'.de')
    if (os.path.exists(path+'.zip')):
        os.remove(path+'.zip')
    if (os.path.exists(path+'.log')):    
        os.remove(path+'.log')
    if (os.path.exists(path+'.tmp')):    
        os.remove(path+'.tmp')

#get userid                    
def getUserId(request):
    id_end=request.find('\ntime = ')
    user_id=request[9:id_end]
    return user_id

#put request into mwhandlequeue
def handle(rq):
    mwhandlequeue.put(rq)    #put request into mwhandlequeue

def handle_revData(data):
    dataend = data.find('\r\n')
    if(dataend != -1):
    	clientrequest = data[:dataend + 2]
        data = data.replace(clientrequest,'')
    return clientrequest

def save_request(clientrequest):
    uuid = hashlib.md5(clientrequest).hexdigest()		    
    userid = getUserId(clientrequest)
    t = '%.4f' %time.time()
    enreq = mwEncrypter.sAES_str_encrypt(clientrequest, uuid)
    sqlString = "insert into Log values(?,?,?,?,?,?);"
    dao.save('/var/log/mwlog.db', sqlString, (buffer(enreq), uuid, "unfinished", t, userid, ""))

##major process	
#start daemon
daemon = mwDaemon.Daemon('/tmp/daemon.pid')
daemon.start() 

# List to keep track of socket descriptors
global server_socket
CONNECTION_LIST = []

#hash map for record socket and user
global soc_uuid_dict
soc_uuid_dict = {}

#start socket     
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("127.0.0.1", PORT))
server_socket.listen(10)

# Add server socket to the list of readable connections
CONNECTION_LIST.append(server_socket)

# start thread: 6 handle thread + 1 return thread
if (threading.activeCount()<7):
    #6 thread start
    for i in range(6):     
        mwhandlethread = Mwhandlethread()    
        mwhandlethread.start()

#recovery
sql_connection = sqlite3.connect('/var/log/mwlog.db',isolation_level=None)
##create table: request uuid state(notreturn,unfinished,finished) time userid result
sql_connection.execute('''create table if not exists Log(request text not null, uuid char[33] not null,state char[20] not null,time char[20] not null,userid varchar[100] not null,result text not null);''')
##select request,uuid when state is unfinished

class RecoveryThread(threading.Thread):
    def Recovery(self,userid,t):
        sql_conn = sqlite3.connect('/var/log/mwlog.db', isolation_level=None)
        result = sql_conn.execute("select request from Log where state = 'unfinished' and userid='" + userid + "' and time<'" + t + "';")
        for row in result:
            data = row[0]
            data = data.replace("#","'",2)  #' can not insert into db
            #print "Pre_Handle: ",data
            handle(data)
        result=sql_conn.execute("select result,uuid from Log where state = 'not return' and userid='" + userid + "' and time<'" + t + "';")
        for row in result:
            data = row[0]
            uuid = row[1]
            sock = soc_uuid_dict.get(userid)
            if sock == None:
                continue
            try:
                sock.sendall(data)
            except:
                soc_uuid_dict[userid]=None
                continue
            while (1):
                try:
                    sql_conn.execute("update Log set state='finished' where uuid='" + uuid + "';")
                except:
                    time.sleep(0.01)
                    continue
                break
            Remove(uuid)
            t_mon = '%.4f' %(time.time() - 2600000)
        while (1):
            try:
                sql_conn.execute("delete from Log where time<'" + t_mon + "';")
            except:
                time.sleep(0.01)
                continue
            break	       
        print "recovery finished"
        #recovery finished
    def run(self):
        #print "recovery started."
        while True:
            if mwrecoveryqueue.qsize() < 1:
                continue
            userid,t = mwrecoveryqueue.get()
            self.Recovery(userid,t)
#print "server started on port " + str(PORT)
data = ''
recovery = RecoveryThread()
recovery.start()

def handle_WebRequest(sock, request):
    global FromFirefox 
    FromFirefox	= True
    headers = firefoxHelper.parse_headers(request)
    token = firefoxHelper.generate_token(headers['Sec-WebSocket-Key'])
    sock.send('\
HTTP/1.1 101 WebSocket Protocol Hybi-10\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Accept: %s\r\n\r\n' % token)
    data = sock.recv(RECV_BUFFER)
    clientrequest = firefoxHelper.parse_data(data)
    save_request(clientrequest)
    userid = getUserId(clientrequest)
    if (soc_uuid_dict.get("fx_"+userid) == None):
        soc_uuid_dict["fx_"+userid] = sock
    #put rq into mwhandlequeue
    handle(clientrequest)
    '''
    while True:
        data = sock.recv(RECV_BUFFER)
	clientrequest = firefoxHelper.parse_data(data)
	save_request(clientrequest)
	userid = getUserId(clientrequest)
        if (soc_uuid_dict.get(userid) == None):
            soc_uuid_dict[userid] = sock
        #put rq into mwhandlequeue
	print("********clientrequest == " + clientrequest)
	handle(clientrequest)
    '''

while 1:
    # Get the list sockets which are ready to be read through select
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],CONNECTION_LIST)
    for sock in error_sockets:
	CONNECTION_LIST.remove(sock)
	del soc_uuid_dict[userid]
	sock.close()

    for sock in read_sockets:
    #New connection
        if sock == server_socket:
        # Handle the case in which there is a new connection recieved through server_socket
            sockfd, addr = server_socket.accept()
            CONNECTION_LIST.append(sockfd)
	# Handle the case in which there is a new connection from the client 
        else:
            #data=''
            try:
                recvdata = sock.recv(RECV_BUFFER)
		# handle request comes from websocket
		if(recvdata.find("websocket")!=-1 or (recvdata.find("-k")==-1 and recvdata!="")):
		    if(recvdata.find("websocket")!=-1):
		    	clientrequest = handle_WebRequest(sock, recvdata)
		    else:
			FromFirefox = True
		        clientrequest = firefoxHelper.parse_data(recvdata)
			#print("fx clientrequest====" + clientrequest)
		        save_request(clientrequest)
		        userid = getUserId(clientrequest)
		        if (soc_uuid_dict.get("fx_"+userid) == None):
		            soc_uuid_dict["fx_"+userid] = sock
		        #put rq into mwhandlequeue
	 	        handle(clientrequest)
                elif recvdata:
    	    	    FromFirefox = False
		    clientrequest = handle_revData(recvdata)
		    token = userUtil.mwGetTokenByReq(clientrequest)
		    userid = getUserId(clientrequest)
		    if(token):
			#ckeck whether the token is expired
   		        if(userUtil.mwCheckToken(token)==False):
			    newToken = userUtil.mwRefreshToken(userid)
			    clientrequest = clientrequest.replace(token, newToken)
		    else:
			#it is login request if the request does not contain token
			userUtil.mwSaveUserInfo(clientrequest)
		    save_request(clientrequest)
		    if (soc_uuid_dict.get(userid) == None):
			soc_uuid_dict[userid] = sock
                    handle(clientrequest)
		#interpret empty result as closed connection
                else:
		    #print("req null......")
		    userid = getUserId(clientrequest)
		    del soc_uuid_dict[userid]
		    if("" in soc_uuid_dict.keys()):
		    	del soc_uuid_dict[""]
		    CONNECTION_LIST.remove(sock)
		    sock.close()
            except Exception,e:
		print Exception,":",e
                sock.close()
                CONNECTION_LIST.remove(sock)
                continue

server_socket.close()
sql_connection.close()
