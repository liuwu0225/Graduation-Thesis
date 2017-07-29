/** Copyright (c) 2016 The FDU Security Team 
 * @author 15212010038@fudan.edu.cn 
 */

package com.middleware.utils;

public class Constant {
	public static final String SERVER_IP = "192.168.7.62";
	public static final String VERSION = "1.0";
	public static final String DESCRIPTION = "Middleware SDK for java";
	public static final String SERVER_URL = "https://192.168.7.62:443/v1/AUTH_";
	public static final String SOCKET_HOST = "127.0.0.1";
	public static final int SOCKET_PORT = 10000;
	
	public static enum MODE{
		NORNAL, ENCRYPT, COMPRESS, ENCRYPT_COMPRESS
	}
	
	public static final String GET_ACCESS_TOKEN = "-k -X POST -d '{\"email\":\"#email#\", \"password\": \"#password#\"}' https://" + SERVER_IP + ":443/oauth/access_token";
	public static final String GET_CONTAINER = "-k -s " + SERVER_URL + " -X GET -H \"X-Auth-Token:\"";
	public static final String CREATE_CONTAINER = "-k -s " + SERVER_URL + "/#container_name# -X PUT -H \"X-Auth-Token:\"";
	public static final String CREATE_DIRECTORY = "-k -X PUT \"" + SERVER_URL + "#directory_path#?op=MKDIRS\" -H \"X-Auth-Token:\"";
	public static final String CREATE_SYMLINK = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=CREATESYMLINK&destination=#dst_path#\" -H \"X-Auth-Token:\"";
	public static final String GET_RECYCLER = "-k \"" + SERVER_URL + "/recycle/user?op=GETRECYCLER&start=#[start: <LONG>]#&limit=#[limit: <LONG>]#\" -H \"X-Auth-Token:\"";
	public static final String GET_FILE_LIST = "-k \"" + SERVER_URL + "#directory_path#?op=LISTDIR&recursive=#[recursive: <true|false>]#&ftype=d\" -H \"X-Auth-Token:\"";
	public static final String GET_FILE_HISTORY = "-k -L \"" + SERVER_URL + "#file_path#?op=GETHISTORY\" -H \"X-Auth-Token:\"";
	public static final String GET_FILE_ATTRIBUTE = "-k \"" + SERVER_URL + "#file_path#?op=GETFILEATTR&version=#[version : LATEST|specified_version]#\" -H \"X-Auth-Token:\"";
	public static final String GET_OP_HISTORY = "-k -L \"" + SERVER_URL + "?op=GET_OP_HISTORY&recent=#[recent: <INT>]#\" -H \"X-Auth-Token:\"";
	public static final String GET_HISTORY_CONTAINER = "-k -X HEAD " + SERVER_URL + "/#container_name# -H \"X-Auth-Token:\"";
	public static final String GET_OP_TASK = "-k -X GET \"" + SERVER_URL + "?op=GET_OP_TASK&tx_id=#[task_id: <task_id>]#\" -H \"X-Auth-Token:\"";
	public static final String GET_QUOTA = "-k -X GET \"" + SERVER_URL + "/quota?op=info\" -H \"X-Auth-Token:\"";
	public static final String CLEAR_RECYCLER = "-k -X POST \"" + SERVER_URL + "/clearrecycle?op=RECYCLER\" -H \"X-Auth-Token:\"";
	public static final String SET_QUOTA = "-k -X POST \"" + SERVER_URL + "/quota?op=createstorage\" -H \"X-Auth-Token:\" -H \"X-Account-Meta-Quota-Bytes:#quota_value#\"";
	public static final String SET_PERMISSON = "-k -X PUT \"" + SERVER_URL + "#path#?op=SETPERMISSION&permission=#[permission: <OCTAL>]#\" -H \"X-Auth-Token:\"";
	public static final String SET_HISTORY_CONTAINER = "-k -X POST " + SERVER_URL + "/#container_name# -H \"X-Auth-Token:\" -H \"X-Versions-Location:#container_name#_versions\"";
	public static final String DELETE_CONTAINER = "-k -s " + SERVER_URL + "/#container_name# -X DELETE -H \"X-Auth-Token:\"";
	public static final String DELETE_DIRECTORY = "-k -X DELETE \"" + SERVER_URL + "#directory_path#?op=DELETE&ftype=d&cover=#[cover: <true|false>]#\" -H \"X-Auth-Token:\"";
	public static final String DELETE_FILE = "-k -X DELETE \"" + SERVER_URL + "#file_path#?op=DELETE&ftype=f&cover=#[cover: <true|false>]#\" -H \"X-Auth-Token:\"";
	public static final String DELETE_OP_HISTORY = "-k -L \"" + SERVER_URL + "?op=DELETE_HISTORY&recent=#[recent: <INT>]#\" -H \"X-Auth-Token:\"";
	public static final String UPLOAD_FILE = "-k -X PUT -T #src_path# \"" + SERVER_URL + "#dst_path#?op=CREATE&overwrite=#[overwrite: <true|false>]#&metadata=#[metadata: <STRING>]#&mode=#[mode: <NORMAL|ENCRYPT|COMPRESS|ENCRYPT_COMPRESS>]#\" -H \"X-Auth-Token:\"";
	public static final String DOWNLOAD_FILE = "-k -L \"" + SERVER_URL + "#src_path#?op=OPEN&offset=#[offset: <LONG>]#&length=#[length: <LONG>]#&version=#[version: <LATEST|specified_version>]#&mode=#[mode: <NORMAL|ENCRYPT|COMPRESS|ENCRYPT_COMPRESS>]#\" -H \"X-Auth-Token:\" -o #dst_path#";
	public static final String MOVE_DIRECTORY = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=MOVE&ftype=d\" -H \"X-Auth-Token:\" -H \"Destination:#dst_path#\"";
	public static final String MOVE_FILE = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=MOVE&ftype=f\" -H \"X-Auth-Token:\" -H \"Destination:#dst_path#\"";
	public static final String COPY_DIRECTORY = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=COPY&ftype=d&async=#[async: <true|false>]#\" -H \"X-Auth-Token:\" -H \"Destination:#dst_path#\"";
	public static final String COPY_FILE = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=COPY&ftype=f&async=#[async: <true|false>]#\" -H \"X-Auth-Token:\" -H \"Destination:#dst_path#\"";
	public static final String RENAME_DIRECTORY = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=RENAME&destination=#dst_path#&ftype=d\" -H \"X-Auth-Token:\"";
	public static final String RENAME_FILE = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=RENAME&destination=#dst_path#&ftype=f\" -H \"X-Auth-Token:\"";
	public static final String RECOVER_DIRECTORY = "-k -X POST -d '{\"list\":[{\"uuid\":\"#uuid#\",\"path\":\"#path#\",\"ftype\":\"d\"}]}' \"" + SERVER_URL + "/batch?op=MOVERECYCLE\" -H \"X-Auth-Token:\"";
	public static final String RECOVER_FILE = "-k -X POST -d '{\"list\":[{\"uuid\":\"#uuid#\",\"path\":\"#path#\",\"ftype\":\"f\"}]}' \"" + SERVER_URL + "/batch?op=MOVERECYCLE\" -H \"X-Auth-Token:\"";
}
