from ttkbootstrap import *

# 匯入 ttkbootstrap 所有元件
# ttkbootstrap 是 tkinter 的美化版本，可提供較漂亮的介面主題


# =========================
# 建立主視窗
# =========================
window = Tk()

# 設定視窗標題
window.title("My GUI")


# =========================
# 設定全域字型
# =========================
font_size = 20

# 設定整個視窗預設字型
# ("字型名稱", 字型大小)
window.option_add("*Font", ("Helvetica", font_size))


# =========================
# 設定主題與按鈕樣式
# =========================
style = Style(theme="minty")

# 使用 minty 主題
# ttkbootstrap 提供許多主題，例如：
# minty、darkly、cosmo、flatly、litera 等

style.configure("my.TButton", font=("Helvetica", font_size))

# 建立自訂按鈕樣式
#
# my.TButton
# ├─ my      -> 自己命名的樣式名稱
# └─ TButton -> 表示這個樣式套用於 Button


# =========================
# 建立標籤(Label)
# =========================
label = Label(window, text="Hello World")

# 放置於第 0 列、第 0 欄
# sticky="E" 表示靠右對齊
label.grid(row=0, column=0, sticky="E")


# =========================
# 按鈕事件函式
# =========================
def show_message():
    """
    當按鈕被按下時執行
    """
    print("Hello World")

    # 將文字輸出到終端機(Console)


# =========================
# 第一個按鈕
# =========================
button = Button(window, text="瀏覽", command=show_message, style="my.TButton")

# row=0     -> 第 0 列
# column=1  -> 第 1 欄
# sticky=W  -> 靠左對齊
button.grid(row=0, column=1, sticky="W")


# =========================
# 第二個按鈕
# =========================
button2 = Button(window, text="顯示", command=show_message, style="my.TButton")

# row=1        -> 第 1 列
# column=0     -> 第 0 欄
# columnspan=2 -> 橫跨兩欄
# sticky="EW"  -> 左右延伸填滿
button2.grid(row=1, column=0, columnspan=2, sticky="EW")


# =========================
# 啟動 GUI 事件迴圈
# =========================
window.mainloop()

# 讓視窗持續顯示
# 等待使用者操作(按鈕、鍵盤、滑鼠等)
