import streamlit as st
from streamlit.script_runner import RerunException
import pandas as pd
import calendar
pd.set_option("display.max_columns", None)
pd.set_option("mode.chained_assignment", None)
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Bridgestone tools", layout="wide", page_icon="./materials/bs-logo-small.png")

# 設定不要顯示"Made with Stramlit"

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

### GFK數據處理視覺化

df = pd.read_csv(
    r"D:\kc.hsu\OneDrive - Bridgestone\GFK data\202201\GFK_CUSTOMREPORT_TRUCKTIRE_TW_BRIDGESTONE_Jan22.csv")

date = datetime.today().strftime("%Y-%m-%d")
date = datetime.strptime(date, "%Y-%m-%d")
interval = date - relativedelta(months=14)
interval = interval.strftime("%Y-%m")
gfk = df.copy()
gfk["Period"] = pd.to_datetime(gfk["Period"], yearfirst=True)
# gfk["Period"] = gfk["Period"].dt.to_period("M")
gfk["Period"] = gfk["Period"].dt.strftime("%Y-%m")
filtered_data = gfk[gfk["Period"] >= interval]

## Top 10 list
top10_players = ["BRIDGESTONE", "MAXXIS", "MICHELIN", "LINGLONG", "JINYUTIRES", "PRESA", "DUNLOP", "GOODYEAR",
                 "YOKOHAMA"]
filtered_data["PLAYERS"] = filtered_data["BRAND"].map(lambda x: "The others" if x not in top10_players else x)

filtered_data = filtered_data.astype({"SALES UNITS": "int", "SALES <LC>": "int", "PRICE TWD/UN.": "int"})

bar_sales_units = filtered_data.groupby(["Period", "BRIDGESTONE TYPE"])[["SALES UNITS"]].sum().reset_index()
bar_sales_units = bar_sales_units.sort_values(by="SALES UNITS", ascending=False)
bar_sales_units["in %"] = 100 * (
            bar_sales_units["SALES UNITS"] / bar_sales_units.groupby("Period")["SALES UNITS"].transform("sum"))

ttl_table = filtered_data[filtered_data["BRIDGESTONE TYPE"] != "EXCLUDED TBR AND LSR2"].groupby(["Period", "BRIDGESTONE TYPE"])[
    ["SALES UNITS"]].sum().unstack("Period").reset_index()

df = df.astype({"SALES UNITS": "int", "SALES <LC>": "int", "PRICE TWD/UN.": "int"})
df["Period"] = pd.to_datetime(df["Period"], dayfirst=True)
qt_data = df.groupby([pd.Grouper(key="Period", freq="QS"), "BRIDGESTONE TYPE"])[["SALES UNITS"]].sum().reset_index()
qt_data["Year"] = qt_data["Period"].dt.year
qt_data["Quarter"] = qt_data["Period"].dt.quarter
qt_data = qt_data.astype({"Year": "str", "Quarter": "str"})
qt_data["Y+Q"] = qt_data["Year"] + "Q" + qt_data["Quarter"]
qt_data["in %"] = 100 * (qt_data["SALES UNITS"] / qt_data.groupby("Period")["SALES UNITS"].transform("sum"))

ttl_qt_table = qt_data[qt_data["BRIDGESTONE TYPE"] != "EXCLUDED TBR AND LSR2"].groupby(["Y+Q", "BRIDGESTONE TYPE"])[["SALES UNITS"]].sum().unstack("Y+Q").reset_index()

### GFK文字敘述
gfk_numbers = filtered_data.groupby(["Period"])[["SALES UNITS"]].sum().reset_index()
previous_mon = int(datetime.today().strftime("%m")) - 1
before_pre_mon = previous_mon - 1
month_names = [calendar.month_name[i] for i in range(1, 13)]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
month_dict = dict(zip(months, month_names))
result_description = "a. " + month_dict[previous_mon] + " vs " + month_dict[before_pre_mon] + " " + "{:.0f}%".format(100 * gfk_numbers.iloc[-1, 1] / gfk_numbers.iloc[-2, 1]) + " , vs PY " + "{:.0f}%".format(100 * gfk_numbers.iloc[-1, 1] / gfk_numbers.iloc[0, 1])

current_year = datetime.today().strftime("%Y")
# 檢查目前今年的資料是幾個月的
cum_months = len(gfk_numbers[gfk_numbers["Period"].str.contains(current_year)])
# 今年累計數量
ytd_units = gfk_numbers[gfk_numbers["Period"].str.contains(current_year)]["SALES UNITS"].sum()
# 去年累計數量
py_units = gfk_numbers[gfk_numbers["Period"].str.contains(str(cum_months - 1))]["SALES UNITS"][0:cum_months].sum()
ytd_py = "b. YTD vs PY " + "{:.0f}%".format(100 * ytd_units / py_units)


logo, space, header = st.columns([0.4, 0.4, 1])
with logo:
    st.image("./materials/bs-logo.png")

with header:
    st.header("GFK report")

st.subheader("Monthly Total sales in unit")

st.write(result_description)
st.write(ytd_py)
chart1, chart2 = st.columns([1, 0.6])
with chart1:
    st.plotly_chart(px.bar(bar_sales_units, x="Period", y="SALES UNITS", color="BRIDGESTONE TYPE",
                           text=bar_sales_units["in %"].map(lambda x: "{:.0f}%".format(x)),
                           title="Monthly truck tires sales units"))
with chart2:
    st.plotly_chart(px.bar(qt_data, x="Y+Q", y="SALES UNITS", color="BRIDGESTONE TYPE", text=qt_data["in %"].map(lambda x: "{:.0f}%".format(x)), labels={"Y+Q": "Quarter"}, title="Quarterly truck tires sales units"))


table1, table2 = st.columns([1, 0.6])
with table1:
    st.write(ttl_table)
with table2:
    st.write(ttl_qt_table)

