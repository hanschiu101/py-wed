####################### 匯入模組 #######################
from ttkbootstrap import *

# 匯入 ttkbootstrap 的所有元件
# ttkbootstrap 可以用來建立較美觀的 Tkinter GUI 介面

import sys

# 匯入 sys 模組，用來取得程式執行相關資訊

import os

# 匯入 os 模組，用來處理資料夾路徑等作業系統功能


####################### 設定工作目錄 ########################
os.chdir(sys.path[0])
# 將目前工作目錄切換到程式檔案所在的資料夾
# 這樣之後讀取或儲存檔案時，會以程式所在位置為基準


####################### 定義函數 ########################
def show_result():
    # 定義一個函數 show_result
    # 當使用者按下按鈕時，會執行這個函數

    entry_text = entry.get()
    # 取得輸入框 Entry 中的文字內容
    # 例如使用者輸入：1+2*3

    try:
        # 嘗試執行可能會發生錯誤的程式碼

        result = eval(entry_text)
        # 使用 eval() 計算輸入的算式
        # 例如 "1+2*3" 會被計算成 7

    except:
        # 如果 eval() 計算時發生錯誤，就會執行這裡

        result = "請輸入有效的計算式"
        # 將結果設定成錯誤提示文字

    label.config(text=result)
    # 將 label 標籤顯示的文字改成計算結果或錯誤訊息


####################### 建立視窗 ########################
window = Tk()
# 建立主視窗物件

window.title("My  GUI")
# 設定視窗標題為 My GUI


####################### 設定字型 ########################
font_size = 20
# 設定字型大小為 20

window.option_add("*Font", ("Helvetica", font_size))
# 設定整個視窗中所有元件的預設字型
# Helvetica 是字型名稱，font_size 是字型大小


####################### 設定主題 ########################
style = Style(theme="minty")
# 建立 Style 物件，並設定 ttkbootstrap 主題為 minty

# "my.TButton" 的命名邏輯：
# 前半段 "my" 是自己取的樣式名稱，可以改成其他名稱，例如 "big"、"red"
# 後半段 "TButton" 是固定寫法，代表這個樣式套用在 ttk 按鈕元件上
#
# 常見元件樣式名稱：
# 按鈕  -> TButton
# 標籤  -> TLabel
# 輸入框 -> TEntry

style.configure("my.TButton", font=("Helvetica", font_size))
# 設定自訂按鈕樣式 my.TButton
# 讓使用這個樣式的按鈕字型變成 Helvetica、大小為 font_size


####################### 建立標籤 ########################
label = Label(window, text="計算結果")
# 建立 Label 標籤元件
# window 代表這個標籤放在主視窗上
# text="計算結果" 代表一開始顯示的文字

label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
# 使用 grid() 排版標籤
# row=2 表示放在第 2 列
# column=0 表示放在第 0 欄
# columnspan=2 表示橫跨 2 欄
# padx=10 表示左右外距 10
# pady=10 表示上下外距 10


####################### 建立按鈕 ########################
button = Button(window, text="顯示計算結果", command=show_result, style="my.TButton")
# 建立 Button 按鈕元件
# text 是按鈕上顯示的文字
# command=show_result 表示按下按鈕時會執行 show_result 函數
# style="my.TButton" 表示套用剛剛設定的自訂按鈕樣式

button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
# 使用 grid() 排版按鈕
# 放在第 1 列、第 0 欄，並橫跨 2 欄


####################### 建立 Entry ########################
entry = Entry(window, width=30)
# 建立 Entry 輸入框元件
# width=30 表示輸入框寬度約為 30 個字元

entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
# 使用 grid() 排版輸入框
# 放在第 0 列、第 0 欄，並橫跨 2 欄


####################### 運行應用程式 ########################
window.mainloop()
# 啟動視窗事件迴圈
# 程式會一直執行，等待使用者操作視窗
