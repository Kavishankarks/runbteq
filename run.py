import pandas as pd
import re 
import streamlit as st
import numpy as np
# df = pd.read_csv("edw_sql_analysis - run5.csv")


# st.title("Analyzing BTEQ Run: A Comprehensive Evaluation of Results ")

st.set_page_config(
    page_title="IWX BTEQ Run Analysis",
    page_icon="https://aks-qa-540.infoworks.technology/assets/IWX_transp.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Tool to analyse the BTEQ Run report "
    }
)

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
        if text_input and st.button("Submit") :     
            dff = df[df["error"] != None]
            errors = dff[dff["error"].str.contains(text_input,case=False)]
            st.write(errors)

    def search_target_table(self):
        unique_tables = {}
        for i in df["target_table"]:
            if i  not in unique_tables and type(i) == str:
                unique_tables[i] = 1
        selected_table = st.selectbox("Select table",unique_tables.keys())
        if st.button("Search table"):
            dff = df[df["target_table"] != None]
            
            target_table = dff[dff["target_table"].str.contains(selected_table,case=False)]
            metadata, parser , sqlimport = self.get_individual_table(target_table)
            st.write(target_table)
            st.write("\t\tMetadata Error",metadata)
            st.write("\t\tParser Error",parser)
            st.write("\t\tSQL Import Error",sqlimport)



    def extractSchemaTable(self,text):
        if(type(text) != str or "Cant" not in text) :
            return None
        pattern = r"schema:\s*(\w+)\s+and\s+table\s+name:\s*(\w+)"
        match = re.search(pattern, text)
        if match: 
            return "Schema : " + match.group(1) + " Table : " + match.group(2)
        else :
            return None

    def get_table_not_found(self):
        errors = df[df["import_status"]=="Failed"]
        tables_count = 0
        for i in errors["error"]:
            res = self.extractSchemaTable(i)
            if(res):
                tables_count += 1
                st.write(res)
        st.write("Total table count : ",tables_count)

    def get_individual_table(self, target_table):
        return (target_table["metadata_build_status"] == "failed").sum() , (target_table["parse_status"] == "Failed").sum(), (target_table["import_status"] == "Failed").sum()

    def get_table_completed(self,list_error):
        unique_tables = {}
        for i in df["target_table"]:
            if i  not in unique_tables and type(i) == str:
                unique_tables[i] = 1
        dff = df[df["target_table"] != None]
        dff.fillna("NA",inplace=True)
        fully_completed =0 
        cnt = 1
        for i in unique_tables.keys():
            target_table = dff[dff["target_table"] == i]
            metadata, parser , sqlimport = self.get_individual_table(target_table)
            if (metadata ==0 and parser ==0 and sqlimport ==0):
                st.write(str(cnt) + ". Table Name : " + i + " Total SQL's :  " + str(len(target_table))  + " Completed ✅ " )
                fully_completed += 1
            else :
                st.write(str(cnt) + ". Table Name : " + i )
                col1, col2, col3, col4, col5 = st.columns(5)
                col2.metric("Total SQL's ",len(target_table))
                col3.metric("Metadata Error",metadata)
                col4.metric("Parser Error",parser)
                col5.metric("SQL Import Error",sqlimport)
                if list_error:
                    st.write(target_table)
            cnt += 1
        st.subheader("Fully completed : " + str(fully_completed) + " out of : " + str(cnt))

    def get_jcl_completed(self,list_error):
        # compare_with_last = st.selectbox("Compare with last",("Yes","No"))
        # if compare_with_last == "Yes" :
        #     upload_last_file = st.file_uploader("Chosse last run report")
        #     last_run_df= pd.read_csv(upload_last_file)
        #     st.write(last_run_df)
        # else :
        unique_jcls = {}
        for i in df["jcl"]:
            if i  not in unique_jcls and type(i) == str:
                unique_jcls[i] = 1
        st.write(unique_jcls.keys())
        st.write(len(unique_jcls))
        dff = df[df["jcl"] != None]
        dff.fillna("NA",inplace=True)
        fully_completed =0 
        cnt = 1
        for i in unique_jcls.keys():
            target_jcl = dff[dff["jcl"] == i]
            metadata, parser , sqlimport = self.get_individual_table(target_jcl)
            if (metadata ==0 and parser ==0 and sqlimport ==0):
                st.subheader(str(cnt) + ". Table Name : " + i  + " Completed ✅ " )
                cola1, cola2 = st.columns(2)
                cola1.metric(" Total SQL's :  " , str(len(target_jcl)) )
                fully_completed += 1
            else :
                total_failed = metadata + parser + sqlimport
                st.subheader(str(cnt) + ". JCL : " + i )
                col1, col2, col3, col4, col5 = st.columns(5)
                col2.metric("Total SQL's ",len(target_jcl))
                col3.metric("Metadata Error",metadata)
                col4.metric("Parser Error",parser)
                col5.metric("SQL Import Error",sqlimport)
                if list_error:
                    st.write(target_jcl)
            cnt += 1
        st.subheader("Fully completed : " + str(fully_completed) + " out of : " + str(cnt))
    
    def error_display(self):
        tab1, tab2, tab3 = st.tabs(["SQL Import error", "Parser error", "Metadata build error"])
        
        with tab1 :
            parser_error = df[df["import_status"]=="Failed"]
            st.write(parser_error)
        with tab2 :
            import_error = df[df["parse_status"]=="Failed"]
            st.write(import_error)
        with tab3:
            metadata_error = df[df["metadata_build_status"]=="failed"]
            st.write(metadata_error)
   
class preProcessData :
    def __init__(self,df) -> None:
        self.actual_columns  = ['jcl', 'control_card', 'sql_liness', 'sql_number', 'query_type',
       'parse_status', 'table_mode', 'target_table', 'dependent_tables',
       'pipelineid', 'import_status', 'metadata_build',
       'metadata_build_status', 'error']
        self.actual_columns_next = [ 'file_name', 'sql_liness', 'sql_number', 'query_type',
       'parse_status', 'table_mode', 'target_table', 'dependent_tables',
       'pipelineid', 'import_status', 'metadata_build',
       'metadata_build_status', 'error'
        ]
        self.current_columns = df.columns
        self.df = df
        
    def update_columns_names(self) :
        if (len(self.df.columns) == 15) :
            self.df = self.df.drop(df.columns[-1], axis=1)
            self.current_columns = self.df.columns
        if(len(self.current_columns)== len(self.actual_columns) ):
            try :
                self.df = self.df.rename(columns = dict(zip(self.current_columns, self.actual_columns)))
            except :
                st.exception("Column count mismatch")
        else :
            # if "file" in self.df.columns :

            try :
                self.df = self.df.rename(columns = dict(zip(self.current_columns, self.actual_columns_next)))
            except :
                st.exception("Column count mismatch")
        return self.df
    
    def replace_nan_with_na(self):
        self.df.fillna("NA",inplace=True)

class jiraMapping :
    def __init__(self,df_mapping) -> None :
        self.actual_columns = ["jira_id","error"]
        self.current_columns = df_mapping.columns
        self.df_mapping = df_mapping

    def update_column_names(self) :
        if(len(self.current_columns)== len(self.actual_columns) ):
            try :
                self.df_mapping = self.df_mapping.rename(columns = dict(zip(self.current_columns, self.actual_columns)))
            except :
                st.exception("Column count mismatch")
        return self.df_mapping

with st.sidebar:
    select_screen = st.sidebar.selectbox("Option", ("BTEQ Run Analysis","Compare two BteqRun Reports"))
uploaded_file = st.file_uploader("Choose a file")


if select_screen == "BTEQ Run Analysis" :
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        preprocess = preProcessData(df)
        df = preprocess.update_columns_names()
        preprocess.replace_nan_with_na()
        st.title("Run report")
        st.write(df)
        summary = Summary(df)
        summary.buildSummary()
        summary.error_display()
        if st.button("Get All Tables Not Found"):
            summary.get_table_not_found()
        summary.keyword_error()
        summary.search_target_table()
        s = st.checkbox("List errors")
        if st.button("Get table analysis") :
            summary.get_table_completed(s)
        if st.button("Get JCL analysis") :
            summary.get_jcl_completed(s)
        uploaded_jira_mapping = st.file_uploader("Chose Jira Mapping ")
        if uploaded_jira_mapping is not None :
                df_jira = pd.read_csv(uploaded_jira_mapping)
                st.write(df_jira)
                # df_jira.columns = df_jira.columns.str.lower().str.replace(' ', '_')
                jiramap = jiraMapping(df_jira)
                df_jira = jiramap.update_column_names()
                st.write(df_jira)
                dff = df[df["target_table"] != None]
                dff.fillna("NA",inplace=True)
                cnt =0
                for i in df_jira["error"] :
                    st.write(df_jira["jira_id"][cnt])
                    cnt += 1
                    try :
                        st.write(dff[dff["error"].str.contains(i,case=False)])  
                    except :
                        st.exception("unknown exception")  
        # st.write("sd")


else :
    st.write("Compare two Bteq")
    uploaded_file_second = st.file_uploader("Choose a compare file")
    df1 = pd.read_csv(uploaded_file)
    if uploaded_file_second :
        df2 = pd.read_csv(uploaded_file_second)

        #preprocess both files
        preprocess_df1 = preProcessData(df1)
        df1 = preprocess_df1.updateColumnsNames()
        preprocess_df1.replace_nan_with_na()
        
        preprocess_df2 = preProcessData(df2)
        df2 = preprocess_df2.updateColumnsNames()
        preprocess_df2.replace_nan_with_na()

        if(len(df1) == len(df2)) :
            if df1.equals(df2):
                st.write("The two DataFrames are identical.")
            else :
                st.write("Comparing the Run files")
        else :
            st.write("Not able to compare because of missmatch in file sizes")
