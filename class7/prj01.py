#######################匯入模組#######################
import requests
import os
import sys

#######################定義函數########################
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
ICON_BASE_URL = "https://openweathermap.org/img/wn/"
#######################主要程式########################
os.chdir(sys.path[0])
city_name = input("請輸入城市名稱:")


send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={UNITS}&lang={LANG}"

print(f"發送的 URL:{send_url}")
response = requests.get(send_url)
info = response.json()

if "weather" in info and "main" in info:
    current_temperature = info["main"]["temp"]
    weather_description = info["weather"][0]["description"]
    icon_code = info["weather"][0]["icon"]
    print(f"城市：{city_name}")
    print(f"溫度：{current_temperature}°C")
    print(f"描述：{weather_description}")
    icon_url = f"{ICON_BASE_URL}{icon_code}@4x.png"
    print(f"下載天氣圖表 URL: {icon_url}")
    icon_response = requests.get(icon_url)
    if icon_response.status_code == 200:
        with open(f"weather.png", "wb") as icon_file:
            icon_file.write(icon_response.content)
            print("天氣圖表保存為weather.png")
    else:
        print("天氣圖表下載失敗")
