import pandas as pd
import plotly.express as px
import pymysql
import os
import json
import streamlit as st
import requests
import geopandas as gpd
import matplotlib.pyplot as plt

# df = pd.read_csv("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/active_cases_2020-07-17_0800.csv")

# fig = px.choropleth(
#     df,
#     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#     featureidkey='properties.ST_NM',
#     locations='state',
#     color='active cases',
#     color_continuous_scale='Greens'
# )

# fig.update_geos(fitbounds="locations", visible=False)

# fig.show()


mydb = pymysql.connect(host="127.0.0.1",
                    user="root",
                    password="admin@123",
                    database="PhonePe_pulsedata"
                    )
cursor = mydb.cursor()

cursor.execute("select * from aggregated_transactions;")
table1 = cursor.fetchall()
Aggre_trans = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

# cursor.execute("select States,Transaction_type, sum(Transaction_count) as Transaction_count from aggregated_transactions group by States,Transaction_type")
# table1 = cursor.fetchall()
# Aggre_trans = pd.DataFrame(table1,columns = ("States","Transaction_type", "Transaction_count"))

#Aggregated_user
cursor.execute("select * from aggregated_user")
mydb.commit()
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_transaction
cursor.execute("select * from map_transaction")
mydb.commit()
table3 = cursor.fetchall()
Map_trans = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
cursor.execute("select * from map_user")
mydb.commit()
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#Top_transaction
cursor.execute("select * from top_transaction")
mydb.commit()
table5 = cursor.fetchall()
Top_trans = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
cursor.execute("select * from top_user")
mydb.commit()
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser")) 

if st.sidebar.button("home"):
    st.write("hi")

if st.sidebar.button("map"):


    data_column = Aggre_trans["Transaction_type"]
    fig = px.choropleth(
        Aggre_trans,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='States',
        color='Transaction_amount',
        hover_data = 'States',
        title='Transaction amount on states',
        color_continuous_scale="dense",
        range_color=(0, 4000000000)
        
    )

    fig.update_geos(fitbounds="locations", visible=False)

    fig.show()




 


# url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"

# # Load GeoJSON data
# response = requests.get(url)
# if response.status_code == 200:
#     data1 = response.json()
# else:
#     st.error(f"Failed to load GeoJSON data. Status code: {response.status_code}")
#     st.stop()

# state_names_tra = [feature["properties"]["ST_NM"] for feature in data1["features"]]
# state_names_tra.sort()

# df_state_names_tra = pd.DataFrame({"States": state_names_tra})

# frames = []

# for year in Map_user["Years"].unique():
#     for quarter in Aggre_trans["Quarter"].unique():
#         at1 = Aggre_trans[(Aggre_trans["Years"] == year) & (Aggre_trans["Quarter"] == quarter)]
#         atf1 = at1[["States", "Transaction_amount"]]
#         atf1 = atf1.sort_values(by="States")
#         atf1["Years"] = year
#         atf1["Quarter"] = quarter
#         frames.append(atf1)

# merged_df = pd.concat(frames)

# fig_tra = px.choropleth(
#     merged_df,
#     geojson=data1,
#     locations="States",
#     featureidkey="properties.ST_NM",
#     color="Transaction_amount",
#     color_continuous_scale="Sunsetdark",
#     range_color=(0, 4000000000),
#     hover_name="States",
#     title="TRANSACTION AMOUNT",
#     animation_frame="Years",
#     animation_group="Quarter"
# )

# fig_tra.update_geos(fitbounds="locations", visible=False)
# fig_tra.update_layout(width=600, height=700)
# fig_tra.update_layout(title_font={"size": 25})

# # Display the Plotly chart using Streamlit
# st.plotly_chart(fig_tra)  
