#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os
from tkinter import filedialog
from PIL import Image, ImageTk

#######################建立視窗########################
window = Tk()
window.title("My  GUI")
#######################設定字型########################
font_size = 20
window.option_add("*Font", ("Helvetica", font_size))
#######################設定主題########################
style = Style(theme="minty")
# "my.TButton"的命名邏輯
# 就像幫東西貼標籤一樣,分成兩個部分,用[]關開:
# 前半段"my"->自己取的名字,可以換成任何你想要的名字,例如"big","red"
# 後半段"TButton"->固定寫法,代表[按鈕]這種元件
#                     T是Ttk(異種按鈕公具的縮寫)的縮寫
#                     就像[T桖]的T一樣,是品牌名稱的開頭
# 常見元件的後半段寫法:
# 按鈕->TButton1ul 標籤->TLabel 輸入框->TEntry
style.configure("my.TButton", font=("Helvetica", font_size))
#######################建立標籤########################
label = Label(window, text="選擇檔案:")
label.grid(row=0, column=0, sticky="E")

label2 = Label(window, text="無")
label2.grid(row=0, column=1, sticky="E")


#######################定義函數########################
def open_file():
    global file_path
    file_path = filedialog.askopenfilename(initialdir=sys.path[0])

    label2.config(text=file_path)


def show_image():
    global file_path
    image = Image.open(file_path)
    image = image.resize((canvas.winfo_width(), canvas.winfo_height()), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo


#######################建立按鈕########################
button = Button(window, text="瀏覽", command=open_file, style="my.TButton")
button.grid(row=0, column=2, sticky="W")

button2 = Button(window, text="顯示", command=show_image, style="my.TButton")
button2.grid(row=1, column=0, columnspan=3, sticky="EW")

canvas = Canvas(window, width=600, height=600)
canvas.grid(
    row=2,
    column=0,
    columnspan=3,
)
window.mainloop()
