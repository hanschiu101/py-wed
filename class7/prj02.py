#######################匯入模組#######################
from ttkbootstrap import *  # 匯入 ttkbootstrap 的所有元件，用來建立美化版 Tkinter 介面
import sys  # 匯入 sys 模組，用來取得程式執行路徑
import os  # 匯入 os 模組，用來切換工作目錄
from PIL import Image, ImageTk  # 匯入 PIL，用來開啟圖片並轉成 Tkinter 可顯示的格式

#######################設定工作目錄########################
os.chdir(sys.path[0])  # 將工作目錄切換到目前 Python 程式所在的資料夾


#######################定義函數########################
def on_switch_change():
    # 當 Checkbutton 狀態改變時，更新標籤文字
    # check_type.get() 會取得目前勾選狀態，結果為 True 或 False
    check_label.config(text=str(check_type.get()))


#######################建立視窗########################
window = Tk()  # 建立主視窗
window.title("Checkbutton")  # 設定視窗標題

#######################設定字型########################
font_size = 20  # 設定字型大小為 20
window.option_add("*Font", ("Helvetica", font_size))  # 設定整個視窗預設字型

#######################設定主題########################
style = Style(theme="minty")  # 設定 ttkbootstrap 主題為 minty

style.configure(
    "my.TCheckbutton", font=("Helvetica", font_size)
)  # 設定自訂 Checkbutton 樣式
style.configure(
    "my.TCHeckbutton", font=("Helvetica", font_size)
)  # 設定另一個樣式名稱，但目前程式中未使用

#######################建立變數########################
check_type = BooleanVar()  # 建立布林變數，用來儲存 Checkbutton 是否被勾選
check_type.set(True)  # 設定 Checkbutton 初始狀態為已勾選 True

#######################建立標籤########################
check_label = Label(window, text="True")  # 建立標籤，初始文字顯示 True
check_label.grid(
    row=1, column=2, padx=10, pady=10
)  # 使用 grid 排版，設定標籤位置與間距

image = Image.open("weather.png")  # 開啟 weather.png 圖片
img = ImageTk.PhotoImage(image)  # 將圖片轉換成 Tkinter 可使用的圖片格式

img_label = Label(window, image=img)  # 建立圖片標籤，用來顯示圖片
img_label.grid(
    row=2, column=1, columnspan=2, padx=10, pady=10
)  # 設定圖片標籤位置，橫跨 2 欄
img_label.image = img  # 保留圖片參考，避免圖片被 Python 回收而無法顯示

#######################建立Checkbutton########################
check = Checkbutton(
    window,  # 指定 Checkbutton 放在主視窗中
    variable=check_type,  # 綁定變數，用來記錄勾選狀態
    onvalue=True,  # 勾選時變數值為 True
    offvalue=False,  # 取消勾選時變數值為 False
    command=on_switch_change,  # 狀態改變時執行 on_switch_change 函數
    style="my.TCheckbutton",  # 套用自訂樣式
)

check.grid(
    row=1, column=1, padx=10, pady=10
)  # 使用 grid 排版，設定 Checkbutton 位置與間距

#######################運行主要程式########################
window.mainloop()  # 啟動主事件迴圈，讓視窗持續顯示
