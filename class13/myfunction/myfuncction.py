####################### 匯入模組 #######################
import requests  # 匯入 requests 模組，用來發送 HTTP 請求，取得 API 回傳資料


####################### 定義類別 #######################
class weatherAPI:
    # 定義 weatherAPI 類別
    # 用來封裝 OpenWeatherMap 天氣 API 的設定與功能

    def __init__(self, api_key, lang="zh_tw"):
        # 建構子：建立 weatherAPI 物件時會自動執行
        # api_key：OpenWeatherMap 的 API 金鑰
        # lang：回傳資料的語言，預設為繁體中文 zh_tw

        self.api_key = api_key
        # 儲存 API 金鑰，之後呼叫 API 時會使用

        self.unit = "metric"
        # 設定溫度單位為 metric，代表攝氏溫度

        self.lang = lang
        # 儲存語言設定

        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast?"
        # OpenWeatherMap 目前天氣 API 的基本網址

        self.icon_base = "https://openweathermap.org/img/wn/"
        # 天氣圖示的基本網址

    def get_current_weather(self, city_name):
        # 取得指定城市的目前天氣資料
        # city_name：城市名稱，例如 "Taipei"

        send_url = (
            f"{self.base_url}"
            f"appid={self.api_key}"
            f"&q={city_name}"
            f"&units={self.unit}"
            f"&lang={self.lang}"
        )
        # 組合完整的 API 請求網址
        # 包含 API key、城市名稱、溫度單位與語言設定

        response = requests.get(send_url)
        # 使用 requests 發送 GET 請求給 OpenWeatherMap API

        return response.json()
        # 將 API 回傳的 JSON 資料轉成 Python 字典並回傳

    def get_weather_summary(self, city_name):
        # 取得指定城市的天氣摘要資訊

        info = self.get_current_weather(city_name)
        # 呼叫 get_current_weather 方法，取得完整天氣資料

        if "weather" in info and "main" in info:
            # 檢查回傳資料中是否包含 weather 和 main 欄位
            # 避免城市名稱錯誤或 API 回傳錯誤時發生程式錯誤

            return {
                "city_name": city_name,
                # 城市名稱
                "weather": info["weather"][0]["main"],
                # 天氣主要狀態，例如 Clear、Clouds、Rain
                "temperature": info["main"]["temp"],
                # 目前溫度，單位為攝氏
                "description": info["weather"][0]["description"],
                # 天氣詳細描述，例如 晴天、多雲、小雨
                "icon_code": info["weather"][0]["icon"],
                # 天氣圖示代碼，可用來取得對應圖片
            }

        return None
        # 如果資料格式不正確，回傳 None

    def get_icon_url(self, icon_code):
        # 根據天氣圖示代碼產生完整圖片網址
        # icon_code：OpenWeatherMap 回傳的圖示代碼，例如 "01d"

        return f"{self.icon_base}{icon_code}@2x.png"
        # 回傳天氣圖示圖片的完整網址

    def get_icon(self, icon_code):
        # 下載指定天氣圖示圖片

        icon_url = self.get_icon_url(icon_code)
        # 取得完整的天氣圖示網址

        response = requests.get(icon_url)
        # 發送 GET 請求下載圖片

        if response.status_code == 200:
            # 如果 HTTP 狀態碼是 200，代表圖片下載成功

            return response.content
            # 回傳圖片的二進位內容

        return None
        # 如果下載失敗，回傳 None

    def get_forecast(self, city_name):
        send_url = (
            f"{self.forecast_url}q={city_name}&appid={self.api_key}"
            f"&units={self.unit}&lang={self.lang}"
        )
        response = requests.get(send_url)
        response.raise_for_status()
        return response.json()

    def get_forecast_summary(self, city_name, count=10):
        forecast_count = max(0, count)
        try:
            info = self.get_forecast(city_name)
            print(info)
        except requests.HTTPError as error:
            response = error.response
            if response is not None and response.status_code == 404:
                return None
            raise
        if "city" not in info and "list" not in info:
            return None
        city_label = info["city"].get("name", city_name)
        forecast_summary = []

        for forecast in info["list"][:forecast_count]:
            forecast_summary.append(
                {
                    "city_name": city_label,
                    "datetime": forecast["dt_txt"],
                    "temperature_celsius":round( forecast["main"]["temp"],2),
                    "description": forecast["weather"][0]["description"],
                    "icon_code": forecast["weather"][0]["icon"],
                }
            )
        return forecast_summary