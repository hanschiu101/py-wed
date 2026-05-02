#######################匯入模組#######################
from ttkbootstrap import *
import sys
import os

#######################設定工作目錄########################
os.chdir(sys.path[0])
#######################定義函數########################
#######################建立視窗########################
window = Tk()
window.title("Checkbutton")
#######################設定字型########################
font_size = 20
window.option_add("*Font", ("Helvetica", font_size))
#######################設定主題########################
style = Style(theme="minty")

style.configure("my.TCheckbutton", font=("Helvetica", font_size))
style.configure("my.TCHeckbutton", font=("Helvetica", font_size))
