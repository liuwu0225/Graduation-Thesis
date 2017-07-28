chrome.runtime.onMessage.addListener(connect_socket);

var socket;

var csPort;

function handle_upload(params){ 
    chrome.runtime.sendMessage({"uploadFile": "Please pick source file and right click to upload, only IMG/TXT/DOC allowed"});   
    var menu = document.getElementById("menu");
    var aMenuLi=menu.children;
    document.oncontextmenu = function(ev){  
        var oEvent=ev || event;
        menu.style.display='block';
        menu.style.left=oEvent.clientX+'px';
        menu.style.top=oEvent.clientY+'px';
              
        aMenuLi[0].onclick=function (){
	    var src_path = oEvent.target.src;
            if(oEvent.target.nodeName=="IMG"){
		if(src_path.indexOf("file://")>-1){
		    src_path = src_path.replace("file://", "");
		}
                if(window.confirm("确定要上传吗?")){
                    var mparams = JSON.parse('{"src_path": "' + src_path + '", "dst_path": "' + params.dst_path + '"}');
                    csPort.postMessage({"request": "upload file", "params": mparams});
                }else{
                    //return false;
                }  
            }else{
              alert("Wrong Type");
            }             
        };

        aMenuLi[0].onmouseover=function (){
            this.style.backgroundColor = "#91c9f7";             
        };

        aMenuLi[0].onmouseout=function (){
            this.style.backgroundColor = "#F5F5F5";             
        };
        return false;
  };
  document.onclick=function (){
      menu.style.display='none';
  };
}

function reset(){
    document.oncontextmenu = function(ev){
        return true;
    };
}

function insertMenuHTML(){
    var div = document.createElement("div");
    div.innerHTML = '<ul id="menu" style="width:150px; border:0.8px solid #A9A9A9; border-radius: 2px; position:absolute; left:0; top:0; display:none; background:#F5F5F5;"><li>上传到云备份服务器</li></ul>';
    document.body.appendChild(div);
}

function connect_socket(message) {
  if(message.getStatus){
      console.log("content script getStatus!");
      csPort.postMessage({"getStatus": message.getStatus});
  }

  else if(!message.connected){
      console.log("content script unconnected!");
      //insert menuHTML
      insertMenuHTML();
      csPort = chrome.runtime.connect({name:"port-from-cs"});
      csPort.onMessage.addListener(function(m) {
          if(m.sendLoginStatus){
              chrome.runtime.sendMessage({"loginstatus": m.loginstatus, "username": m.username});
          }else{
              if(m.JResult.msg == "upload success!"){
                  alert("上传成功！");
                  reset();
              }else{
                  chrome.runtime.sendMessage({"JResult": m.JResult, "username": m.username});
              }    
      	  }
      });

      var email = message.email;
      var pwd = message.pwd;
      csPort.postMessage({"email": email, "pwd": pwd});
  }else{
      console.log("content script connected!");
      var request = message.request;
      var params = message.params;
      if(request == "upload file"){
          handle_upload(params);
      }else{
          csPort.postMessage({"request": request, "params": params});
      }   
  }
}
