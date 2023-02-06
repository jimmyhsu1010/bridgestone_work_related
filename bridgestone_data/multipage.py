"""
這個檔案主要是用來在物件的情況下在streamlit實現頁面轉換
"""

# Import necessary libraries
import streamlit as st

# Define the multipage class to manage the multiple apps in the program
class MultiPage:

    def __init__(self):
        """初始化會生成list來存放其他的頁面應用"""
        self.pages = []

    def add_page(self, title, func):
        """用來新增頁面的method

        Args:
            title :: str 要用來增加到app的頁面名稱
            func :: 要用來在streamlit上面生成的頁面功能
        """

        self.pages.append(
            {
                "title": title,
                "function": func
            }
        )

    def run(self):
        # 下拉式選單建立的method
        page = st.sidebar.selectbox(
            "BRIDGESTONE TOOLS MENU",
            self.pages,
            format_func=lambda page: page["title"]
        )

        # run the app function
        page["function"]()


