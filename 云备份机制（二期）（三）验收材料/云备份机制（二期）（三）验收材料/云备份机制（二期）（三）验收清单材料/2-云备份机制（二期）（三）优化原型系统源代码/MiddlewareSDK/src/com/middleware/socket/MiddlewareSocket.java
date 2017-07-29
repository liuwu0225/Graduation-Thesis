package com.middleware.socket;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Iterator;
import java.util.concurrent.Callable;

import com.middleware.utils.Constant;

public class MiddlewareSocket implements Callable<String>{
	
	private Socket mwSocket;
	private String request;
	
	public MiddlewareSocket(String request) {
		this.request =request;
	}

	@Override
	public String call() {
		String result = "";
		try {
			mwSocket = new Socket(Constant.SOCKET_HOST, Constant.SOCKET_PORT);
			PrintWriter mwWriter = new PrintWriter(mwSocket.getOutputStream());
			mwWriter.write(this.request);
			mwWriter.flush();
			
			InputStream mwInputStream=mwSocket.getInputStream();
	        BufferedReader mwBufferedReader = new BufferedReader(new InputStreamReader(mwInputStream));
	        //skip uuid and get mwresult
	        String info=mwBufferedReader.readLine();
	        if(info!=null)
	        	result = mwBufferedReader.readLine();
			mwWriter.close();
	        mwInputStream.close();
	        mwBufferedReader.close();
	        mwSocket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
        return result;
	}
}
