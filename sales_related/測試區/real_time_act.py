import pandas as pd
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import time
import pyodbc
import warnings
from PIL import Image,ImageTk

warnings.filterwarnings("ignore")


class RealTimeAct(tk.Tk):
    server = "10.226.0.53"
    database = "master"
    username = "BIUser"
    password = "test"
    current_month = datetime.now().strftime("'%Y-%m'")
    today = datetime.now().strftime("%Y-%m-%d")

    cnxn = pyodbc.connect(driver='SQL Server', server=server, database=database, uid=username, password=password)
    script = "select * from [10.212.27.198].FC0.dbo.V_BI_ORDER where convert(varchar(7), 訂單建立日, 120) = {}".format(current_month)

    target_path = r"D:\kc.hsu\OneDrive - Bridgestone\數據\2022ACT\2021-2022_Size Data_All_TBR_rawling_data.xlsx"
    category_table = r"C:\Users\kc.hsu\Python workspace\sales_related\ReferenceTable\20220801_category_types.xlsx"


    def __init__(self):
        super().__init__()
        self.wm_attributes("-topmost", 1)
        self.wm_title("每日TBR(G)販社訂單即時數據")
        self.ishii_of_course = tk.PhotoImage(file=r"D:\kc.hsu\My Documents\My Pictures\石井大頭娃娃of_course.gif")
        self.ishii_countermeasure = tk.PhotoImage(file=r"D:\kc.hsu\My Documents\My Pictures\石井大頭娃娃_countermeasure.gif")
        self.ishii_serious = tk.PhotoImage(file=r"D:\kc.hsu\My Documents\My Pictures\石井大頭娃娃_serious.gif")
        self.ishii_angry = tk.PhotoImage(file=r"D:\kc.hsu\My Documents\My Pictures\石井大頭娃娃_angry.gif")
        # self.wm_maxsize(400, 150)
        self.wm_iconbitmap(r"D:\kc.hsu\My Documents\My Pictures\BS方形logo.ico")
        self.connection = pd.read_sql(self.script, self.cnxn)
        self.category = pd.read_excel(self.category_table)
        self.cuscode_type = dict(zip(self.category["客戶代號"], self.category["大通路"]))
        # self.parent = parent
        self.target_vol = self.getTarget()

        self.refresh_data()
        # self.run()
        self.mainloop()

    def getTarget(self):
        df = pd.read_excel(self.target_path, sheet_name="Sheet1")
        ob = df[(df["預算/前實績"] == "23OB_V2") & (df["國內市場財別"] == "TBR(G)")]
        ob_sc_target = int(ob[(ob["年月"] == int(datetime.now().strftime("%Y%m"))) & (ob["通路明細"] != "FLT-REP")]["條數"].sum())
        ob_sc_flt_target = int(ob[(ob["年月"] == int(datetime.now().strftime("%Y%m"))) & (ob["通路明細"] == "FLT-REP")]["條數"].sum())
        ob_ttl_target = int(ob[(ob["年月"] == int(datetime.now().strftime("%Y%m")))]["條數"].sum())
        return ob_sc_target, ob_sc_flt_target, ob_ttl_target


    def refresh_data(self):
        df = self.connection
        df["中計"] = df["中計"].fillna("")
        df = df[df["實際出貨日"] <= self.today]
        df["大通路"] = df["買方"].map(self.cuscode_type)
        tbrg = df[df["中計"].str.contains("LSR2|TBR")]
        result = tbrg[tbrg["訂單類型"].isin(["ZKE", "ZSO1", "ZOR1"])][["訂單數量", "交貨數量"]].sum()
        sc = tbrg[tbrg["訂單類型"].isin(["ZKE", "ZSO1"])][["訂單數量", "交貨數量"]].sum()
        fc = tbrg[(tbrg["訂單類型"].isin(["ZOR1"])) & (tbrg["大通路"] != "OE")][["訂單數量", "交貨數量"]].sum()
        if round((int(result[1]) / self.target_vol[2]) * 100, 1) < 50:
            tk.Label(image=self.ishii_angry).grid(row=0, column=4, rowspan=5, columnspan=5)
        elif 50 <= round((int(result[1]) / self.target_vol[2]) * 100, 1) < 80:
            tk.Label(image=self.ishii_countermeasure).grid(row=0, column=4, rowspan=5, columnspan=5)
        elif 80 <= round((int(result[1]) / self.target_vol[2]) * 100, 1) < 100:
            tk.Label(image=self.ishii_serious).grid(row=0, column=4, rowspan=5, columnspan=5)
        else:
            tk.Label(image=self.ishii_of_course).grid(row=0, column=4, rowspan=5, columnspan=5)
        tk.Label(self, text="販社訂單: {}".format(int(sc[0])), font=("Arial", 12)).grid(row=0, column=0)
        tk.Label(self, text="販社出貨: {}".format(int(sc[1])), font=("Arial", 12)).grid(row=0, column=1)
        tk.Label(self, text="本月販社目標: {}".format(self.target_vol[0]), font=("Arial", 12)).grid(row=0, column=2)
        tk.Label(self, text="達成率: {}%".format(round((int(sc[1]) / self.target_vol[0]) * 100, 1)), font=("Arial", 12)).grid(row=0, column=3)
        tk.Label(self, text="FLT-REP訂單: {}".format(int(fc[0])), font=("Arial", 12)).grid(row=1, column=0)
        tk.Label(self, text="FLT-REP出貨: {}".format(int(fc[1])), font=("Arial", 12)).grid(row=1, column=1)
        tk.Label(self, text="本月FLT-REP目標: {}".format(self.target_vol[1]), font=("Arial", 12)).grid(row=1, column=2)
        tk.Label(self, text="達成率: {}%".format(round((int(fc[1]) / self.target_vol[1]) * 100, 1)),
                 font=("Arial", 12)).grid(row=1, column=3)
        tk.Label(self, text="TBR(G)訂單: {}".format(int(result[0])), font=("Arial", 12)).grid(row=2, column=0)
        tk.Label(self, text="TBR(G)出貨: {}".format(int(result[1])), font=("Arial", 12)).grid(row=2, column=1)
        tk.Label(self, text="本月TBR(G)目標: {}".format(self.target_vol[2]), font=("Arial", 12)).grid(row=2, column=2)
        tk.Label(self, text="達成率: {}%".format(round((int(result[1]) / self.target_vol[2]) * 100, 1)),
                 font=("Arial", 12)).grid(row=2, column=3)
        tk.Label(self, text="更新時間：{}".format(time.strftime("%Y-%m-%d %H:%M")), font=("Arial", 10)).grid(row=3, column=0)
        tk.Button(self, text="Download raw data", command=self.download).grid(row=3, column=3)
        self.after(20000, self.refresh_data)
        # return result

    def run(self):
        # orderLabel = (self, text="目前販社訂單總數: {}".format(int(self.refresh_data[0])), font=("Arial", 20)).grid(row=0, column=0)
        # shipLabel = self.Label(self, text="目前販社出貨總數: {}".format(int(self.refresh_data[1])), font=("Arial", 20)).grid(row=1, column=0)
        # timeLabel = self.Label(self, text="更新時間：{}".format(time.strftime("%Y-%m-%d %H:%M")), font=("Arial", 12)).grid(row=2, column=0)
        pass

    def download(self):
        df = self.connection
        df["中計"] = df["中計"].fillna("")
        df = df[df["實際出貨日"] <= self.today]
        df["大通路"] = df["買方"].map(self.cuscode_type)
        tbrg = df[df["中計"].str.contains("LSR2|TBR")]
        result = tbrg[tbrg["訂單類型"].isin(["ZKE", "ZSO1", "ZOR1"])]
        path = filedialog.askdirectory()
        export_file_name = path + "/" + datetime.today().strftime("%Y%m%d") + "_TBR(G) raw data.xlsx"
        result.to_excel(export_file_name, index=False)
        # return result


if __name__ == "__main__":
    RealTimeAct()
