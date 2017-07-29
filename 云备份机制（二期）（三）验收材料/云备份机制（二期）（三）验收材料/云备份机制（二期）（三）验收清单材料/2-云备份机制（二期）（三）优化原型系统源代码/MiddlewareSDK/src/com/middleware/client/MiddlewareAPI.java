/** Copyright (c) 2016 The FDU Security Team 
 * by 15212010038@fudan.edu.cn 
 */

package com.middleware.client;

import java.util.Date;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import com.middleware.socket.MiddlewareSocket;
import com.middleware.utils.Constant;
import com.middleware.utils.Constant.MODE;

import net.sf.json.JSONObject;

public class MiddlewareAPI implements IMiddlewareAPI{	
	private String userid;
	private String access_token;
	private ExecutorService exec; 
	
	public MiddlewareAPI(String userID, String pwd) {
		start();
		this.access_token = this.getAccessToken(userID, pwd);
		this.userid = userID;
	}
	
	public void setAccess_token(String access_token) {
		this.access_token = access_token;
	}

	public String getAccess_token() {
		return access_token;
	}
	
	public String getUserid() {
		return userid;
	}

	public void setUserid(String userid) {
		this.userid = userid;
	}

	private String sendRequest(String request){
		String result = "";
		MiddlewareSocket middlewareSocket = new MiddlewareSocket(request);
		Future<String> mwFuture= exec.submit(middlewareSocket);
		try {
			result = mwFuture.get();
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (ExecutionException e) {
			e.printStackTrace();
		}
		return result;
	}
	
	public void start(){
		exec = Executors.newCachedThreadPool();
	}
	
	public void stop(){
		exec.shutdown();
	}
	
	public String setUerIDAndToken(String request){
		String userid = getUserid().replace("@", "").replace(".", "");
		return request.replace("AUTH_", "AUTH_" + userid).replace("X-Auth-Token:", "X-Auth-Token:" + getAccess_token());
	}
	
	public String formatRequest(String request){
		request = "userid = " + getUserid() + "\n" + "time = " + new Date().getTime() + "\n" + "request = " + request + "\r\n";
		return request;
	}

	@Override
	public String getAccessToken(String userID, String pwd) {
		String token = null;
		String request = Constant.GET_ACCESS_TOKEN.replace("#email#", userID).replace("#password#", pwd);
		request = formatRequest(request);
		String result = this.sendRequest(request).replace("mwresult = ", "");
		JSONObject jsonObject = JSONObject.fromObject(result);
		token = (String) jsonObject.get("access_token");
		return token;
	}

	@Override
	public String getContainer() {
		String request = Constant.GET_CONTAINER;
		request = setUerIDAndToken(request);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String createContainer(String containerName) {
		String request = Constant.CREATE_CONTAINER;
		request = setUerIDAndToken(request);
		request = request.replace("#container_name#", containerName);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String createDirectory(String directoryPath) {
		String request = Constant.CREATE_DIRECTORY;
		request = setUerIDAndToken(request);
		request = request.replace("#directory_path#", directoryPath);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String craeteSymlink(String srcPath, String dstPath) {
		String request = Constant.CREATE_SYMLINK;
		request = setUerIDAndToken(request);
		request = request.replace("#src_path#", srcPath).replace("#dst_path#", dstPath);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String getRecycler(long start, long limit) {
		String request = Constant.GET_RECYCLER;
		request = setUerIDAndToken(request);
		request = request.replace("#[start: <LONG>]#", String.valueOf(start)).replace("#[limit: <LONG>]#", String.valueOf(limit));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String getFileList(String directoryPath, boolean recursive) {
		String request = Constant.GET_FILE_LIST;
		request = setUerIDAndToken(request);
		request = request.replace("#directory_path#", directoryPath).replace("#[recursive: <true|false>]#", String.valueOf(recursive));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String getFileHistory(String filePath) {
		String request = Constant.GET_FILE_HISTORY;
		request = setUerIDAndToken(request);
		request = request.replace("#file_path#", filePath);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String getFileAttribute(String filePath, String version) {
		String request = Constant.GET_FILE_ATTRIBUTE;
		request = setUerIDAndToken(request);
		request = request.replace("#file_path#", filePath).replace("#[version : LATEST|specified_version]#", version);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String getOpHistory(int recent) {
		String request = Constant.GET_OP_HISTORY;
		request = setUerIDAndToken(request);
		request = request.replace("#[recent: <INT>]#", String.valueOf(recent));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String getHistoryContainer(String containerName) {
		String request = Constant.GET_HISTORY_CONTAINER;
		request = setUerIDAndToken(request);
		request = request.replace("#container_name#", containerName);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String getOpTask(String taskID) {
		String request = Constant.GET_OP_TASK;
		request = setUerIDAndToken(request);
		request = request.replace("#[task_id: <task_id>]#", taskID);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String getQuota() {
		String request = Constant.GET_QUOTA;
		request = setUerIDAndToken(request);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String clearRecycler() {
		String request = Constant.CLEAR_RECYCLER;
		request = setUerIDAndToken(request);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String setQuota(long quotaValue) {
		String request = Constant.SET_QUOTA;
		request = setUerIDAndToken(request);
		request = request.replace("#quota_value#", String.valueOf(quotaValue));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String setPermission(String path, long permision) {
		String request = Constant.SET_PERMISSON;
		request = setUerIDAndToken(request);
		request = request.replace("#path#", path).replace("#[permission: <OCTAL>]#", String.valueOf(permision));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String setHistoryContainer(String containerName) {
		String request = Constant.SET_HISTORY_CONTAINER;
		request = setUerIDAndToken(request);
		request = request.replace("#container_name#", containerName);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String deleteContainer(String containerName) {
		String request = Constant.DELETE_CONTAINER;
		request = setUerIDAndToken(request);
		request = request.replace("#container_name#", containerName);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String deleteDirectory(String directoryPath, boolean cover) {
		String request = Constant.DELETE_DIRECTORY;
		request = setUerIDAndToken(request);
		request = request.replace("#directory_path#", directoryPath).replace("#[cover: <true|false>]#", String.valueOf(cover));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String deleteFile(String filePath, boolean cover) {
		String request = Constant.DELETE_FILE;
		request = setUerIDAndToken(request);
		request = request.replace("#file_path#", filePath).replace("#[cover: <true|false>]#", String.valueOf(cover));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String deleteOpHistory(int recent) {
		String request = Constant.DELETE_OP_HISTORY;
		request = setUerIDAndToken(request);
		request = request.replace("#[recent: <INT>]#", String.valueOf(recent));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String uploadFile(String srcPath, String dstPath, boolean overwrite, String metadata, MODE mode) {
		String request = Constant.UPLOAD_FILE;
		request = setUerIDAndToken(request);
		request = request.replace("#src_path#", srcPath).replace("#dst_path#", dstPath).replace("#[overwrite: <true|false>]#", String.valueOf(overwrite));
		request = request.replace("#[metadata: <STRING>]#", metadata).replace("#[mode: <NORMAL|ENCRYPT|COMPRESS|ENCRYPT_COMPRESS>]#", String.valueOf(mode));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String downloadFile(String srcPath, long offset, long length, String version, MODE mode, String dstPath) {
		String request = Constant.DOWNLOAD_FILE;
		request = setUerIDAndToken(request);
		request = request.replace("#src_path#", srcPath).replace("#[offset: <LONG>]#", String.valueOf(offset)).replace("#[length: <LONG>]#", String.valueOf(length));
		request = request.replace("#[version: <LATEST|specified_version>]#", version).replace("#[mode: <NORMAL|ENCRYPT|COMPRESS|ENCRYPT_COMPRESS>]#", String.valueOf(mode));
		request = request.replace("#dst_path#", dstPath);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String moveDirectory(String srcPath, String dstPath) {
		String request = Constant.MOVE_DIRECTORY;
		request = setUerIDAndToken(request);
		request = request.replace("#src_path#", srcPath).replace("#dst_path#", dstPath);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String moveFile(String srcPath, String dstPath) {
		String request = Constant.MOVE_FILE;
		request = setUerIDAndToken(request);
		request = request.replace("#src_path#", srcPath).replace("#dst_path#", dstPath);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String copyDirectory(String srcPath, String dstPath, boolean async) {
		String request = Constant.COPY_DIRECTORY;
		request = setUerIDAndToken(request);
		request = request.replace("#src_path#", srcPath).replace("#dst_path#", dstPath).replace("#[async: <true|false>]#", String.valueOf(async));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String copyFile(String srcPath, String dstPath, boolean async) {
		String request = Constant.COPY_FILE;
		request = setUerIDAndToken(request);
		request = request.replace("#src_path#", srcPath).replace("#dst_path#", dstPath).replace("#[async: <true|false>]#", String.valueOf(async));
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String renameDirectory(String srcPath, String dstPath) {
		String request = Constant.RENAME_DIRECTORY;
		request = setUerIDAndToken(request);
		request = request.replace("#src_path#", srcPath).replace("#dst_path#", dstPath);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String renameFile(String srcPath, String dstPath) {
		String request = Constant.RENAME_FILE;
		request = setUerIDAndToken(request);
		request = request.replace("#src_path#", srcPath).replace("#dst_path#", dstPath);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String recoverDirectory(String uuid, String path) {
		String request = Constant.RECOVER_DIRECTORY;
		request = setUerIDAndToken(request);
		request = request.replace("#uuid#", uuid).replace("#path#", path);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}

	@Override
	public String recoverFile(String uuid, String path) {
		String request = Constant.RECOVER_FILE;
		request = setUerIDAndToken(request);
		request = request.replace("#uuid#", uuid).replace("#path#", path);
		request = formatRequest(request);
		String result = sendRequest(request).replace("mwresult = ", "");
		return result;
	}
}
