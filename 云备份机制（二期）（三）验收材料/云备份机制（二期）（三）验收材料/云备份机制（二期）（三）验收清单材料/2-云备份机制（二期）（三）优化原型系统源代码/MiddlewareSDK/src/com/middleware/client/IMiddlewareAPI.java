package com.middleware.client;

import com.middleware.utils.Constant.MODE;

public interface IMiddlewareAPI {
	String getAccessToken(String userID, String pwd);
	String getContainer();
	String createContainer(String containerName);
	String createDirectory(String directoryPath);
	String craeteSymlink(String srcPath, String dstPath);
	String getRecycler(long start, long limit);
	String getFileList(String directoryPath, boolean recursive);
	String getFileHistory(String filePath);
	String getFileAttribute(String filePath, String version);
	String getOpHistory(int recent);
	String getHistoryContainer(String containerName);
	String getOpTask(String taskID);
	String getQuota();
	String clearRecycler();
	String setQuota(long quotaValue);
	/**
	 * @param permission OCTAL
	 * */
	String setPermission(String path, long permision);
	String setHistoryContainer(String containerName);
	String deleteContainer(String containerName);
	String deleteDirectory(String directoryPath, boolean cover);
	String deleteFile(String filePath, boolean cover);
	String deleteOpHistory(int recent);
	String uploadFile(String srcPath, String dstPath, boolean overwrite, String metadata, MODE mode);
	String downloadFile(String srcPath, long offset, long length, String version, MODE mode, String dstPath);
	String moveDirectory(String srcPath, String dstPath);
	String moveFile(String srcPath, String dstPath);
	String copyDirectory(String srcPath, String dstPath, boolean async);
	String copyFile(String srcPath, String dstPath, boolean async);
	String renameDirectory(String srcPath, String dstPath);
	String renameFile(String srcPath, String dstPath);
	String recoverDirectory(String uuid, String path);
	String recoverFile(String uuid, String path);
}
