#######################匯入模組#######################
from tkinter import *


#######################定義函數########################
def hi_fun():
    # 透過change變數來判斷是否要顯示"Hi SinguLar"或是清空標籤
    global change
    if change == False:
        display.config(text="green", fg="black", bg="green")
    else:
        display.config(text="red", fg="black", bg="red")
    change = not (change)


# 初始直射為False
change = False

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
