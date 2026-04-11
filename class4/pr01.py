#######################匯入模組#######################
# 匯入 thinter模組和random模組
from tkinter import *
from PIL import Image, ImageTk

# pip install pillow
import sys
import os

#######################設定工作目標########################
# 設定工作目標
os.chdir(sys.path[0])


#######################定義函數########################
# 定義一個函數,用來處理按下案鍵時要做的事情
def move_circle(event):
    # 取得按下的按鈕
    key = event.keysym
    print(key)  # 判斷按下的是哪一個按鍵,並根據不同按鈕來移動不同的圓形
    if key == "Right":
        canvas.move(circle, 10, 0)
    elif key == "Left":
        canvas.move(circle, -10, 0)
    elif key == "Up":
        canvas.move(circle, 0, -10)
    elif key == "Down":
        canvas.move(circle, 0, 10)
    elif key == "w":
        canvas.move(rectangle, 0, -10)
    elif key == "s":
        canvas.move(rectangle, 0, 10)
    elif key == "a":
        canvas.move(rectangle, -10, 0)
    elif key == "d":
        canvas.move(rectangle, 10, 0)


#######################建立視窗########################
# 創建主視窗
windows = Tk()
#######################建立畫布########################
# 創建一個畫布，設定其寬度為600，高度為600
canvas = Canvas(windows, width=600, height=600, bg="white")
# 將畫布加入主視窗中
canvas.pack()
# 設定主視窗標題
windows.title("My first GUI")
#######################設定視窗圖片########################
# 設定視窗圖片
windows.iconbitmap("crocodile2.ico")
#######################載入圖片########################
# tkinter 內建 PhotoImage ,只支援PNG、GIF、PGM、PPM格式(不支援JPG、BMG等)
# img = PhotoImage(file="crocodile2.png")
# [Pillow 方式]使用Image.open()載入圖片
# 好處:
# 1.支援幾乎所有格式(JPG、PNG、BMP、WebP、TIFF 等)
# 2.可以顯示前對圖片做處理(縮放、載切、旋轉、慮鏡等)
imge = Image.open("crocodile2.png")
# 將PIL Image物件轉換thinter可用的PhotoImage物件
img = ImageTk.PhotoImage(imge)
#######################圖片顯示########################
# 在畫布上顯示圖片,設定圖片的中心座標為(300,300)
my_image = canvas.create_image(300, 300, image=img)
#######################畫圓形########################

# 在畫布上畫一個圓形,起初位置是(250,150),結束位置為(300,200),填充顏色為紅色
circle = canvas.create_oval(250, 150, 300, 200, fill="red")
# 在畫布上畫一個矩形,起初位置是(220,400),結束位置為(340,200),填充顏色為藍色
rectangle = canvas.create_rectangle(220, 400, 340, 430, fill="blue")
# 在畫布上顯示一段文字,位置為(300,100),文字為"Corcodile",顏色為黑色,字體為Arial,大小為30
msg = canvas.create_text(300, 100, text="Corcodile", fill="black", font=("Arial", 30))
#######################綁定案鍵事件########################
# 將案鍵事件綁定到畫布上,當按下鍵盤上的任意鍵時,移動對應物件
canvas.bind_all("<Key>", move_circle)

#######################運行應用程式########################
# 開始執行主迴圈，等待用戶操作
windows.mainloop()
