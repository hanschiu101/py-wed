def say_hello():
    print("Hello !")


def run_with_announce(func):
    print("Running...")


func()
print("Done.")

print("直接呼叫:")
say_hello()

print()
print("透過run_with_announce呼叫:")
run_with_announce(say_hello)

print("---------------------")


# =========================================================
# =========================================================
def gift_wrap(func):
    def wrapper():
        print("Wrapping the gift...")
        func()
        print("Gift wrapped!")

    return wrapper


def say_hello():
    print("Hello !")


say_hello = gift_wrap(say_hello)
say_hello()
