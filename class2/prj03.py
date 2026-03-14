#######################匯入模組#######################
# 匯入 thinter模組和random模組
from tkinter import *
import random


#######################定義函數########################
def hi_fun():
    # 顯示"Hi Singular",並隨機選擇一種顏色
    fg_colors = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
    """
    比對展開寫法
    fg_colors="#"
    for j in range(6):
        fg_colors+=random.choice("0123456789ABCDEF")
        """
    bg_colors = "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
    display.config(text="Hi Singular", fg=fg_colors, bg=bg_colors)


#######################建立視窗########################
# 創建主視窗
windows = Tk()
# 設定主視窗標題
windows.title("My first GUI")
#######################建立按鈕########################
# 創建一個按鈕，當被按下時，就會執行hi_fun()函數
btn1 = Button(windows, text="screen", command=hi_fun)
# 將按鈕加入視窗中
btn1.pack()
#######################建立標籤########################
# 創建一個標籤，顯示"Hi Singular"，前景顏色為紅色，背景顏色為黑色
# Labl參數說明:(視窗名稱，文字內容，前景顏色，背景顏色)
display = Label(windows, text="")

# 將標籤家入主視窗中
display.pack()


#######################運行應用程式########################
# 開始執行主迴圈，等待用戶操作
windows.mainloop()
