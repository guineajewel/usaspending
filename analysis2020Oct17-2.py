# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 11:53:20 2020

@author: Mohammed Kamal

YES 1. Populate “_Cnt1” table in the csv_database for October 2008 thru December 2008 and 
   for January 2009 thru December 2019
   [Read the csv files from ./data_noflt/*.csv and create table name ends withh _Cnt and append for all agencies]
NO 2. Populate “allagency1” table based on allaward and filteredaward
NO 3. Populate “vendors1” table based on 

"""

import os
import pandas as pd
import setuprefvar as st
import linuxpostgres_cred as creds
import sqlstmnts as sqst

from sqlalchemy import create_engine

conn_string = "postgresql://"+creds.PGUSER+":"+creds.PGPASSWORD+"@"+creds.PGHOST+":"+creds.PORT+"/"+creds.PGDATABASE
engine = create_engine(conn_string)

agency_year = st.years
agency_abb  = st.agencyabb
agency_code = st.agencycode

for m in range(len(agency_abb)):
    Cnt_table_name = agency_abb[m]+"_Cnt1"
    #Plt_table_name = agency_abb[m]+"_Plt1"
    #ana_table_name = agency_abb[m]+"_analysis_n1"     
    
    path1 = '/data/backups/.spyder-py3/data_noflt/2008_OctToDec_noflt_'+ agency_abb[m] +'_'+ agency_code[m] +'_Prime/'
    dirs = os.listdir(path1)
    #print(path1)
    #print(dirs)
    for i in range(len(dirs)):
        filename = path1+dirs[i]
        print(filename)            
        
        #use this df only for "_Cnt1"
        df = pd.read_csv(filename, usecols=st.forcount1, dtype=st.forcountdtype, encoding='utf-8')
        print(Cnt_table_name)
        df.to_sql(Cnt_table_name, engine, if_exists='append')

        ##use this df only for "_Plt1"
        # df = pd.read_csv(filename, usecols=st.forplot1, dtype=st.forplotdtype, encoding='utf-8')
        # #use this filter only for "_Plt1" -- do not use filder for "_Cnt1"
        # df = df[  (df['naics_code'].isin(st.selected_naics)) & \
        #       (df['primary_place_of_performance_country_code']=="USA") 
        #      ]
        # print(Plt_table_name)
        # df.to_sql(Plt_table_name, engine, if_exists='append')

        # print(ana_table_name)
        # df = pd.read_csv(filename, usecols=st.forana1, dtype = st.foranadtype, encoding='utf-8')
        # df = df[(df['naics_code'].isin(st.selected_naics)) & \
        #  (df['primary_place_of_performance_country_code']=="USA")]
    
        # df['period_of_performance_start_date']=df['period_of_performance_start_date'].str[:10]
        # df['period_of_performance_current_end_date']=df['period_of_performance_current_end_date'].str[:10]
        # df['period_of_performance_potential_end_date']=df['period_of_performance_potential_end_date'].str[:10]
        # df.to_sql(ana_table_name, engine, if_exists='append')

for m in range(len(agency_abb)):
    Cnt_table_name = agency_abb[m]+"_Cnt1"
#    Plt_table_name = agency_abb[m]+"_Plt1"
#    ana_table_name = agency_abb[m]+"_analysis_n1"
     
    for l in range(len(agency_year)):
        path1 = '/data/backups/.spyder-py3/data_noflt/' + agency_year[l] + '_JanToDec_noflt_'+ agency_abb[m] +'_'+ agency_code[m] +'_Prime/'
        dirs = os.listdir(path1)
        
        for i in range(len(dirs)):
            filename = path1+dirs[i]
            print(filename)            
            
            #use this df only for "_Cnt1"
            df = pd.read_csv(filename, usecols=st.forcount1, dtype=st.forcountdtype, encoding='utf-8')
            print(Cnt_table_name)
            df.to_sql(Cnt_table_name, engine, if_exists='append')
    
            # #use this df only for "_Plt1"
            # df = pd.read_csv(filename, usecols=st.forplot1, dtype=st.forplotdtype, encoding='utf-8')
            # #use this filter only for "_Plt1" -- do not use filder for "_Cnt1"
            # df = df[  (df['naics_code'].isin(st.selected_naics)) & \
            #       (df['primary_place_of_performance_country_code']=="USA") 
            #      ]
            # print(Plt_table_name)
            # df.to_sql(Plt_table_name, engine, if_exists='append')
    
            # print(ana_table_name)
            # df = pd.read_csv(filename, usecols=st.forana1, dtype = st.foranadtype, encoding='utf-8')
            # df = df[(df['naics_code'].isin(st.selected_naics)) & \
            #  (df['primary_place_of_performance_country_code']=="USA")]
        
            # df['period_of_performance_start_date']=df['period_of_performance_start_date'].str[:10]
            # df['period_of_performance_current_end_date']=df['period_of_performance_current_end_date'].str[:10]
            # df['period_of_performance_potential_end_date']=df['period_of_performance_potential_end_date'].str[:10]
            # df.to_sql(ana_table_name, engine, if_exists='append')
            
for m in range(len(agency_abb)):    
    table_name = 'allagency1'
    agencyabb=[agency_abb[m]]
    sqlstmt = sqst.sqlst13.format(agency_abb[m])
    df = pd.read_sql_query(sqlstmt, engine)
    sqlstmt = sqst.sqlst14.format(agency_abb[m])
    df1 = pd.read_sql_query(sqlstmt, engine)
    df['allaward'] = df1['allaward']
    df['allawardtotal'] = df1['allawardtotal']
    df['filteredaward'] = df1['filteredaward']
    df['filteredawardtotal'] = df1['filteredawardtotal']
    
    for i in range(10):
        agencyabb.append(agency_abb[m])
    df['agency_abb'] = agencyabb
    df.to_sql(table_name, engine, if_exists='append')
    
# table_name = 'vendors1'
# for m in range(len(agency_abb)):
#     sqlst = sqst.sqlst6.format(agency_abb[m])
#     df = pd.read_sql_query(sqlst, engine)
#     df[df.columns[1]] = df[df.columns[1]].replace('[\$,]', '', regex=True).astype(float)
#     df['agency_abb'] = agency_abb[m]
#     df['index'] = m
#     df.to_sql(table_name, engine, if_exists='append')