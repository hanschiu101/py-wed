from ttkbootstrap import *  # 🌈 匯入美化版 Tkinter（ttkbootstrap）
from PIL import Image, ImageTk  # 🖼 處理圖片（天氣 icon）
import requests  # 🌐 發送 HTTP 請求
from io import BytesIO  # 📦 把網路圖片變成記憶體檔案

# =========================
# 🔑 OpenWeather API 設定
# =========================
API_KEY = "892da2f13edf3c7f382637760e72d224"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
UNITS = "metric"  # 🌡 預設單位（攝氏）
LANGU = "zh_tw"  # 🌏 中文天氣描述
ICON_BASE_URL = "https://openweathermap.org/img/wn/"

# 🌡 儲存目前攝氏溫度（之後可轉華氏）
current_temp_c = 0


# =========================
# 🌍 查詢天氣功能
# =========================
def get_weather():

    global current_temp_c  # 使用全域變數保存溫度

    city = city_entry.get()  # ⌨️ 取得使用者輸入城市

    # ❌ 沒輸入城市
    if city == "":
        temp_label.config(text="請輸入城市")
        return

    # 🌐 API 請求 URL（查天氣）
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"

    # 📡 發送請求
    data = requests.get(url).json()

    # ✅ 成功取得資料
    if data["cod"] == 200:

        # 🌡 取得攝氏溫度
        current_temp_c = data["main"]["temp"]

        # ☁️ 天氣描述（例如：晴天、陰天）
        desc = data["weather"][0]["description"]

        # 🌤 icon 代碼
        icon_code = data["weather"][0]["icon"]

        # 🖼 icon 圖片網址
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

        # 📥 下載圖片
        response = requests.get(icon_url)

        # 🖼 轉成 Pillow 圖片
        image_data = Image.open(BytesIO(response.content))

        # 🔄 轉成 tkinter 可用圖片
        photo = ImageTk.PhotoImage(image_data)

        # 📌 顯示圖片（避免被回收）
        icon_label.config(image=photo)
        icon_label.image = photo

        # 🌡 更新溫度顯示（會依勾選切換）
        update_temperature()

        # 📝 顯示天氣描述
        desc_label.config(text=f"描述: {desc}")

    else:
        # ❌ 找不到城市
        temp_label.config(text="找不到城市")
        desc_label.config(text="")
        icon_label.config(image="")


# =========================
# 🔁 更新溫度顯示（攝氏 / 華氏）
# =========================
def update_temperature():

    # ☑️ 如果勾選（True）→ 華氏
    if temp_var.get():

        f = (current_temp_c * 9 / 5) + 32  # 攝氏轉華氏
        temp_label.config(text=f"溫度: {f:.1f}°F")

    # 🌡 否則顯示攝氏
    else:
        temp_label.config(text=f"溫度: {current_temp_c:.1f}°C")


# =========================
# 🪟 建立主視窗
# =========================
window = Window(themename="minty")  # 🌈 ttkbootstrap 主題
window.title("Weather App")  # 視窗標題

# 📐 讓第二欄可以自動伸縮
window.columnconfigure(1, weight=1)

# =========================
# 🎨 樣式設定（字型統一）
# =========================
style = window.style

style.configure("Weather.TLabel", font=("微軟正黑體", 24))
style.configure("Weather.TEntry", font=("微軟正黑體", 24))
style.configure("Weather.TButton", font=("微軟正黑體", 22))
style.configure("Weather.TCheckbutton", font=("微軟正黑體", 18))


# =========================
# ⌨️ 城市輸入區
# =========================
city_label = Label(
    window,
    text="請輸入想搜尋的城市：",
    style="Weather.TLabel",
)
city_label.grid(row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="w")

city_entry = Entry(
    window,
    width=20,
    style="Weather.TEntry",
)
city_entry.grid(row=0, column=1, padx=10, pady=(20, 10), sticky="ew")


# =========================
# 🔘 查詢按鈕
# =========================
search_button = Button(
    window,
    text="獲得天氣資訊",
    style="Weather.TButton",
    command=get_weather,  # 點擊後查天氣
)
search_button.grid(row=0, column=2, padx=(10, 20), pady=(20, 10))


# =========================
# 🌤 圖片顯示區
# =========================
icon_label = Label(window)
icon_label.grid(row=1, column=0, padx=20, pady=20)


# =========================
# 🌡 溫度顯示
# =========================
temp_label = Label(
    window,
    text="溫度: ?°C",
    style="Weather.TLabel",
)
temp_label.grid(row=1, column=1, padx=20, pady=20)


# =========================
# ☁️ 天氣描述
# =========================
desc_label = Label(
    window,
    text="描述: ?",
    style="Weather.TLabel",
)
desc_label.grid(row=1, column=2, padx=20, pady=20)


# =========================
# ☑️ 溫度切換（攝氏 / 華氏）
# =========================
temp_var = BooleanVar()  # 勾選狀態變數

check = Checkbutton(
    window,
    text="切換成華氏溫度 °F",
    variable=temp_var,
    style="Weather.TCheckbutton",
    command=update_temperature,  # 勾選就更新溫度
)
check.grid(row=2, column=0, columnspan=3, pady=(0, 20))


# =========================
# 🚀 啟動程式
# =========================
window.mainloop()
