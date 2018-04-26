package com.artenum.keridwen.paramerters;

public class GlobalParameter {
	
	private String keyName;
	private String category;
	private String typeAString;
	
	private Object valueAsObject = null;
	private float valueAsFloat;
	private double valueAsDouble; 
	private int valueAsInt;
	private String valueAsString;
	
	private String unit;
	
	private String description;
	
	final static public String OBJECT = "Object";
	final static public String FLOAT = "float";
	final static public String DOUBLE = "double";
	final static public String INT = "int";
    final static public String STRING = "String";
	
	public GlobalParameter(){
		
	}
	
	public GlobalParameter( String keyName, String category, Object value, String unit, String description){
	
		this.valueAsObject = value;
		this.typeAString = OBJECT;
		setMeta(keyName, category, unit, description);
	}
	
	public GlobalParameter( String keyName, String category, float value, String unit, String description){
		this.valueAsObject = null;
		this.valueAsFloat = value;
		this.typeAString = FLOAT;
		setMeta(keyName, category, unit, description);
	}
	
	public GlobalParameter( String keyName, String category, int value, String unit, String description){
		this.valueAsObject = null;
		this.valueAsInt = value;
		this.typeAString = INT;
		setMeta(keyName, category, unit, description);
	}
	
	public GlobalParameter( String keyName, String category, double value, String unit, String description){
		this.valueAsObject = null;
		this.valueAsDouble = value;
		this.typeAString = DOUBLE;
		setMeta(keyName, category, unit, description);
	}
	
	public GlobalParameter( String keyName, String category, String value, String unit, String description){
		this.valueAsObject = null;
		this.valueAsString = value;
		this.typeAString = STRING;
		setMeta(keyName, category, unit, description);
	}
	
	public Object getValue(){
				
		if (this.typeAString.equals(OBJECT)){
			return(this.valueAsObject);
		} else if (this.typeAString.equals(FLOAT)){
			return( new Float(this.valueAsFloat));
		} else if (this.typeAString.equals(DOUBLE)){
			return( new Float(this.valueAsDouble));
		} else if (this.typeAString.equals(INT)){
			return( Integer.valueOf(this.valueAsInt));
		} else if (this.typeAString.equals(STRING)){
			return( new Float(this.valueAsString));
		} else {
			return null;
		}	
	}
	
	
	private void setMeta(String keyName, String category, String unit, String description){
		this.keyName = keyName;
		this.category = category;
		this.unit = unit;
		this.description = description;
	}

	public String getKeyName() {
		return keyName;
	}

	public void setKeyName(String keyName) {
		this.keyName = keyName;
	}

	public String getCategory() {
		return category;
	}

	public void setCategory(String category) {
		this.category = category;
	}

	public String getUnit() {
		return unit;
	}

	public void setUnit(String unit) {
		this.unit = unit;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public String getTypeAString() {
		return typeAString;
	}

	public void setTypeAString(String typeAString) {
		this.typeAString = typeAString;
	}

	public Object getValueAsObject() {
		return(getValue());
	}

	public void setValueAsObject(Object valueAsObject) {
		this.setTypeAString(OBJECT);
		this.valueAsObject = valueAsObject;
	}

	public float getValueAsFloat() {
		return valueAsFloat;
	}

	public void setValueAsFloat(float valueAsFloat) {
		this.setTypeAString(FLOAT);
		this.valueAsFloat = valueAsFloat;
	}

	public double getValueAsDouble() {
		return valueAsDouble;
	}

	public void setValueAsDouble(double valueAsDouble) {
		this.setTypeAString(DOUBLE);
		this.valueAsDouble = valueAsDouble;
	}

	public int getValueAsInt() {
		return valueAsInt;
	}

	public void setValueAsInt(int valueAsInt) {
		this.setTypeAString(INT);
		this.valueAsInt = valueAsInt;
	}

	public String getValueAsString() {
		return valueAsString;
	}

	public void setValueAsString(String valueAsString) {
		this.setTypeAString(STRING);
		this.valueAsString = valueAsString;
	}
}
