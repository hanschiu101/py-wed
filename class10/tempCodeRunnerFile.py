#######################模組#######################
# 匯入 asyncio，用來處理非同步事件迴圈
import asyncio

# 匯入 discord.py，用來連接與操作 Discord Bot
import discord

# 匯入 os，用來讀取環境變數
import os

# 從 dotenv 匯入 load_dotenv，用來讀取 .env 檔案
from dotenv import load_dotenv

#######################初始化#######################
# 讀取 .env 檔案中的環境變數
load_dotenv()

# 建立並設定新的 asyncio 事件迴圈
asyncio.set_event_loop(asyncio.new_event_loop())

# 建立 Discord intents，決定 Bot 可以接收哪些事件
intents = discord.Intents.default()

# 開啟讀取訊息內容的權限
# 若要使用 message.content 判斷訊息內容，必須啟用
intents.message_content = True

# 建立 Discord Client 物件
bot = discord.Client(intents=intents)

# 建立斜線指令管理器
tree = discord.app_commands.CommandTree(bot)


#######################事件#######################
# 當 Bot 成功登入並準備完成時觸發
@bot.event
async def on_ready():
    # 在終端機輸出登入成功訊息
    print(f"({bot.user}) 已登入！")

    # 將斜線指令同步到 Discord
    await tree.sync()


# 當頻道中有新訊息時觸發
@bot.event
async def on_message(message):
    # 如果訊息作者是 Bot 自己，就直接忽略
    # 避免 Bot 回覆自己的訊息造成無限循環
    if message.author == bot.user:
        return

    # 如果使用者輸入的訊息是 hello
    if message.content == "hello":
        # 在同一個頻道回覆「你好！」
        await message.channel.send("你好！")


#######################指令#######################
# 建立斜線指令 /hello
# name：指令名稱
# description：指令說明
@tree.command(name="hello", description="say hello to the bot")
async def hello(interaction: discord.Interaction):
    # 回覆斜線指令的互動訊息
    await interaction.response.send_message("你好！")


#######################啟動#######################
# 主程式函式
def main():
    # 從環境變數讀取 DC_BOT_TOKEN，並啟動 Bot
    bot.run(os.getenv("DC_BOT_TOKEN"))


# 如果這個檔案是被直接執行，就執行 main()
if __name__ == "__main__":
    main()
