package com.artenum.keridwen.paramerters;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;

import com.thoughtworks.xstream.XStream;
import com.thoughtworks.xstream.io.xml.StaxDriver;

public class GlobalParamXMLReader {

	private File fileIn = null;
	private XStream xstream;
	
	public GlobalParamXMLReader(File file){
	
		this.fileIn = file;
		
		xstream = new XStream(new StaxDriver());
	}
	
	public ArrayList<GlobalParameter> read(){
		String tmpLine = "";
		String input = ""; 
		ArrayList<GlobalParameter> globaParamList = null;
	  

		InputStream ist = null;
		try {
			ist = new FileInputStream(fileIn);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		BufferedReader istream = new BufferedReader(new InputStreamReader(ist));
		try {
			while( (tmpLine = istream.readLine()) != null){
				input = input + tmpLine;
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		//System.out.println("THE XML Stuff: " + input);
		
		return( (ArrayList<GlobalParameter>) this.xstream.fromXML(input));		
	}
	
}
