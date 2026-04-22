import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")
st.title("Cricket Data Analysis")
# Load the dataset
df=pd.read_csv("newfile.csv")

#---------NAVIGATION BAR----------------#
selected = option_menu(
    menu_title=None,
    options=["Home", "Player Analysis","Country Insights","Comparison","Data Explorer"],
    icons=["house","person","globe","bar-chart","table"],
    orientation="horizontal"
)
 #----- Home Page----#

if selected == "Home":
    st.title("Cricket Analysis Dashboard")
    col1,col2,col3 = st.columns(3)
    col1.metric("Total Player", df["Player"].nunique())
    col2.metric("Total Runs", df["Runs"].sum())
    col3.metric("Countries", df["Country"].nunique())
    st.dataframe(df.head())

#------ Player Analysis-------#

elif selected == "Player Analysis":
    st.title("Player Analysis")
    player = st.selectbox("Select Player", df["Player"])
    pdata = df[df["Player"]== player].reset_index()

    values=pdata[["100","50","4s","6s"]].iloc[0]

    fig=px.bar(
        x=values,
        y=values.index
    )

    fig.update_xaxes(range=[0, values.max() + 20])


    # stats=["100","50","4s","6s"]
    # chart_data =(
    #     pdata[stats]
    #     .iloc[0]
    #     .reset_index()
    # )
    # chart_data.columns = ["Stat","Value"]

    # fig=px.bar(
    #     chart_data,
    #     x="Stat",
    #     y="Value",
    # ) 
    col4,col5,col6,col7 = st.columns(4)
    total_runs = pdata["Runs"].sum()
    total_matches = pdata["Matches"]
    hundreds = pdata["100"].sum()
    sixties = pdata["6s"].sum()
    col4.metric(label="Total Runs", value=total_runs)
    col5.metric(label="Total Matches", value=total_matches)
    col6.metric(label="Total 100s", value=hundreds)
    col7.metric(label="Total 6s", value=sixties)
    st.plotly_chart(fig, use_container_width=True)
    
#------ Country Insights-------#

elif selected == "Country Insights":
    st.title("Country Insights")
    country_runs = df.groupby("Country")["Runs"].sum().reset_index()
    fig=px.pie(
        country_runs,
        names="Country",
        values="Runs",
    )
    st.plotly_chart(fig, use_container_width=True)

#------ Comparison-------#
elif selected == "Comparison":
    st.title("Player Comparison")
    players = st.multiselect(
        "Compare Players",
        df["Player"],
        default=df["Player"].head(5)
    )
    compare=df[df["Player"].isin(players)]
    fig=px.scatter(
        compare,
        x="Strike_rate",
        y="Ave",
        size="Runs",
        color="Country",
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected == "Data Explorer":
        st.title("Data Explorer")
        st.dataframe(df)