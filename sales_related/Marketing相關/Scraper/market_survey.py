import requests
import pandas as pd

def get_conti_shops(token="Token On9UaUJGfifbr7iv8Wip3Qtt"):
    city_key = ['桃園市', '臺北市', '新北市', '基隆市', '宜蘭縣', '花蓮縣', '苗栗縣', '新竹市', '新竹縣',
       '彰化縣', '臺中市', '高雄市', '屏東縣', '臺南市', '嘉義市', '嘉義縣', '雲林縣', '臺東縣',
       '南投縣']
    city_value = ['北區', '北區', '北區', '北區', '北區', '北區', '中區', '北區', '北區', 
            '中區', '中區', '南區', '南區', '南區', '南區', '南區', '中區', '南區', 
            '中區']
    area = dict(zip(city_key, city_value))
    url = "https://dealerlocator.continental-tyres.com/api/v1/dealers/within_bounds.json?bbox%5Bsw_lat%5D=20.51451874962974&bbox%5Bsw_lon%5D=116.38594733593749&bbox%5Bne_lat%5D=26.554154788170955&bbox%5Bne_lon%5D=125.53755866406249&brand_key=continental&only_featured=false&max_detailed=8000&max_all_details=400&market_key=tw&business_unit_key=plt&attributes="
    headers= {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36", "Authorization": token}
    res = requests.get(url, headers=headers)
    df = pd.DataFrame(res.json())
    df["shop_type"] = df["name"].map(lambda x: "BestDrive" if "百世德" in x else "一般店")
    df["city"] = df["address"].map(lambda x: x["city"])
    df["address"] = df["address"].map(lambda x: x["street"])
    df["area"] = df["city"].map(area)
    result = df[['shop_type', 'name', 'phone', 'area', 'city', 'address', 'location']]
    return result


def get_michelin_shops():
    url = "https://www.michelin.com.tw/api/getdealer.php"
    city_key = ['台中市', '桃園市', '嘉義市', '花蓮縣', '高雄市', '屏東縣', '台南市', '苗栗縣', '台北市',
       '嘉義縣', '雲林縣', '新北市', '宜蘭縣', '基隆市', '澎湖縣', '彰化縣', '南投縣', '新竹縣',
       '新竹市', '台東縣', '金門縣']
    city_value = ['中區', '北區', '南區', '北區', '南區', '南區', '南區', '中區', '北區', 
                '南區', '中區', '北區', '北區', '北區', '南區', '中區', '中區', '北區', 
                '北區', '南區', '北區']
    area = dict(zip(city_key, city_value))
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
    df["area"] = df["county"].map(area)
    return df