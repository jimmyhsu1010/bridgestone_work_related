import pandas as pd
import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

st.set_page_config(page_title="Test page", layout="wide")
st.title("Test")

shows = pd.read_csv("GFK_CUSTOMREPORT_TRUCKTIRE_TW_BRIDGESTONE_Feb22.csv")

# AgGrid(shows)
gb = GridOptionsBuilder.from_dataframe(shows)

# gb.configure_pagination()
gb.configure_side_bar()
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_default_column(groupable=True, values=True, enableRowGroup=True, editable=True, enablePivot=True, draggable=True, aggFunc=["sum", "mean"])
gridOptions = gb.build()

AgGrid(gridOptions=gridOptions, enable_enterprise_modules=True, dataframe=shows)