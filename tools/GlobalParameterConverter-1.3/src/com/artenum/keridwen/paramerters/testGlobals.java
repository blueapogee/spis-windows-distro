package com.artenum.keridwen.paramerters;

import java.io.File;
import java.util.ArrayList;
import java.util.Iterator;

import com.thoughtworks.xstream.XStream;

public class testGlobals {

	/**
	 * @param args
	 */
	public static void main(String[] args) {

		ArrayList<GlobalParameter> globalParamList = new ArrayList<GlobalParameter>();
		
		GlobalParameter floatParam = new GlobalParameter("theFloatParam", "pre-proc", 3.124259f, "[m.s-1]", "A first example");
		globalParamList.add(floatParam);
		
		GlobalParameter doubleParam = new GlobalParameter("theDoubleParam", "pre-proc", -1.2345, "[kg]", "A second example");
		globalParamList.add(doubleParam);
		
		GlobalParameter intParam = new GlobalParameter("theIntParam", "pre-proc", 1789, "[y]", "A third example");
		globalParamList.add(intParam);
		
	    Iterator<GlobalParameter> iter = globalParamList.iterator();
		while(iter.hasNext()){
			GlobalParameter  param = iter.next();
			System.out.println(param.getKeyName() + " " + param.getCategory() + " " + param.getValue() + " " + param.getUnit() + " " + param.getDescription());
		}
		
		GlobalParamXMLWriter writer = new GlobalParamXMLWriter(globalParamList);
		writer.setFile(new File("/Users/juju/globalParam.xml"));
		writer.write();
		
		GlobalParamXMLReader reader = new GlobalParamXMLReader(new File("/Users/juju/globalParam.xml"));
		
		ArrayList<GlobalParameter> reloadedGlobalParamList = reader.read();
		
		System.out.println("=========================");
	     iter = reloadedGlobalParamList.iterator();
			while(iter.hasNext()){
				GlobalParameter  param = iter.next();
				System.out.println(param.getKeyName() + " " + param.getCategory() + " " + param.getTypeAString() + " "+ param.getValue() + " " + param.getUnit() + " " + param.getDescription());
			}
		
		System.out.println("End");
	}

}
