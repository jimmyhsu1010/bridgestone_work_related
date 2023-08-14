from bs_tools.zmaw import DataExtract
from datetime import datetime
import pandas as pd

cur_month = datetime.today().date().strftime("%Y-%m") + "-01"

category_table = pd.read_excel("./ReferenceTable/20220801_category_types.xlsx")
pcode = pd.read_excel("./ReferenceTable/20220721_PCODE整理表.xlsx")

def generateAct():
    result = DataExtract().sales_preprocessing()
    return result