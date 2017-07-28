var connected = false;

init();

function init(){

	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		chrome.tabs.sendMessage(tabs[0].id, {"getStatus": "getStatus"});
	});

	chrome.runtime.onMessage.addListener(handle_result);

	document.getElementById("main").style.display = "none";
	document.getElementById("p1").style.display = "none";
	document.getElementById("p2").style.display = "none";
	do_select("block", "none", "<h>container_name:</h>", "");
}

function handle_result(message){
	if(message.uploadFile){
		document.getElementById("txtContent").innerHTML = message.uploadFile;
	}else if(message.loginstatus){
	    document.getElementById("login").style.display = "none";
	    document.getElementById("main").style.display = "block";
	    //document.getElementById("params").style.display = "none";
	    document.getElementById("p1").style.display = "none";
	    document.getElementById("p2").style.display = "none";
	    do_select("block", "none", "<h>container_name:</h>", "");
	    document.getElementById("username").innerHTML = "welcome " + message.username + "!";
	    connected = true;
	}else{
	    document.getElementById("login").style.display = "none";
	    document.getElementById("main").style.display = "block";
	    document.getElementById("username").innerHTML = "welcome " + message.username + "!";
	    display_result(message.JResult);
	    connected = true;
	}
}

function display_result(JResult){
	resultString = "*************"+"\r\n";
	for(var key in JResult){
	    resultString = resultString + key + ": " +  JResult[key] + "\r\n";
	}
	document.getElementById("txtContent").innerHTML = resultString;
}

function do_select(param1display, param2display, param1Text, param2Text){
	document.getElementById("p1").style.display = param1display;
	document.getElementById("p2").style.display = param2display;
	document.getElementById("p1Name").innerHTML = param1Text;
	document.getElementById("p2Name").innerHTML = param2Text;
	document.getElementById("p1Value").value = "";
	document.getElementById("p2Value").value = "";
}

/*chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    	// get any previously set cookie for the current tab
	    chrome.cookies.get({
	      url: tabs[0].url,
	      name: "access_token"
	    }, function(cookie) {
	      if(cookie) {
	      	  document.getElementById("loginStatus").style.display = "none";
	      	  document.getElementById("btnSend").disabled = false;
	      	  connected = true;
	      }else{
	      	  document.getElementById("welcome").style.display = "none";
	      	  document.getElementById("btnSend").disabled = true;
	      }
	    });
});*/
document.getElementById("reqSelect").addEventListener("change", function(e) {
	document.getElementById("params").style.display = "block";
	document.getElementById("txtContent").innerHTML = "";
	var myselect = document.getElementById("reqSelect");
	var request = myselect.options[myselect.selectedIndex].value;
	switch(request){
	//case "get container":
	//	do_select("none", "none", "", "");
	//    break;
	case "create container":
		do_select("block", "none", "<h>container_name:</h>", "");
	    break;
	case "create directory":
		do_select("block", "none", "<h>directory_path:</h>", "");
	    break;
	case "get quota":
		do_select("none", "none", "", "");
	    break;
	case "clear recycler":
		do_select("none", "none", "", "");
	    break;
	case "set quota": 
		do_select("block", "none", "<h>quota_value:</h>", "");
	    break;
	case "delete container":
		do_select("block", "none", "<h>container_name:</h>", "");
	    break;
	case "delete directory":
		do_select("block", "none", "<h>directory_path:</h>", "");
	    break;
	case "delete file":
		do_select("block", "none", "<h>file_path:</h>", "");
	    break;
	case "upload file":
		do_select("block", "none", "<h>dst_path:</h>", "");
	    break;
	case "rename directory":
		do_select("block", "block", "<h>src_path:</h>", "<h>dst_path:</h>");
	    break;
	case "rename file":	
		do_select("block", "block", "<h>src_path:</h>", "<h>dst_path:</h>");
		break; 
	default:
		document.getElementById("p1").style.display = "none";
		document.getElementById("p2").style.display = "none";
	    document.getElementById("txtContent").innerHTML = "Wrong Request";
    }

});

document.getElementById("btnConnect").addEventListener("click", function(e) {
	
  	var email = document.getElementById("email").value;
  	var pwd = document.getElementById("pwd").value;

  	console.log("executeScript!");
	chrome.tabs.executeScript(null, {
		file: "/content_scripts/content_connect.js"
	});

	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		chrome.tabs.sendMessage(tabs[0].id, {"email": email, "pwd": pwd, "connected": connected});
	});
});

document.getElementById("btnSend").addEventListener("click", function(e) {
	if(connected){
		var myselect = document.getElementById("reqSelect");
		var request = myselect.options[myselect.selectedIndex].value;
		var params = JSON.parse('{"no_param": "no params"}');
		switch(request){
		//case "get container":
		//    break;
		case "create container":
			var container_name = document.getElementById("p1Value").value;
			if(container_name===""){
				document.getElementById("txtContent").innerHTML = "Please input container_name";
				return;
			}
			params = JSON.parse('{"container_name": "' + container_name + '"}');
		    break;
		case "create directory":
			var directory_path = document.getElementById("p1Value").value;
			if(directory_path===""){
				document.getElementById("txtContent").innerHTML = "Please input directory_path";
				return;
			}
			params = JSON.parse('{"directory_path": "' + directory_path + '"}'); 
		    break;
		case "get quota":
		    break;
		case "clear recycler":
		    break;
		case "set quota":
			var quota_value = document.getElementById("p1Value").value;
			if(quota_value===""){
				document.getElementById("txtContent").innerHTML = "Please input quota_value";
				return;
			}
			params = JSON.parse('{"quota_value": "' + quota_value + '"}'); 
		    break;
		case "delete container":
			var container_name_delete = document.getElementById("p1Value").value;
			if(container_name_delete===""){
				document.getElementById("txtContent").innerHTML = "Please input container_name";
				return;
			}
			params = JSON.parse('{"container_name": "' + container_name_delete + '"}'); 
		    break;
		case "delete directory":
			var directory_path_delete = document.getElementById("p1Value").value;
			if(directory_path_delete===""){
				document.getElementById("txtContent").innerHTML = "Please input directory_path";
				return;
			}
			params = JSON.parse('{"directory_path": "' + directory_path_delete + '", "cover": "true"}');  
		    break;
		case "delete file":
			var file_path_delete = document.getElementById("p1Value").value;
			if(file_path_delete===""){
				document.getElementById("txtContent").innerHTML = "Please input file_path";
				return;
			}
			params = JSON.parse('{"file_path": "' + file_path_delete + '", "cover": "true"}');   
		    break;
		case "upload file":
		    	var upload_dst_path = document.getElementById("p1Value").value;
			if(upload_dst_path===""){
				document.getElementById("txtContent").innerHTML = "Please input dst_path";
				return;
			}
			params = JSON.parse('{"dst_path": "' + upload_dst_path + '", "cover": "true"}');
		    break;
		case "rename directory":
			var src_path_directory = document.getElementById("p1Value").value;
			var dst_path_directory= document.getElementById("p2Value").value; 
			if(src_path_directory===""){
				document.getElementById("txtContent").innerHTML = "Please input src_path";
				return;
			}else if(dst_path_directory===""){
				document.getElementById("txtContent").innerHTML = "Please input dst_path";
				return;
			}
			params = JSON.parse('{"src_path": "'+ src_path_directory +'", "dst_path": "' + dst_path_directory + '"}'); 
		    break;
		case "rename file":	
			var src_path_file = document.getElementById("p1Value").value;
			var dst_path_file= document.getElementById("p2Value").value; 
			if(src_path_file===""){
				document.getElementById("txtContent").innerHTML = "Please input src_path";
				return;
			}else if(dst_path_file===""){
				document.getElementById("txtContent").innerHTML = "Please input dst_path";
				return;
			}
			params = JSON.parse('{"src_path": "'+ src_path_file +'", "dst_path": "' + dst_path_file + '"}'); 
			break; 
		default:
		    document.getElementById("txtContent").innerHTML = "Wrong Request";
	    }

		chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
			chrome.tabs.sendMessage(tabs[0].id, {"request": request, "params": params,"connected": connected});
		});

	}else{

	}
});
