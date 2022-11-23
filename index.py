import streamlit as st
import pandas as pd
import plotly_express as px
# --------------------------- title and side bar ------------------------------------------------
st.title("Chess Games Analysis")
"""
An app that takes chess data and perform analysis into it.
"""
# --------------------------- side bar ---------------------------------------
st.sidebar.markdown(""" ## Data input """)
file = st.sidebar.file_uploader("File",type=["csv"])

if file:
    """## Data Overview"""
    # show head of the data
    df = pd.read_csv(file)
    colums =list(df.columns)
    cols = st.sidebar.multiselect("Columns to enclude",colums,colums)
    df = df[cols]
    st.write(df.head())
    # perform the analysis
    st.write(df.describe())
    """#### Missing values"""
    st.bar_chart(df.isna().sum())
    'Data Shape'
    st.info(df.shape)
    if st.checkbox("Clean columns with missing data ?"):
        d = df.isna().sum()
        cols = d[d>0].index
        df = df.drop(cols,axis=1)
        'Data Shape After'
        st.info(df.shape)
    if st.checkbox("Clean rows with missing data ?"):
        df = df.dropna()
        'Data Shape After'
        st.info(df.shape)

    #--------------------------- Start the question and answers ------------------------------------------
    """## Q&A Section"""
    """#### Which player wins most of the  games ? """
    """number of games won by each player or ended with draw."""
    ''
    d = df["winner"].value_counts()
    fig = px.pie(names=d.index,values=d.values,
                 color_discrete_sequence=["#FDFEFE","#17202A"," #3498DB"],
                 labels={"names":"Player","values":"Num of games"},
                 width=800,
                 height=500
                 )
    fig.update_layout(
        paper_bgcolor="#283747",
        font_color="#bbb",
        legend_title_font_size=15,
        legend_title_font_color="#fff",
        legend_title_text="Game winner"
          )
    st.plotly_chart(fig)
    """#### Do the high-ranked palyer always wins? """
    """number of games ended with the high players winning and vice versa."""
    ''
    d=df.copy()
    d["w>b"] = (d["white_rating"] > d["black_rating"])
    mask=((d["winner"]=="White" )& (d["w>b"]==True)) | ((d["winner"]=="Black") & (d["w>b"]==False))
    d["situation"] = "Low rank wins"
    d.loc[mask,"situation"] = "High rank wins"
    d = d["situation"].value_counts()
    fig = px.pie(names=d.index, values=d.values,
                 color_discrete_sequence=["#FDFEFE", "#17202A", " #3498DB"],
                 labels={"names": "Situation", "values": "Num of games"},
                 width=800,
                 height=500
                 )
    fig.update_layout(
        paper_bgcolor="#283747",
        font_color="#bbb",
        legend_title_font_size=15,
        legend_title_font_color="#fff",
        legend_title_text="Game winner"
    )
    st.plotly_chart(fig)
    """#### Which opening moves most used ? """
    d = df["opening_shortname"].value_counts().nlargest(10).sort_values(ascending=False)
    st.bar_chart(d)