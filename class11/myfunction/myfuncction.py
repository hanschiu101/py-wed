#######################匯入模組#######################
import requests  # 匯入 requests 模組，用來發送 HTTP 請求，取得網路 API 資料


#######################定義類別#######################
class weatherAPI:
    # 定義一個 weatherAPI 類別，用來封裝 OpenWeatherMap 天氣 API 的相關設定與功能

    def __init__(self, api_key, lang="zh_tw"):
        # 初始化方法，建立 weatherAPI 物件時會自動執行
        # api_key：OpenWeatherMap 的 API 金鑰
        # lang：回傳天氣資料的語言，預設為繁體中文 zh_tw

        self.api_key = api_key
        # 將傳入的 API 金鑰儲存到物件屬性中，之後呼叫 API 時會使用

        self.unit = "metric"
        # 設定溫度單位為 metric，代表使用攝氏溫度

        self.lang = lang
        # 儲存語言設定，例如 zh_tw 代表繁體中文

        self.url = "https://api.openweathermap.org/data/2.5/weather?"
        # OpenWeatherMap 目前天氣資料 API 的基本網址

        self.icon_base = "https://openweathermap.org/img/wn/"
        # 天氣圖示的基本網址，之後可搭配 icon 代碼取得天氣圖示圖片

    def get_current_weather(self, city_name):
        send_url = f"{self.base_url}appid={self.api_key}&q={city_name}&units={self.unit}&lang={self.lang}"

        response = requests.get(send_url)
        return response.json()

    def get_weather_summary(self, city_name):
        info = self.get_current_weather(city_name)
        if "weather" in info and "main" in info:
            return {
                city_name: info["weather"]["main"],
                "temperature": info["main"]["temp"],
                "description": info["weather"]["description"],
                "icon_code": info["weather"]["icon"],
            }
        return None

    def get_icon_url(self, icon_code):
        return f"{self.icon_base}{icon_code}@2x.png"

    def get_icon(self, icon_code):
        icon_url = self.get_icon_url(icon_code)
        response = requests.get(icon_url)
        if response.status_code == 200:
            return response.content
        return None
