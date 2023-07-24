import requests
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import json


def get_path():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    return path


def zip_code() -> dict:
    """讀取Monica整理好的郵遞區號和區域對照表

    Returns:
        dict: 返回郵遞區號和區域的字典
    """
    path = get_path()
    zip_code = pd.read_excel(path)
    zip_code_dict = dict(zip(zip_code["郵遞"], zip_code["Area"]))
    return zip_code_dict


def get_zip_code() -> dict:
    """取得各縣市對照各地區的郵遞區號

    Returns:
        dict: 返回城市和區域的郵遞區號表的字典
    """
    url = "https://zip5.5432.tw/js/zip3.js"
    res = requests.get(url)
    zip_code = json.loads(res.text.split("=")[1].split(";")[0])
    new_dict = {}
    for i, j in zip_code.items():
        new_dict[i] = {k[:-1]: int(y) for k, y in j.items()}
    return new_dict


def get_conti_shops(z_code: dict, token="Token On9UaUJGfifbr7iv8Wip3Qtt") -> pd.DataFrame:
    """取得Conti的所有經銷店家表

    Args:
        z_code (dict): 傳入郵遞區號的字典
        token (str, optional): 預設的token，如果有變更就需要去抓取. Defaults to "Token On9UaUJGfifbr7iv8Wip3Qtt".

    Returns:
        pd.DataFrame: 返回pandas表格
    """
    url = "https://dealerlocator.continental-tyres.com/api/v1/dealers/within_bounds.json?bbox%5Bsw_lat%5D=20.51451874962974&bbox%5Bsw_lon%5D=116.38594733593749&bbox%5Bne_lat%5D=26.554154788170955&bbox%5Bne_lon%5D=125.53755866406249&brand_key=continental&only_featured=false&max_detailed=8000&max_all_details=400&market_key=tw&business_unit_key=plt&attributes="
    headers= {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", "Authorization": token}
    res = requests.get(url, headers=headers)
    df = pd.DataFrame(res.json())
    df["shop_type"] = df["name"].map(lambda x: "BestDrive" if "百世德" in x else "一般店")
    df["city"] = df["address"].map(lambda x: x["city"])
    df["zip_code"] = df["address"].map(lambda x: int(x["zip_code"][:3]))
    df["address"] = df["address"].map(lambda x: x["street"])
    df["area"] = df["zip_code"].map(z_code)
    df["brand"] = "Continental"
    result = df[['brand', 'shop_type', 'name', 'phone', 'zip_code', 'area', 'city', 'address']]
    return result


def get_michelin_shops(z_code: dict) -> pd.DataFrame:
    """取得Michelin的所有經銷店家表

    Args:
        z_code (dict): 傳入郵遞區號的字典

    Returns:
        pd.DataFrame: 返回pandas表格
    """
    new_zip_code = get_zip_code()
    url = "https://www.michelin.com.tw/api/getdealer.php"
    categories = ["michelin", "tryeplus", "other"]
    dfs = []
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    for category in categories:
        data = {"category": category}
        res = requests.post(url, data=data, headers=headers)
        df = pd.DataFrame(res.json()["data"])
        df["shop_type"] = category
        dfs.append(df)
    df = pd.concat(dfs, ignore_index=True)
    df["shop_type"] = df["shop_type"].map(lambda x: "TyrePlus" if x == "tryeplus" else "MTC" if x =="michelin" else "一般店")
    df["district"] = df["district"].map(lambda x: x.replace("台", "臺") if "台東" in x else x.replace("園", "鳳") if "園山" in x else x)
    df["zip_code"] = df.apply(lambda x: new_zip_code[x["county"]][x["district"][:-1]], axis=1)
    df["area"] = df["zip_code"].map(z_code)
    df["brand"] = "Michelin"
    result = df[['brand', 'shop_type', 'name', 'tel', 'zip_code', 'area', 'county', 'address']]
    result.columns = ['brand', 'shop_type', 'name', 'phone', 'zip_code', 'area', 'city', 'address']
    return result


def get_goodyear_shops(z_code: dict) -> pd.DataFrame:
    """取得Goodyear的所有經銷店家表

    Args:
        z_code (dict): 傳入郵遞區號的字典

    Returns:
        pd.DataFrame: 返回pandas表格
    """
    url = "https://www.goodyear.com.tw/wp-content/themes/hattframework/hatt_templates/stores/ajax-find-stores.php"
    d = "se_current_location=false&coordinates=&range=10&state=&area=&specialty=&category=&current_page=1&post_per_page=10&all_stores=1"
    data = {}
    for i in d.split("&"):
        item = i.split("=")
        data[item[0]] = item[1]
    res = requests.post(url, data=data)
    df = pd.DataFrame(res.json()["all_stores"])
    df["zip_code"] = df["ht_store_postal_code"].map(lambda x: int(x[:3]))
    df["area"] = df["zip_code"].map(z_code)
    df["brand"] = "Goodyear"
    result = df[["brand", "ht_store_cat", "title", "ht_store_phone", "zip_code", "area", "ht_store_state", "ht_store_address"]]
    result.columns = ['brand', 'shop_type', 'name', 'phone', 'zip_code', 'area', 'city', 'address']
    return result


def get_competitor_shops() -> pd.DataFrame:
    """返回所有競品店的經銷商表格

    Returns:
        pd.DataFrame: 返回pandas表格
    """
    z_code = zip_code()
    mi = get_michelin_shops(z_code)
    conti = get_conti_shops(z_code)
    gy = get_goodyear_shops(z_code)
    df = pd.concat([mi, conti, gy], axis=0, ignore_index=True)
    return df
    
    
    
    