import streamlit as st
import pandas as pd
import numpy as np 
import plotly_express as px

'''
# Club and Nationality Viewing Application
'''
 
df = st.cache_data(pd.read_csv)("football_data.csv")

clubs = st.sidebar.multiselect('Show the Players for the club',df['Club'].unique())

countries = st.sidebar.multiselect('Show Player from country', df['Nationality'].unique())


new_df = df[(df['Club'].isin(clubs)) & (df['Nationality'].isin(countries))]

st.write(new_df)

fig = px.scatter(new_df, x='Overall', y = 'Age', color= 'Name')


'''
### Here is the result displayed in a chart
'''

st.plotly_chart(fig)


# st.write('You selected', option)

# df = pd.read_csv("football_data.csv")
# option = st.selectbox('Which club do you like best?',df['Club'].unique())
# st.write('You selected', option)

# if st.checkbox('Show dataframe'): st.write (df)

# url = st.text_input('Enter your favorite URL')
# st.write('The entered URL is', url )
# x = st.slider('x')
# st.write(x, 'squared is =', x*x)

