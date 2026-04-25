#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os

#######################設定工作目錄########################
os.chdir(sys.path[0])


#######################定義函數########################
def show_result():
    entry_text = entry.get()
    try:
        result = eval(entry_text)
    except:
        result = "請輸入有效的計算式"

    label.config(text=result)


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
label = Label(window, text="計算結果")
label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

#######################建立按鈕########################
button = Button(window, text="顯示計算結果", command=show_result, style="my.TButton")
button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
#######################建立Entry########################
entry = Entry(window, width=30)
entry.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
#######################運行應用程式########################
window.mainloop()
