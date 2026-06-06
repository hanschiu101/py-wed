# =========================================================
# 函式可以當成參數傳遞
# =========================================================


# 定義一個普通函式
def say_hello():
    # 印出 Hello
    print("Hello !")


# 定義一個函式
# 參數 func 代表「要被執行的函式」
def run_with_announce(func):
    # 執行傳進來的函式前，先印出提示文字
    print("Running...")

    # 呼叫傳進來的函式
    # 這裡的 func 其實就是外面傳進來的 say_hello
    func()

    # 函式執行完後，印出提示文字
    print("Done.")


# 印出提示文字
print("直接呼叫:")

# 直接呼叫 say_hello 函式
say_hello()

# 印出空行
print()

# 印出提示文字
print("透過 run_with_announce 呼叫:")

# 把 say_hello 函式本身傳進 run_with_announce
# 注意：這裡不要加括號
# say_hello 代表函式本身
# say_hello() 代表立刻執行函式
run_with_announce(say_hello)

# 印出分隔線
print("---------------------")


# =========================================================
# 裝飾器範例：不帶參數的裝飾器
# =========================================================


# 定義一個裝飾器函式
# func 代表被裝飾、被包裝的原始函式
def gift_wrap(func):

    # 定義一個內部函式 wrapper
    # wrapper 會取代原本的函式
    def wrapper():
        # 在原本函式執行前，先做一些事情
        print("Wrapping the gift...")

        # 執行原本被傳進來的函式
        func()

        # 在原本函式執行後，再做一些事情
        print("Gift wrapped!")

    # 回傳 wrapper 函式
    # 注意：這裡是 wrapper，不是 wrapper()
    # wrapper 代表把函式回傳出去
    # wrapper() 代表立刻執行 wrapper
    return wrapper


# 重新定義 say_hello 函式
# 這會覆蓋前面定義過的 say_hello
def say_hello():
    # 印出 Hello
    print("Hello !")


# 手動使用裝飾器
# 1. 把 say_hello 函式傳進 gift_wrap
# 2. gift_wrap 回傳 wrapper
# 3. 再把 wrapper 存回 say_hello
say_hello = gift_wrap(say_hello)

# 呼叫 say_hello()
# 因為 say_hello 已經被 wrapper 取代
# 所以實際執行的是 wrapper()
say_hello()


# =========================================================
# 帶參數的裝飾器
# =========================================================


# 定義一個「帶參數的裝飾器」
# name：指令名稱，例如 hello
# description：指令說明，例如 打招呼
def register_command(name, description):  # 外層函式：接收裝飾器參數

    # 當 Python 執行到 @register_command(...) 時
    # 會先呼叫這個外層函式
    print(f"[登記] 指令 /{name}: {description}")

    # 定義真正的裝飾器函式
    # func 代表被裝飾的原始函式
    def decorator(func):  # 中層函式：接收被裝飾的函式

        # 定義包裝函式
        # 呼叫原本函式時，實際上會執行 wrapper
        def wrapper():  # 內層函式：包裝原本函式

            # 在原本函式執行前，先印出指令執行訊息
            print(f"[執行] 指令 /{name}")

            # 執行原本被裝飾的函式
            func()

        # 回傳包裝後的新函式
        return wrapper

    # 回傳真正的裝飾器
    return decorator


# 使用帶參數的裝飾器
# 這行等同於：
# hello_command = register_command(
#     name="hello",
#     description="打招呼"
# )(hello_command)
@register_command(name="hello", description="打招呼")
def hello_command():
    # 原本 hello_command 要執行的內容
    print("你好！我是 hello 指令！")
