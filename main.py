import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

file = st.file_uploader(" Upload your excel file here", type=['xlsx'])
if file:
    df= pd.read_excel(file)


    df1= df.iloc[:,:22]
    st.write(df.head(50))#################################
    df1 = df1.fillna(0)

    df2= df1.iloc[:,1:]
    for col in df2.columns:
        try:
            df2[col] = pd.to_numeric(df2[col], errors='coerce')
            df2[col].fillna(0, inplace=True)
        except Exception as e:  
            print("An error occurred:", e)

    # scaling = MinMaxScaler()
    scaling = StandardScaler()
    scaled_df2 = scaling.fit_transform(df2)
    df2 = pd.DataFrame(scaled_df2,columns=df2.columns)

    # print(df2.head())

    # df_keyphrase = df.iloc[:,0]

    df1['Keyword Phrase'] = df1['Keyword Phrase'].str.replace('[^a-zA-Z0-9]','')

    dfn = df1['Keyword Phrase']
    dfn = dfn.dropna(how='all')

    dfn = dfn.sort_values(ascending= False)

    # dfn.to_csv('keyword phrase.csv')

    df3 = pd.concat([dfn, df2], axis=1)

    df3['score'] =  df2.sum(axis=1)
    
    new_df = df3.iloc[:, [0, -1]]

    new_df.sort_values('Keyword Phrase', ascending= False)
    sv = st.number_input('how much minimum keyword score you want?:', min_value=1, max_value=10, value=5)
    if sv:
        def g(df, num):
            filtered_df = df[(df['Keyword Phrase'].str.startswith('a')) & (df['score'] > num)]
            for char in range(ord('b'), ord('z') + 1):
                filtered_df = pd.concat([filtered_df, df[(df['Keyword Phrase'].str.startswith(chr(char))) & (df['score'] > num)]])
            
            return filtered_df

    df_k = g(new_df.copy(),sv)
    
    
   

    df_k['category'] = df_k['Keyword Phrase'].str[0].str.lower()
    print(df_k.head())

    file = df_k.to_csv()

    number = st.number_input('how many keyword you wantto display?:', min_value=0, max_value=500, value=50)
    st.write("Number of Total rows: ",df_k.shape[0])
    if number:    
        st.write((df_k.head(number)))  
        st.download_button(
            label="Download",
            data=file,
            file_name="keyword.csv",    
        )

