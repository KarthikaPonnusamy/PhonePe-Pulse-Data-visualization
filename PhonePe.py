import pandas as pd
import plotly.express as px
import pymysql
import streamlit as st
import os
import json
from streamlit_option_menu import option_menu
from PIL import Image


#CONNECT WITH LOCAL DB
mydb = pymysql.connect(host="127.0.0.1",
                        user="root",
                        password="admin@123",
                        database="PhonePe_pulsedata"
                    )
cursor = mydb.cursor()

cursor.execute("select Years,Quarter,Transaction_type,Transaction_count as Transaction_count from aggregated_transactions group by Years,Quarter,Transaction_type,Transaction_count")
table2=cursor.fetchall()
chart_data=pd.DataFrame(table2,columns=("Years","Quarter","Transaction_type","Transaction_count"))



#MENU - HOME PAGE
icon = Image.open("ICN.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded"
                   )

st.sidebar.header(":violet[**Phonepe Pulse Data Visualization**]")


with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data on Map","Contact Us"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-1px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
    

if selected == "Home":

    st.markdown("# :violet[PhonePe Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1,col2 = st.columns([2,2],gap="medium")
    with col1:
        st.markdown("##")
        st.image("PhonePe_logo.jpg")
        text = """
                **The Indian digital payments story has truly captured the world's imagination.** 
                *From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet, and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government*.

                *Founded in December 2015, PhonePe has been a strong beneficiary of the API-driven digitization of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India*.

                **PhonePe Pulse** *is our way of giving back to the digital payments ecosystem*.
                """


        st.markdown(text, unsafe_allow_html=True)
        st.write("---")

    with col2:

        st.video("C:/Users/pkart/OneDrive/Desktop/phonepe/PhonepeVideo.mp4")

#MENU - TOP CHARTS
if selected == "Top Charts":

    st.markdown("## :violet[Top Charts]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")

    with colum1:
        Year = st.slider("**Transaction Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Transaction Quarter", min_value=1, max_value=4)


    # Top Charts - TRANSACTIONS    
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")


        if Year == 2023 and Quarter == 4:
            styled_text = "<div style='text-align: center; color: blue; font-weight: bold;'>DATA NOT AVAILABLE FOR SELECTION</div>"
            st.markdown(styled_text,unsafe_allow_html=True)
        else:

            #PIE CHART FOR TOP STATE WITH TRANSACTIONS       
            with col1:

                    st.markdown("### :violet[State]")
                    cursor.execute(f"select States, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from aggregated_transactions where Years = {Year} and Quarter = {Quarter} group by States order by Total desc limit 10")
                    df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
                    fig = px.pie(df, values='Total_Amount',
                                    names='State',
                                    title='Top 10',
                                    color_discrete_sequence=px.colors.sequential.Agsunset,
                                    hover_data=['Transactions_Count'],
                                    labels={'Transactions_Count':'Transactions_Count'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)


            #PIE CHART FOR TOP DISTRICT WITH TRANSACTIONS        
            with col2:

                    st.markdown("### :violet[District]")
                    cursor.execute(f"select District , sum(Transaction_count) as Total_Count, sum(Transaction_amount) as Total from map_transaction where Years = {Year} and Quarter = {Quarter} group by District order by Total desc limit 10")
                    df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

                    fig = px.pie(df, values='Total_Amount',
                                    names='District',
                                    title='Top 10',
                                    color_discrete_sequence=px.colors.sequential.Agsunset,
                                    hover_data=['Transactions_Count'],
                                    labels={'Transactions_Count':'Transactions_Count'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)


            #PIE CHART FOR TOP PINCODE WITH TRANSACTIONS   
            with col3:

                    st.markdown("### :violet[Pincode]")
                    cursor.execute(f"select pincodes, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_transaction where Years = {Year} and Quarter = {Quarter} group by pincodes  order by Total desc limit 10")
                    df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
                    fig = px.pie(df, values='Total_Amount',
                                    names='Pincode',
                                    title='Top 10',
                                    color_discrete_sequence=px.colors.sequential.Agsunset,
                                    hover_data=['Transactions_Count'],
                                    labels={'Transactions_Count':'Transactions_Count'})

                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig,use_container_width=True)
            
# Top Charts - USERS          
    if Type == "Users":

        selection = st.radio("Select chart type",["Bar chart TOP 10 Brands & District","Pie chart TOP 10 Pincode & State"],horizontal=True)
   
        if Year == 2023 and Quarter == 4:

            styled_text = "<div style='text-align: center; color: blue; font-weight: bold;'>DATA NOT AVAILABLE FOR SELECTION</div>"
            st.markdown(styled_text,unsafe_allow_html=True)

        else:

            if selection == "Bar chart TOP 10 Brands & District":
                col1,col2 = st.columns([2,2],gap="small")
                
                #TOP USERS - BRAND
                with col1:
                        st.markdown("### :violet[Brands]")
                        cursor.execute(f"select Brands, sum(Transaction_count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from aggregated_user where Years = {Year} and Quarter = {Quarter} group by Brands order by Total_Count desc limit 10")
                        df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                        fig = px.bar(df,
                                    title='Top 10',
                                    x="Total_Users",
                                    y="Brand",
                                    orientation='h',
                                    color='Avg_Percentage',
                                    color_continuous_scale=px.colors.sequential.Agsunset)
                    
                        st.plotly_chart(fig,use_container_width=True)   

                #TOTAL USER - DISTRICT
                with col2:
                        st.markdown("### :violet[District]")
                        cursor.execute(f"select Districts, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where Years = {Year} and Quarter = {Quarter} group by Districts order by Total_Users desc limit 10")
                        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
                        df.Total_Users = df.Total_Users.astype(float)
                        fig = px.bar(df,
                                    title='Top 10',
                                    x="Total_Users",
                                    y="District",
                                    orientation='h',
                                    color='Total_Users',
                                    color_continuous_scale=px.colors.sequential.Agsunset)
                    
                        st.plotly_chart(fig,use_container_width=True)


         
            elif selection == "Pie chart TOP 10 Pincode & State":
                col3,col4 = st.columns([2,2],gap="small")

                #TOP USER - PINCODE
                with col3:
                        st.markdown("### :violet[Pincode]")
                        cursor.execute(f"select Pincodes, sum(RegisteredUser) as Total_Users from top_user where Years = {Year} and Quarter = {Quarter} group by Pincodes order by Total_Users desc limit 10")
                        df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Total_Users'])
                        fig = px.pie(df,
                                    values='Total_Users',
                                    names='Pincode',
                                    title='Top 10',
                                    color_discrete_sequence=px.colors.sequential.Agsunset,
                                    hover_data=['Total_Users'])
                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig,use_container_width=True)

                #TOP USER - STATE          
                with col4:
                        st.markdown("### :violet[State]")
                        cursor.execute(f"select States, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where Years = {Year} and Quarter = {Quarter} group by States order by Total_Users desc limit 10")
                        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
                        fig = px.pie(df, values='Total_Users',
                                        names='State',
                                        title='Top 10',
                                        color_discrete_sequence=px.colors.sequential.Agsunset,
                                        hover_data=['Total_Appopens'],
                                        labels={'Total_Appopens':'Total_Appopens'})

                        fig.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig,use_container_width=True)

    #TOP PAYMENT TYPE
    st.markdown("## :violet[Top Payment Type]")

    cursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from aggregated_transactions where Years= {Year} and Quarter = {Quarter} group by Transaction_type order by Transaction_type")
    df =pd.DataFrame(cursor.fetchall(),columns=(["Transaction_type","Total_Transactions","Total_amount"]))

    fig = px.bar(df,
                    title='Transaction Types vs Total_Transactions',
                    x="Transaction_type",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Magenta)
    
    st.plotly_chart(fig,use_container_width=False)
    



#MENU-EXPLORE DATA
    
if selected == "Explore Data on Map":
        
        st.markdown("## :violet[Explore Data on Map and Charts]")
        Type = st.selectbox("**Type**", ("Transactions", "Users"))
        mapcol1,mapcol2 = st.columns([2,2],gap="small")

        with mapcol1:
            Year= st.selectbox("Select the Transaction Year",("2018","2019","2020","2021","2022"))
        with mapcol2:
            Quarter=st.selectbox("Select the Transaction Quarter",("1","2","3","4"))

        if Type == "Transactions":

            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            cursor.execute(f"select States, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where Years = {Year} and Quarter = {Quarter} group by States order by States")
            table1 = cursor.fetchall()
            Aggre_trans = pd.DataFrame(table1,columns = ("States","Total_Transactions" ,"Total_amount"))
            Aggre_trans.Total_Transactions=  Aggre_trans.Total_Transactions.astype(int)

            #MAP FUNCTION - STATES & AMOUNT
    
            fig = px.choropleth(
                                Aggre_trans,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='States',
                                color='Total_amount',
                                hover_data='States',
                                color_continuous_scale="oxy",
                                range_color=(0, 5000000000))

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(width= 900, height= 700)
            fig.update_layout(
                            geo=dict(
                                lonaxis=dict(range=[-5, 200]),  # Adjust the longitude axis range
                                lataxis=dict(range=[150, 300]),      # Adjust the latitude axis range
                            )
                        )
                                
            st.plotly_chart(fig)


            #MAP FUNCTION - STATES & TRANSACTION
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            fig = px.choropleth(
                                Aggre_trans,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='States',
                                color='Total_Transactions',
                                hover_data='States',
                                color_continuous_scale="Picnic",
                                range_color=(0,20000000))
            

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(width= 900, height= 700)
            fig.update_layout(
                            geo=dict(
                                lonaxis=dict(range=[-5, 200]),  # Adjust the longitude axis range
                                lataxis=dict(range=[150, 300]),      # Adjust the latitude axis range
                            )
                        )
            st.plotly_chart(fig)


            #TRANSACTION ON SELECTED DISTRICTS
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("# ")
            st.markdown("## :violet[Select State to explore more]")
            state=st.selectbox("select the state",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                'Uttarakhand', 'West Bengal'),index=30)
            
            
         
            cursor.execute(f"select States, District,Years,Quarter, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from map_transaction where Years = {Year} and Quarter = {Quarter} and States = '{state}' group by States, District,Years,Quarter order by States,District")
        
            df1 = pd.DataFrame(cursor.fetchall(), columns=['States','District','Years','Quarter',
                                                         'Total_Transactions','Total_amount'])
            fig = px.bar(df1,
                            title=state,
                            x="District",
                            y="Total_Transactions",
                            orientation='v',
                            color='Total_amount',
                            color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)


        if Type =="Users":
                
                st.markdown("## :violet[State Data - User App opening frequency]")
                

                cursor.execute(f"select States, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where Years = {Year} and Quarter = {Quarter} group by States order by States")
                df=pd.DataFrame(cursor.fetchall(),columns=["States","Total_Users","Total_Appopens"])              
                df.Total_Appopens=df.Total_Appopens.astype(float)

                #MAP FUNCTION - STATES & APPOPENS
                fig = px.choropleth(
                                df,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='States',
                                color='Total_Appopens',
                                hover_data='States',
                                color_continuous_scale="Purp",
                                range_color=(0,400000000))
            

                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(width= 900, height= 700)
                fig.update_layout(
                            geo=dict(
                                lonaxis=dict(range=[-5, 200]),  # Adjust the longitude axis range
                                lataxis=dict(range=[150, 300]),      # Adjust the latitude axis range
                            )
                        )
                st.plotly_chart(fig)

                #Bar chart- district wise App opens
                st.markdown("# ")
                st.markdown("# ")
                st.markdown("# ")
                st.markdown("## :violet[Select State to explore more]")
                state=st.selectbox("select the state",('Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                                                'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                                                'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa',
                                                'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir',
                                                'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep',
                                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
                                                'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan',
                                                'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                                                'Uttarakhand', 'West Bengal'),index=30)
                

                cursor.execute(f"select States,Years,Quarter,Districts,sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where Years = {Year} and Quarter = {Quarter} and States = '{state}' group by States, Districts,Years,Quarter order by States,Districts")
                df = pd.DataFrame(cursor.fetchall(), columns=['States','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
                df.Total_Appopens = df.Total_Appopens.astype(int)

                fig = px.bar(df,
                                title=state,
                                x="District",
                                y="Total_Appopens",
                                orientation='v',
                                color='Total_Appopens',range_color=(0,50000000),
                                color_continuous_scale=px.colors.sequential.Purpor)
                st.plotly_chart(fig,use_container_width=True)

if selected == "Contact Us":
        
        st.markdown("## :violet[Contact Us]")
        col1, col2 =st.columns([3,2],gap="medium")
        with col1:
            st.image("abc.png")
        with col2:
            st.header("**Key**")
             
            text = """
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;***The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. 
                    The report is available as a free download on the PhonePe Pulse website and GitHub.***
                    """
            st.write(text, unsafe_allow_html=True)

    
            name = "Data visualized by: Karthika P "
            mail = (f'{"Mail :"}  {"pkarthika923@gmail.com"}')
            social_media = {"GITHUB": "https://github.com/KarthikaPonnusamy ",
                            "LINKEDIN": "https://www.linkedin.com/in/karthika-p-863361277/"
                            }
            st.subheader(name)
            st.write(mail)
            
            cols = st.columns(len(social_media))
            for index, (platform, link) in enumerate(social_media.items()):
                cols[index].write(f"[{platform}]({link})")

       
                
        
