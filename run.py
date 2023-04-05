import pandas as pd
import re 
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
# df = pd.read_csv("edw_sql_analysis - run5.csv")



def extractSchemaTable(text):
    pattern = r"schema:\s*(\w+)\s+and\s+table\s+name:\s*(\w+)"
    match = re.search(pattern, text)
    if match: 
        return "Schema : " + match.group(1) + " Table : " + match.group(2)
    else :
        return "No match found."
    
class Summary :
    def __init__(self,df):
        self.df = df
        
    def get_metadata_completed(self):
        return (self.df["metadata_build_status"] == "completed").sum()
    
    def get_metadata_failed(self):
        return (self.df["metadata_build_status"] == "failed").sum()
    
    def get_parse_completed(self):
        return (self.df["parse_status"] == "Success").sum()
    
    def get_parse_failed(self):
        return (self.df["parse_status"] == "Failed").sum()
        
    def get_import_completed(self):
        return (self.df["import_status"] == "Success").sum()
    
    def get_import_failed(self):
        return (self.df["import_status"] == "Failed").sum()
    
    def buildSummary(self):
        st.write("Total number of SQL's : ", len(df))
        st.write("Total build completed :" , self.get_metadata_completed())
        st.write("Total build failed : ", self.get_metadata_failed()) 
        st.write("Parser complete : " , self.get_parse_completed()) 
        st.write("Parser Failed : " ,self.get_parse_failed())
        st.write("SQL Import complete : " ,self.get_import_completed()) 
        st.write("SQL Import Failed : ", self.get_import_failed())
        
    def keyword_error(self):
    	text_input = st.text_input("Search Error")
    	if text_input :
    		dff = df[df["error "] != None]
    		dff.fillna("NA",inplace=True)
    		errors = dff[dff["error "].str.contains(text_input,case=False)]
    		st.write(errors)
			
		
        	 
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
	df = pd.read_csv(uploaded_file)
	st.title("Run report")
	st.write(df)
	summary = Summary(df)
	summary.buildSummary()
	
	if st.button("Get All parser error"):
		parser_error = df[df["parse_status"]=="Failed"]
		st.write(parser_error)
	if st.button("Get All SQL Import error"):
		import_error = df[df["import_status"]=="Failed"]
		st.write(import_error)
	if st.button("Get All Metadata build error"):
		metadata_error = df[df["metadata_build_status"]=="failed"]
		st.write(metadata_error)
	summary.keyword_error()



