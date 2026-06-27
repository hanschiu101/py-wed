import requests  # 匯入 requests 套件，用來發送 HTTP 請求

# OpenWeatherMap API 金鑰
API_KEY = "892da2f13edf3c7f382637760e72d224"

# OpenWeatherMap 5 天 / 3 小時天氣預報 API 網址
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?"

# 設定溫度單位為攝氏
UNITS = "metric"

# 設定回傳語言為繁體中文
LANG = "zh_tw"

# 要查詢天氣的城市名稱
city_name = "Taipei"

# 組合完整的 API 請求網址
send_url = (
    f"{BASE_URL}q={city_name}"      # 城市名稱參數
    f"&appid={API_KEY}"             # API 金鑰
    f"&units={UNITS}"               # 溫度單位
    f"&lang={LANG}"                 # 回傳語言
)

# 印出實際發送的 URL，方便檢查
print(f"發送的 URL: {send_url}")

# 發送 GET 請求到 OpenWeatherMap API
response = requests.get(send_url)

# 如果 HTTP 狀態碼不是 200，會拋出錯誤
response.raise_for_status()

# 將 API 回傳的 JSON 資料轉成 Python 字典
info = response.json()

# 印出完整的回傳資料，方便除錯
print(info)

# 檢查回傳資料中是否包含 city 和 list 欄位
# city：城市資訊
# list：天氣預報資料列表
if "city" in info and "list" in info:

    # 逐筆讀取天氣預報資料
    for forecast in info["list"]:

        # 預報時間
        dt_txt = forecast["dt_txt"]

        # 溫度，單位是攝氏
        temp = forecast["main"]["temp"]

        # 天氣描述，例如：晴、陰、多雲、小雨
        weather_description = forecast["weather"][0]["description"]

        # 印出時間、溫度與天氣描述
        print(dt_txt, temp, weather_description)

else:
    # 如果回傳資料沒有 city 或 list，代表可能查詢失敗
    print("找不到城市")
    