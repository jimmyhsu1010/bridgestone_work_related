import streamlit as st
import pandas as pd
import plotly.express as px

from multipage import MultiPage
from pages import gfk_report #import the pages we need here

# 建立app物件
app = MultiPage()

# 主頁面的佈局建立
st.set_page_config(page_title="Bridgestone tools", layout="wide", page_icon="./materials/bs-logo-small.png") #設定網頁佈局和標籤logo

# 設定不要顯示"Made with Stramlit"
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 加入app
app.add_page("GFK Report Generator", gfk_report.app)

# The main app
app.run()