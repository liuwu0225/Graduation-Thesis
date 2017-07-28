//chrome.runtime.onMessage.addListener(connect);
chrome.runtime.onConnect.addListener(handleConnection);

var portFromCS;

var socket;

var login = false;
var userid = "";
var access_token = "";
var timestamp = "";

function set_userid_token(request){
	request = request.replace("AUTH_", "AUTH_" + userid).replace("X-Auth-Token:", "X-Auth-Token:" + access_token);
	return request;
}

function format_request(request){
    request = "userid = " + userid + "\n" + "time = " + new Date().getTime() + "\n" + "request = " + request + "\r\n";
    return request;
}

function set_user_info(JResult){
    userid = JResult.tanent;
    access_token = JResult.access_token;
}

function parse_request(request, params){
    var parseRequest = "";
    switch(request){
	//case "get container":
	//    parseRequest = GET_CONTAINER;
	//    break;
	case "create container":
	    parseRequest = CREATE_CONTAINER.replace("#container_name#", params.container_name);
	    break;
	case "create directory":
	    parseRequest = CREATE_DIRECTORY.replace("#directory_path#", params.directory_path); 
	    break;
	case "get quota":
	    parseRequest = GET_QUOTA;
	    break;
	case "clear recycler":
	    parseRequest = CLEAR_RECYCLER;
	    break;
	case "set quota":
	    parseRequest = SET_QUOTA.replace("#quota_value#", params.quota_value);
	    break;
	case "delete container":
	    parseRequest = DELETE_CONTAINER.replace("#container_name#", params.container_name); 
	    break;
	case "delete directory":
	    parseRequest = DELETE_DIRECTORY.replace("#directory_path#", params.directory_path).replace("#[cover: <true|false>]#", params.cover);
	    break;
	case "delete file":
	    parseRequest = DELETE_FILE.replace("#file_path#", params.file_path).replace("#[cover: <true|false>]#", params.cover);
	    break;
	case "upload file":
	    parseRequest = UPLOAD_FILE.replace("#src_path#", params.src_path).replace("#dst_path#", params.dst_path).replace("#[overwrite: <true|false>]#", "true").replace("#[metadata: <STRING>]#", "").replace("#[mode: <NORMAL|ENCRYPT|COMPRESS|ENCRYPT_COMPRESS>]#", ""); 
	    break;
	case "rename directory": 
	    parseRequest = RENAME_DIRECTORY.replace("#src_path#", params.src_path).replace("#dst_path#", params.dst_path);
	    break;
	case "rename file":
	    parseRequest = RENAME_FILE.replace("#src_path#", params.src_path).replace("#dst_path#", params.dst_path);
	    break;
	default:
	    return "wrong request"; 
    }
    return parseRequest;
}

function handleConnection(p) {
    portFromCS = p;
    var JResult;
    portFromCS.onMessage.addListener(function(m) {
        if(m.getStatus){
            portFromCS.postMessage({"loginstatus": login, "sendLoginStatus": "sendLoginStatus", "username": userid});
        }else if(login){
	    var parseRequest = parse_request(m.request, m.params);
	    if(parseRequest == "wrong request"){
		JResult = JSON.parse('{"wrong_request": "wrong_request", "tanent": "kaeyika163com"}');
		portFromCS.postMessage({"JResult": JResult, "username": JResult.tanent});
	    }else{
	    	parseRequest = set_userid_token(parseRequest);
		parseRequest = format_request(parseRequest);
	    	console.log(parseRequest);
	    	send(parseRequest);
	    }
        }else{
            connect(m);
        }
    });
}

function connect(message) {
    console.log("doLogin");
    if(login){
    	return;
    } 
    /*var JResult = JSON.parse('{"msg": "0"}');
    portFromCS.postMessage({"JResult": JResult, "username": "kaeyika163com"});
    login = true;*/
    var host = "ws://127.0.0.1:10000/"
    socket = new WebSocket(host);
    try {
        socket.onopen = function (msg) {
            //get access token while connect to the server at the first time
            request = GET_ACCESS_TOKEN.replace("#email#", message.email).replace("#password#", message.pwd);
	    request = format_request(request);
            send(request);
            login = true;
            //storeToken("HJJKSdosdklsdkOLSkoas12");
        };
	
	pyresult = ""
        socket.onmessage = function (msg) {
	    pyresult = pyresult + msg.data
	    if(msg.data.charAt(msg.data.length-1)=="#"){
	    //if the result contains tag "#", it means this is the last response from the server and handle it.
	        pyresult = pyresult.substring(0,pyresult.length-1);
		var JResult = JSON.parse(pyresult);
		portFromCS.postMessage({"JResult": JResult, "username": userid});
		//reset pyresult for next request
		pyresult="";
		if(JResult.tanent){
		    set_user_info(JResult)
		}
	    }
        };

        socket.onclose = function (msg) {
	    portFromCS.postMessage({"mstatus": "connection closed"});
	    login = false;	
	};
    }
    catch (ex) {
        log(ex);
    }
}

function send(request){
    socket.send(request);
}

function storeToken(token){
    console.log("set cookie ");
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        console.log("url = " + tabs[0].url);
        chrome.cookies.set({
          url: tabs[0].url,
          //url: "www.baidu.com",
          name: "access_token",
          value: "dasdkasdkjaskdjaskldjaskd"
        });
    });
}

var SERVER_IP = "192.168.7.62";
var VERSION = "1.0";
var DESCRIPTION = "Middleware SDK for firefox";
var SERVER_URL = "https://192.168.7.62:443/v1/AUTH_";

var GET_ACCESS_TOKEN = "-k -X POST -d '{\"email\":\"#email#\", \"password\": \"#password#\"}' https://" + SERVER_IP + ":443/oauth/access_token";
var GET_CONTAINER = "-k -s " + SERVER_URL + " -X GET -H \"X-Auth-Token:\"";
var CREATE_CONTAINER = "-k -s " + SERVER_URL + "/#container_name# -X PUT -H \"X-Auth-Token:\"";
var CREATE_DIRECTORY = "-k -X PUT \"" + SERVER_URL + "#directory_path#?op=MKDIRS\" -H \"X-Auth-Token:\"";
var CREATE_SYMLINK = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=CREATESYMLINK&destination=#dst_path#\" -H \"X-Auth-Token:\"";
var GET_RECYCLER = "-k \"" + SERVER_URL + "/recycle/user?op=GETRECYCLER&start=#[start: <LONG>]#&limit=#[limit: <LONG>]#\" -H \"X-Auth-Token:\"";
var GET_FILE_LIST = "-k \"" + SERVER_URL + "#directory_path#?op=LISTDIR&recursive=#[recursive: <true|false>]#&ftype=d\" -H \"X-Auth-Token:\"";
var GET_FILE_HISTORY = "-k -L \"" + SERVER_URL + "#file_path#?op=GETHISTORY\" -H \"X-Auth-Token:\"";
var GET_FILE_ATTRIBUTE = "-k \"" + SERVER_URL + "#file_path#?op=GETFILEATTR&version=#[version : LATEST|specified_version]#\" -H \"X-Auth-Token:\"";
var GET_OP_HISTORY = "-k -L \"" + SERVER_URL + "?op=GET_OP_HISTORY&recent=#[recent: <INT>]#\" -H \"X-Auth-Token:\"";
var GET_HISTORY_CONTAINER = "-k -X HEAD " + SERVER_URL + "/#container_name# -H \"X-Auth-Token:\"";
var GET_OP_TASK = "-k -X GET \"" + SERVER_URL + "?op=GET_OP_TASK&tx_id=#[task_id: <task_id>]#\" -H \"X-Auth-Token:\"";
var GET_QUOTA = "-k -X GET \"" + SERVER_URL + "/quota?op=info\" -H \"X-Auth-Token:\"";
var CLEAR_RECYCLER = "-k -X POST \"" + SERVER_URL + "/clearrecycle?op=RECYCLER\" -H \"X-Auth-Token:\"";
var SET_QUOTA = "-k -X POST \"" + SERVER_URL + "/quota?op=createstorage\" -H \"X-Auth-Token:\" -H \"X-Account-Meta-Quota-Bytes:#quota_value#\"";
var SET_PERMISSON = "-k -X PUT \"" + SERVER_URL + "#path#?op=SETPERMISSION&permission=#[permission: <OCTAL>]#\" -H \"X-Auth-Token:\"";
var SET_HISTORY_CONTAINER = "-k -X POST " + SERVER_URL + "/#container_name# -H \"X-Auth-Token:\" -H \"X-Versions-Location:#container_name#_versions\"";
var DELETE_CONTAINER = "-k -s " + SERVER_URL + "/#container_name# -X DELETE -H \"X-Auth-Token:\"";
var DELETE_DIRECTORY = "-k -X DELETE \"" + SERVER_URL + "#directory_path#?op=DELETE&ftype=d&cover=#[cover: <true|false>]#\" -H \"X-Auth-Token:\"";
var DELETE_FILE = "-k -X DELETE \"" + SERVER_URL + "#file_path#?op=DELETE&ftype=f&cover=#[cover: <true|false>]#\" -H \"X-Auth-Token:\"";
var DELETE_OP_HISTORY = "-k -L \"" + SERVER_URL + "?op=DELETE_HISTORY&recent=#[recent: <INT>]#\" -H \"X-Auth-Token:\"";
var UPLOAD_FILE = "-k -X PUT -T #src_path# \"" + SERVER_URL + "#dst_path#?op=CREATE&overwrite=#[overwrite: <true|false>]#&metadata=#[metadata: <STRING>]#&mode=#[mode: <NORMAL|ENCRYPT|COMPRESS|ENCRYPT_COMPRESS>]#\" -H \"X-Auth-Token:\"";
var DOWNLOAD_FILE = "-k -L \"" + SERVER_URL + "#src_path#?op=OPEN&offset=#[offset: <LONG>]#&length=#[length: <LONG>]#&version=#[version: <LATEST|specified_version>]#&mode=#[mode: <NORMAL|ENCRYPT|COMPRESS|ENCRYPT_COMPRESS>]#\" -H \"X-Auth-Token:\" -o #dst_path#";
var MOVE_DIRECTORY = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=MOVE&ftype=d\" -H \"X-Auth-Token:\" -H \"Destination:#dst_path#\"";
var MOVE_FILE = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=MOVE&ftype=f\" -H \"X-Auth-Token:\" -H \"Destination:#dst_path#\"";
var COPY_DIRECTORY = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=COPY&ftype=d&async=#[async: <true|false>]#\" -H \"X-Auth-Token:\" -H \"Destination:#dst_path#\"";
var COPY_FILE = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=COPY&ftype=f&async=#[async: <true|false>]#\" -H \"X-Auth-Token:\" -H \"Destination:#dst_path#\"";
var RENAME_DIRECTORY = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=RENAME&destination=#dst_path#&ftype=d\" -H \"X-Auth-Token:\"";
var RENAME_FILE = "-k -X PUT \"" + SERVER_URL + "#src_path#?op=RENAME&destination=#dst_path#&ftype=f\" -H \"X-Auth-Token:\"";
var RECOVER_DIRECTORY = "-k -X POST -d '{\"list\":[{\"uuid\":\"#uuid#\",\"path\":\"#path#\",\"ftype\":\"d\"}]}' \"" + SERVER_URL + "/batch?op=MOVERECYCLE\" -H \"X-Auth-Token:\"";
var RECOVER_FILE = "-k -X POST -d '{\"list\":[{\"uuid\":\"#uuid#\",\"path\":\"#path#\",\"ftype\":\"f\"}]}' \"" + SERVER_URL + "/batch?op=MOVERECYCLE\" -H \"X-Auth-Token:\"";
