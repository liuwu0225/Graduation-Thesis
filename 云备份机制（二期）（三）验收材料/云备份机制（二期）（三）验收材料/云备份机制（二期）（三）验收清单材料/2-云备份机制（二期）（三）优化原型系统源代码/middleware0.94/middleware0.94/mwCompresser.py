import zipfile 
import os

class Compresser():
 
    def compress_file(self,filename,tofilename):
        if (not os.path.exists(filename)):
            return "compress error: No such file."
        try:
            os.chdir(os.path.dirname(filename))
            (filenames,filename)=os.path.split(filename)
            f = zipfile.ZipFile(tofilename,'w',zipfile.ZIP_DEFLATED) 
            f.write(filename) 
            f.close()
            return "compress success."
        except:
            return "compress error."

    def decompress_file(self,filename,tofilename):
        if (not os.path.exists(filename)):
            return "decompress error: No such file."
        try:
            zfile = zipfile.ZipFile(filename,'r')
            for filename in zfile.namelist():
                data = zfile.read(filename)
                file = open(tofilename, 'w+b')
                file.write(data)
                file.close()
                return "decompress success."
        except:
            pass
            return "decompress error."

if __name__ == '__main__':
    compresser = Compresser()
    compresser.compress_file('/home/liangjiao/mytest/version1.txt','/home/liangjiao/mytest/version111.zip')
    compresser.decompress_file('/home/liangjiao/mytest/version111.zip','/home/liangjiao/mytest/version00.txt')
    print 'ok'
