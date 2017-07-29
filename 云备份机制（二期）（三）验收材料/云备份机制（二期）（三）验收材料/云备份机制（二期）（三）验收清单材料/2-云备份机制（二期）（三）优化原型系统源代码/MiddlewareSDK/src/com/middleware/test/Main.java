package com.middleware.test;

import com.middleware.client.MiddlewareAPI;
import com.middleware.utils.Constant.MODE;

import net.sf.json.JSONObject;

public class Main {
	public static void main(String[] args) {
		JSONObject jsonObject;
		String result;
		MiddlewareAPI middlewareAPI = new MiddlewareAPI("kaeyika@163.com", "123456");
		try {
			//clearRecycler
			Thread.sleep(500);
			result = middlewareAPI.clearRecycler();
			jsonObject = JSONObject.fromObject(result);
			System.out.println("clearRecycler:" + jsonObject.get("status"));
			//getContainer
			Thread.sleep(500);
			result = middlewareAPI.getContainer();
			jsonObject = JSONObject.fromObject(result);
			System.out.println("getContainer:" + jsonObject.get("status"));
			//createContainer
			Thread.sleep(500);
			result = middlewareAPI.createContainer("newNormal");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("createContainer:" + jsonObject.get("status"));
			//createDirectory
			Thread.sleep(500);
			result = middlewareAPI.createDirectory("/normal/mydirectory");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("createDirectory:" + jsonObject.get("status"));
			/*//craeteSymlink
			Thread.sleep(500);
			result = middlewareAPI.craeteSymlink("/home/herh/test.docx", "/normal/test.docx");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("craeteSymlink:" + jsonObject.get("status"));*/
			//getRecycler
			Thread.sleep(500);
			result = middlewareAPI.getRecycler(0, 5);
			jsonObject = JSONObject.fromObject(result);
			System.out.println("getRecycler:" + jsonObject.get("status"));
			//getFileList
			Thread.sleep(500);
			result = middlewareAPI.getFileList("/normal", true);
			jsonObject = JSONObject.fromObject(result);
			System.out.println("getFileList:" + jsonObject.get("status"));
			//getFileHistory
			Thread.sleep(500);
			result = middlewareAPI.getFileHistory("/normal/test_cache.docx");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("getFileHistory:" + jsonObject.get("status"));
			//getFileAttribute
			Thread.sleep(500);
			result = middlewareAPI.getFileAttribute("/normal/test_cache.docx", "LATEST");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("getFileAttribute:" + jsonObject.get("status"));
			//getOpHistory
			Thread.sleep(500);
			result = middlewareAPI.getOpHistory(5);
			jsonObject = JSONObject.fromObject(result);
			System.out.println("getOpHistory:" + jsonObject.get("status"));
			/*//getHistoryContainer
			Thread.sleep(500);
			result = middlewareAPI.getHistoryContainer("normal");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("getHistoryContainer:" + jsonObject.get("status"));
			//getOpTask(need test again)
			Thread.sleep(500);
			result = middlewareAPI.getOpTask("656565");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("getOpTask:" + jsonObject.get("status"));*/
			//getQuota
			Thread.sleep(500);
			result = middlewareAPI.getQuota();
			jsonObject = JSONObject.fromObject(result);
			System.out.println("getQuota:" + jsonObject.get("status"));
			//setQuota
			Thread.sleep(500);
			result = middlewareAPI.setQuota(99999999);
			jsonObject = JSONObject.fromObject(result);
			System.out.println("setQuota:" + jsonObject.get("status"));
			/*//setPermission
			Thread.sleep(500);
			result = middlewareAPI.setPermission("/cache", 0777777);
			jsonObject = JSONObject.fromObject(result);
			System.out.println("setPermission:" + jsonObject.get("status"));
			//setHistoryContainer
			Thread.sleep(500);
			result = middlewareAPI.setHistoryContainer("normal");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("setHistoryContainer:" + jsonObject.get("status"));*/
			//deleteContainer
			Thread.sleep(500);
			result = middlewareAPI.deleteContainer("newNormal");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("deleteContainer:" + jsonObject.get("status"));
			//deleteDirectory
			Thread.sleep(500);
			result = middlewareAPI.deleteDirectory("/normal/mydirectory", true);
			jsonObject = JSONObject.fromObject(result);
			System.out.println("deleteDirectory:" + jsonObject.get("status"));
			//deleteFile
			Thread.sleep(500);
			result = middlewareAPI.deleteFile("/normal/test_cache.docx", true);
			jsonObject = JSONObject.fromObject(result);
			System.out.println("deleteFile:" + jsonObject.get("status"));
			//uploadFile
			Thread.sleep(500);
			result = middlewareAPI.uploadFile("/home/herh/test.docx", "/javatest/test.docx", true, "", MODE.NORNAL);
			jsonObject = JSONObject.fromObject(result);
			System.out.println("uploadFile:" + jsonObject.get("status"));
			//downloadFile
			Thread.sleep(500);
			result = middlewareAPI.downloadFile("/javatest/test.docx", 0, 9999999, "LATEST", MODE.NORNAL, "/home/herh/javatest.docx");
			//jsonObject = JSONObject.fromObject(result);
			System.out.println("downloadFile:" + result);
			//moveDirectory
			Thread.sleep(500);
			result = middlewareAPI.moveDirectory("/mid/moved", "/normal/moved");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("moveDirectory:" + jsonObject.get("status"));
			//moveFile
			Thread.sleep(500);
			result = middlewareAPI.moveFile("/mid/server.crt", "/normal/server.crt");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("moveFile:" + jsonObject.get("status"));
			//copyDirectory
			Thread.sleep(500);
			result = middlewareAPI.copyDirectory("/normal/moved", "/mid/moved", true);
			jsonObject = JSONObject.fromObject(result);
			System.out.println("copyDirectory:" + jsonObject.get("status"));
			//copyFile
			Thread.sleep(500);
			result = middlewareAPI.copyFile("/mid/server.key", "/normal/server.key", true);
			jsonObject = JSONObject.fromObject(result);
			System.out.println("copyFile:" + jsonObject.get("status"));
			//renameDirectory
			Thread.sleep(500);
			result = middlewareAPI.renameDirectory("/mid/rename", "/mid/rn");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("renameDirectory:" + jsonObject.get("status"));
			//renameFile
			Thread.sleep(500);
			result = middlewareAPI.renameFile("/normal/server.crt", "/normal/rnserver.crt");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("renameFile:" + jsonObject.get("status"));
			/*//recoverDirectory
			Thread.sleep(500);
			result = middlewareAPI.recoverDirectory("142152124522", "/mid/rn");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("recoverDirectory:" + jsonObject.get("status"));
			//recoverFile
			Thread.sleep(500);
			result = middlewareAPI.recoverFile("142152124522", "/cache/test.docx");
			jsonObject = JSONObject.fromObject(result);
			System.out.println("recoverFile:" + jsonObject.get("status"));*/
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
	}
}
