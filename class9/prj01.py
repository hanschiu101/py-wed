# 定義一個普通函式
def say_hello():
    print("Hello !")


# 定義一個函式，參數 func 代表「要被執行的函式」
def run_with_announce(func):
    print("Running...")  # 執行前先印出提示

    func()  # 執行傳進來的函式

    print("Done.")  # 執行完後印出提示


print("直接呼叫:")
say_hello()  # 直接呼叫 say_hello 函式

print()
print("透過 run_with_announce 呼叫:")

# 把 say_hello 函式當成參數傳進 run_with_announce
# 注意：這裡是 say_hello，不是 say_hello()
run_with_announce(say_hello)

print("---------------------")


# =========================================================
# 裝飾器範例：不帶參數的裝飾器
# =========================================================


# 定義一個裝飾器函式
# func 代表被包裝的原始函式
def gift_wrap(func):

    # wrapper 是包裝後的新函式
    def wrapper():
        print("Wrapping the gift...")  # 執行原函式前做的事

        func()  # 執行原本的函式

        print("Gift wrapped!")  # 執行原函式後做的事

    # 回傳包裝後的函式
    return wrapper


# 重新定義 say_hello 函式
def say_hello():
    print("Hello !")


# 手動使用裝飾器
# 把 say_hello 傳進 gift_wrap
# 再把回傳的 wrapper 存回 say_hello
say_hello = gift_wrap(say_hello)

# 這時呼叫 say_hello()
# 其實是在呼叫 wrapper()
say_hello()


# =========================================================
# 帶參數的裝飾器
# =========================================================


# 定義一個「帶參數的裝飾器」
# name：指令名稱，例如 hello
# description：指令說明，例如 打招呼
def register_command(name, description):  # 外層：接收裝飾器參數

    # 當裝飾器被建立時，先印出登記指令的訊息
    print(f"[登記] 指令 /{name}: {description}")

    # 定義真正的裝飾器
    # func 代表被裝飾的原始函式
    def decorator(func):  # 中層：接收函式

        # 定義包裝函式
        # 之後呼叫原本函式時，其實會執行 wrapper
        def wrapper():  # 內層：包裝函式

            # 在執行原本函式前，先印出執行指令的訊息
            print(f"[執行] 指令 /{name}")

            # 執行原本被裝飾的函式
            func()

        # 回傳包裝後的新函式
        return wrapper

    # 回傳真正的裝飾器 decorator
    return decorator


@register_command(name="hello", description="打招呼")
def hello_command():
    print("你好！我是 hello 指令！")
