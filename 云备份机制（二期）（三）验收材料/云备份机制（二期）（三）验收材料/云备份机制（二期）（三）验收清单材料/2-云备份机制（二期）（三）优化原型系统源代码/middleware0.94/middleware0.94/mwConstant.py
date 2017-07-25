#this file save the request constants

#CHUNKSIZE defines the size of the file chunk, 800 for test and 4M for practical.
__CHUNKSIZE__ = 800
#__CHUNKSIZE__ = 4194304
#CACHESIZE defines the size of the cache
__CACHESIZE__ = 9999999
#CACHEPATH defines the path of cache path
__CACHEPATH__ = "/home/herh/lw/cache"

#the following constants represent requests
__LOGIN__ = 'curl -k -X POST -d \'{"email":"#email#", "password": "#password#"}\' https://192.168.7.62:443/oauth/access_token'
__VERIFY_TOKEN__ = '''curl -k -i -X POST "https://192.168.7.62:443/v1/verify_token" -H "X-Auth-Token:#token#" --cacert /root/task/api/ssl/ssl_dir/ca.crt'''
__COPY__ = '''curl -k -X PUT "https://192.168.7.62:443/v1/AUTH_#userid##src_path#?op=COPY&ftype=f&async=true" -H "X-Auth-Token:#token#" -H "Destination:#des_path#"'''
__RENAME__ = '''curl -k -X PUT "https://192.168.7.62:443/v1/AUTH_#userid##src_name#?op=RENAME&destination=#des_name#&ftype=f" -H "X-Auth-Token:#token#"'''
__JOIN__ = '''curl -k -i -X PUT -d '[#file_attr#]' "https://192.168.7.62:443/v1/AUTH_#userid##path#?multipart-manifest=put&overwrite=false" -H "X-Auth-Token:#token#" -H "X-Static-Large-Object: true"'''
__DELETE__ = '''curl -k -X DELETE "https://192.168.7.62:443/v1/AUTH_#userid##file_path#?op=DELETE&ftype=f&cover=true" -H "X-Auth-Token:#token#"'''
__SEGMENT__ = '''curl -k -i -X PUT -T "https://192.168.7.62:443/v1/AUTH_#userid#/segments#path#?op=CREATE&overwrite=true&metadata=\{"
natrue":"split file"\}&mode=" -H "X-Auth-Token: #token#"'''
#database path
__MWLOG__ = '/var/log/mwlog.db'
__MWCACHE__ = '/var/log/mwcache.db'
