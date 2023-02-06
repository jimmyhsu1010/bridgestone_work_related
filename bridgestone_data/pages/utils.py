import pandas as pd
import calendar
pd.set_option("display.max_columns", None)
pd.set_option("mode.chained_assignment", None)
import plotly.express as px
from datetime import datetime
from dateutil.relativedelta import relativedelta


class GfkEtl:
    def __init__(self, data):
        self.data = data # Uploaded GFK raw data

    def type_change(self):
        self.data = self.data.astype({"SALES UNITS": "int", "SALES <LC>": "int", "PRICE TWD/UN.": "int"})


