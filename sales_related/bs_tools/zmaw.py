import tkinter as tk
from tkinter import filedialog
import pandas as pd


class DataExtract:
    
    type_keys = ['訂單日期', '實際出貨日', '訂單單號', '訂單項次', '買方', '物料', '物料說明', '國別', '銷售數量', '銷貨單價']
    type_values = [str, str, str, str, str, str, str, str, int, int]
    type_dict = dict(zip(type_keys, type_values))
    
    def __init__(self):
        self.path = self.get_path()
        
    def get_path(self):
        paths = []
        while True:
            answer = input("選擇路徑?(Y/N)").upper()
            if answer == "Y":
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilenames()
                paths += file_path    
            else:
                break
        return paths
            
        
    def read_data(self):
        dfs = []
        # path = self.path.replace("\\", "/")
        for path in self.path:
            if path.split(".")[-1] == "csv" and "ag" in path:
                ag = pd.read_csv(path)
                ag = self.ag_extract(ag)
                dfs.append(ag)
            elif path.split(".")[-1] == "pkl" and "ag" in path:
                ag = pd.read_pickle(path)
                ag = self.ag_extract(ag)
                dfs.append(ag)
            elif path.split(".")[-1] == "csv" and "sc" in path:
                sc = pd.read_csv(path)
                sc = self.sc_extract(sc)
                dfs.append(sc)
            elif path.split(".")[-1] == "pkl" and "sc" in path:
                sc = pd.read_pickle(path)
                sc = self.sc_extract(sc)
                dfs.append(sc)
            elif path.split(".")[-1] == "xlsx" and "ag" in path:
                ag = pd.read_excel(path)
                ag = self.ag_extract(ag)
                dfs.append(ag)
            else:
                sc = pd.read_excel(path)
                sc = self.sc_extract(sc)
                dfs.append(sc)
        data = pd.concat(dfs)
        data = data.drop_duplicates(subset=["實際出貨日", "訂單單號", "訂單項次"], keep="last")
        return data

    def ag_extract(self, df):
        # ag = self.read_data()
        ag = df
        ag.columns = ag.columns.str.strip()
        ag = ag[(ag["S_配銷通路"].isin(["AG", "FT"])) & (ag["S_中計商品代號1"].isin(["LR2", "TR2", "TR3", "TR5", "TR4"]))]
        ag = ag[["D_文件日期", "D_實際發貨日期", "S_訂單單號", "S_項次", "S_買方(客戶號碼)", "S_物料編號", "S_物料說明", "S_國別", "S_數量", "S_項目淨值"]]
        ag.columns = self.type_keys
        # ag = ag.astype(self.type_dict)
        return ag
    
    def sc_extract(self, df):
        # sc = self.read_data()
        sc = df
        sc.columns = sc.columns.str.strip()
        sc = sc[sc["中計"].isin(["LSR2", "TBR3", "TBR5", "TBR2", "TBR4"])]
        sc = sc[["訂單建立日", "實際出貨日", "訂單單號", "訂單項次", "買方", "物料", "物料說明", "國別", "銷售數量", "銷貨單價"]]
        sc.columns = self.type_keys
        # sc = sc.astype(self.type_dict)
        return sc
    
    def sales_preprocessing(self):
        df = self.read_data()
        df["訂單日期"] = df["訂單日期"].dt.date
        df["實際出貨日"] = df["實際出貨日"].dt.date
        df = df.astype(self.type_dict)
        df["訂單單號"] = df["訂單單號"].map(lambda x: x.replace(".0", "") if "." in x else x)
        df["訂單項次"] = df["訂單項次"].map(lambda x: x.replace(".0", "") if "." in x else x)
        df["銷貨單價"] = df["銷貨單價"].fillna(0).astype(int)
        return df