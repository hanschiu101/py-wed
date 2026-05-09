import tkinter as tk
import requests
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "892da2f13edf3c7f382637760e72d224"

unit = "metric"
last_data = None


def toggle_unit():
    global unit

    if unit_var.get():
        unit = "imperial"
    else:
        unit = "metric"

    # 如果有資料就即時更新
    if last_data:
        update_display(last_data)


def get_weather():
    global last_data

    city = entry.get()

    if not city:
        result.config(text="⚠️ 請輸入城市")
        return

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric&lang=zh_tw"
    )

    try:
        data = requests.get(url).json()

        if data["cod"] != 200:
            result.config(text="❌ 找不到城市")
            return

        last_data = data
        update_display(data)

    except:
        result.config(text="⚠️ 發生錯誤")


def update_display(data):
    temp_c = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    icon = data["weather"][0]["icon"]

    if unit == "imperial":
        temp = (temp_c * 9 / 5) + 32
        symbol = "°F"
    else:
        temp = temp_c
        symbol = "°C"

    icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
    icon_img = requests.get(icon_url).content

    img = Image.open(BytesIO(icon_img))
    img = img.resize((100, 100))
    photo = ImageTk.PhotoImage(img)

    icon_label.config(image=photo)
    icon_label.image = photo

    result.config(text=f"{entry.get()}\n\n🌡 {temp:.1f}{symbol}\n{desc}")


# ===== UI =====
root = tk.Tk()
root.title("Weather App")
root.geometry("320x470")

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=10)

tk.Button(root, text="查詢天氣", command=get_weather).pack()

# ✔ 單位切換
unit_var = tk.BooleanVar()

check = tk.Checkbutton(
    root, text="顯示華氏 (°F)", variable=unit_var, command=toggle_unit
)
check.pack(pady=5)

icon_label = tk.Label(root)
icon_label.pack(pady=10)

result = tk.Label(root, font=("Arial", 14))
result.pack()

root.mainloop()
