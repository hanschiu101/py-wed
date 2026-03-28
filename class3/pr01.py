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
#######################運行應用程式########################
# 開始執行主迴圈，等待用戶操作
windows.mainloop()
