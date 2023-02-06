import streamlit as st
import pandas as pd

def app():
    logo, space, header = st.columns([0.4, 0.4, 1])
    with logo:
        st.image("./materials/bs-logo.png")

    with header:
        st.header("GFK Report")

    with st.expander("Click here to upload the GFK raw data"):
        uploaded_file = st.file_uploader("You can choose or just drag a file here, but please use ONLY xlsx or csv file.", type=["csv", "xlsx"])
        if uploaded_file is not None:
            try:
                data = pd.read_csv(uploaded_file)
            except Exception as e:
                print(e)
                data = pd.read_excel(uploaded_file)

    st.caption("""If the file's uploaded, please click the button 'Generate the report' below.""")
    if st.button("Generate the report"):
        st.dataframe(data)


