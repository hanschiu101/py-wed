####################### 匯入模組 #######################
import requests

# 匯入 requests 模組
# 用來向網路 API 發送請求，取得天氣資料


####################### 定義變數 ########################
API_KEY = "892da2f13edf3c7f382637760e72d224"
# OpenWeatherMap 的 API 金鑰
# 用來證明你有權限使用這個天氣 API

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
# OpenWeatherMap 目前天氣資料 API 的基本網址

UNITS = "metric"
# 設定溫度單位
# metric 代表使用攝氏溫度 °C

LANG = "zh_tw"
# 設定回傳語言
# zh_tw 代表繁體中文


####################### 主要程式 ########################
city_name = input("請輸入城市名稱:")
# 讓使用者輸入想查詢天氣的城市名稱
# 例如：Taipei、Tokyo、London

send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={UNITS}&lang={LANG}"
# 組合完整的 API 請求網址
# appid 放入 API 金鑰
# q 放入使用者輸入的城市名稱
# units 設定溫度單位
# lang 設定回傳語言

print(f"發送的 URL:{send_url}")
# 印出實際發送的網址
# 方便檢查網址內容是否正確

response = requests.get(send_url)
# 使用 requests.get() 向 API 發送 GET 請求
# response 會儲存伺服器回傳的資料

info = response.json()
# 將 API 回傳的 JSON 資料轉換成 Python 字典
# 之後就可以用 key 取出資料


if "weather" in info and "main" in info:
    # 判斷回傳資料中是否有 weather 和 main 這兩個欄位
    # 如果有，代表成功取得天氣資訊

    current_temperature = info["main"]["temp"]
    # 從 main 欄位中取得目前溫度

    weather_description = info["weather"][0]["description"]
    # 從 weather 清單中的第一筆資料取得天氣描述
    # 例如：晴、陰、多雲、小雨

    print(f"城市：{city_name}")
    # 印出使用者輸入的城市名稱

    print(f"溫度：{current_temperature}°C")
    # 印出目前溫度，單位是攝氏

    print(f"描述：{weather_description}")
    # 印出天氣描述

else:
    # 如果回傳資料中沒有 weather 或 main
    # 代表可能城市名稱錯誤，或 API 無法取得資料

    print("找不到該城市或無法獲取天氣資訊")
    # 顯示錯誤提示訊息
