import sys
import socket
import hashlib
import time

userid = 'kaeyika163com'
time = '%.4f' %time.time()
#token
#request =  '-k -X POST -d \'{"password": "123456", "email":"kaeyika@163.com"}\' https://192.168.7.62:443/oauth/access_token'

#get container
request = '-k -s https://192.168.7.62:443/v1/AUTH_kaeyika163com -X GET -H "X-Auth-Token:OrdtlnLagFUOVSpIJSKOxtCUkEh7EptGh59vLeUv"'

#normal
#request = '-k -X GET "https://localhost:443/v1/AUTH_kaeyika163com?op=GET_OP_TASK&tx_id=tx8877afff801a4c75aee4aba454b76fa6" -H "X-Auth-Token:  jZNLlcC7mlupK2vBikw90IhenY903hmgvgprgoKP"'



#download
#request = '-k -L "https://192.168.7.62:443/v1/AUTH_kaeyika163com/normal/jsontest.py?op=OPEN&mode=NORMAL" -H "X-Auth-Token: h83UwNB6YiWVn3lVOrUM3fW1fPptahwZNBkGWnep" -o /home/herh/mwtest/jsontest1.py'

#upload
#request = '-k -X PUT -T /home/herh/mwtest/json test.py "https://192.168.7.62:443/v1/AUTH_kaeyika163com/normal/jsontest.py?op=CREATE&overwrite=true&mode=NORMAL" -H "X-Auth-Token:  h83UwNB6YiWVn3lVOrUM3fW1fPptahwZNBkGWnep"'


#get request
clientrequest = 'userid = ' + userid + '\n' + 'time = ' + time + '\n' + 'request = ' + request + '\r\n'

s=socket.socket()
s.connect(('127.0.0.1',10000))
s.sendall(clientrequest)
data = ''

while(1):
    recdata=s.recv(500)
    if recdata:
        data = data + recdata
        #to sign the end of result,\r\n is in the end  
        dataend = data.find('\r\n')
    
        if(dataend != -1):
            mwdata = data[:dataend+2]
            data = data.replace(mwdata,'')
            print 'client recv msg:'
            print mwdata
            break


s.close()
    
