#######################匯入模組#######################
import requests

#######################定義函數########################
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"
LANG = "zh_tw"
#######################主要程式########################
city_name = input("請輸入城市名稱:")


send_url = f"{BASE_URL}appid={API_KEY}&q={city_name}&units={UNITS}&lang={LANG}"

print(f"發送的 URL:{send_url}")
response = requests.get(send_url)
info = response.json()

if "weather" in info and "main" in info:
    current_temperature = info["main"]["temp"]
    weather_description = info["weather"][0]["description"]

    print(f"城市：{city_name}")
    print(f"溫度：{current_temperature}°C")
    print(f"描述：{weather_description}")
else:
    print("找不到該城市或無法獲取天氣資訊")