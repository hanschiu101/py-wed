import requests

API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast?"
UNITS = "metric"
LANG = "zh_tw"

city_name = "Taipei"

send_url = (
    f"{BASE_URL}q={city_name}"
    f"&appid={API_KEY}"
    f"&units={UNITS}"
    f"&lang={LANG}"
)

print(f"發送的 URL: {send_url}")

response = requests.get(send_url)
response.raise_for_status()

info = response.json()
print(info)

# 檢查回傳資料中是否包含 city 和 list 欄位
if "city" in info and "list" in info:
    for forecast in info["list"]:
        dt_txt = forecast["dt_txt"]
        temp = forecast["main"]["temp"]
        weather_description = forecast["weather"][0]["description"]

        print(dt_txt, temp, weather_description)
else:
    print("找不到城市")

    