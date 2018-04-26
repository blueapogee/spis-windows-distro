package com.artenum.keridwen.paramerters;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;

import com.thoughtworks.xstream.XStream;

public class GlobalParamXMLWriter {
	
	private File outputFile = null;
	private XStream xtream; 
	private ArrayList<GlobalParameter> globalParamList;

	public GlobalParamXMLWriter(ArrayList<GlobalParameter> globalParamList){

	    xtream = new XStream();
		this.globalParamList = globalParamList;
	}

	public void setFile(File file){
		this.outputFile = file;
	}
	
	public String serialize(ArrayList<GlobalParameter> globalParamList){
         return( xtream.toXML(globalParamList));	      	
	}
	
	public void write(){
		if (outputFile != null){
			try {
				FileWriter outFile = new FileWriter(outputFile.getAbsolutePath());
				PrintWriter out = new PrintWriter(outFile);
				out.println(serialize(globalParamList));
				out.flush();
			}catch (Exception e) {
				// TODO: handle exception
			}
		}
	}
}
