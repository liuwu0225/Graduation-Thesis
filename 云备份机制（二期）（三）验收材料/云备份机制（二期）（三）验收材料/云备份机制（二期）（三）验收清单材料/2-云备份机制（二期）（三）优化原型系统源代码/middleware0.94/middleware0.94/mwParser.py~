class Parser():
    request = ''
    def __init__(self,r):
        self.request = r

    ###parse:
    def parse(self):
        #parse the request
        ##default  compress_encrypt_upload
        ##default  download_decrypt_decompress
        if(self.request.find('op=CREATE&') != -1):    #create file
            if(self.request.find('mode=ENCRYPT_COMPRESS') != -1):    #compress and encrypt the file
                return 'COMPRESSENCRYPTUPLOAD'
            elif(self.request.find('mode=ENCRYPT') != -1):    #encrypt the file
                return 'ENCRYPTUPLOAD'
            elif(self.request.find('mode=COMPRESS') != -1):    #compress the file
                return 'COMPRESSUPLOAD'
            else:
                return 'UPLOAD'

        elif(self.request.find('op=OPEN&') != -1):    #download file
            if(self.request.find('mode=ENCRYPT_COMPRESS') != -1):    #decompress and decrypt the file
                return 'DECRYPTDECOMPRESSDOWNLOAD'
            elif(self.request.find('mode=ENCRYPT') != -1):    #decrypt the file
                return 'DECRYPTDOWNLOAD'
            elif(self.request.find('mode=COMPRESS') != -1):    #decrypt the file
                return 'DECOMPRESSDOWNLOAD'
            else:
                return 'DOWNLOAD'

	elif(self.request.find('op=GET_REQUEST&') != -1):
	    return 'GETREQUEST'

	elif(self.request.find('op=WITHDRAW_REQUEST&') != -1):
	    return 'WITHDRAWREQUEST'

        else:
            return 'OTHERS'
        ##end

	
