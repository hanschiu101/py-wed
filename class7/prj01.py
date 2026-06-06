####################### 匯入模組 #######################
import requests  # 用來發送 HTTP 請求，取得網路 API 資料
import os  # 用來處理作業系統相關功能，例如切換資料夾
import sys  # 用來取得程式執行路徑等系統資訊

####################### 定義變數 #######################
API_KEY = "892da2f13edf3c7f382637760e72d224"
# OpenWeatherMap 的 API 金鑰，用來授權取得天氣資料

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
# OpenWeatherMap 目前天氣 API 的基本網址

UNITS = "metric"
# 設定溫度單位為攝氏

LANG = "zh_tw"
# 設定回傳的天氣描述語言為繁體中文

ICON_BASE_URL = "https://openweathermap.org/img/wn/"
# 天氣圖示的基本網址

####################### 主要程式 #######################
os.chdir(sys.path[0])
# 將目前工作目錄切換到程式所在的資料夾
# 這樣下載的 weather.png 會儲存在程式同一個資料夾中

city_name = input("請輸入城市名稱:")
# 讓使用者輸入想查詢天氣的城市名稱

send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={UNITS}&lang={LANG}"
# 組合完整的 API 請求網址
# 包含 API 金鑰、城市名稱、溫度單位與語言設定

print(f"發送的 URL:{send_url}")
# 印出發送的 API 網址，方便檢查是否正確

response = requests.get(send_url)
# 向 OpenWeatherMap 發送 GET 請求，取得天氣資料

info = response.json()
# 將 API 回傳的 JSON 格式資料轉成 Python 字典

if "weather" in info and "main" in info:
    # 檢查回傳資料中是否包含 weather 和 main
    # 若有，代表成功取得天氣資訊

    current_temperature = info["main"]["temp"]
    # 從 main 中取得目前溫度

    weather_description = info["weather"][0]["description"]
    # 從 weather 清單中的第一筆資料取得天氣描述

    icon_code = info["weather"][0]["icon"]
    # 取得天氣圖示代碼，例如 01d、02n 等

    print(f"城市：{city_name}")
    # 印出查詢的城市名稱

    print(f"溫度：{current_temperature}°C")
    # 印出目前溫度

    print(f"描述：{weather_description}")
    # 印出天氣描述

    icon_url = f"{ICON_BASE_URL}{icon_code}@4x.png"
    # 組合完整的天氣圖示下載網址
    # @4x 代表較大尺寸的圖示

    print(f"下載天氣圖表 URL: {icon_url}")
    # 印出圖示下載網址

    icon_response = requests.get(icon_url)
    # 發送請求下載天氣圖示圖片

    if icon_response.status_code == 200:
        # 如果 HTTP 狀態碼是 200，代表圖片下載成功

        with open(f"weather.png", "wb") as icon_file:
            # 以二進位寫入模式開啟 weather.png 檔案
            # 如果檔案不存在會自動建立

            icon_file.write(icon_response.content)
            # 將下載到的圖片內容寫入 weather.png

            print("天氣圖表保存為weather.png")
            # 顯示圖片已成功儲存
    else:
        # 如果狀態碼不是 200，代表圖片下載失敗

        print("天氣圖表下載失敗")
        # 顯示下載失敗訊息else:
    print("查詢失敗，請確認城市名稱是否正確")
