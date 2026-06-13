import requests
import asyncio
import discord
import os
from dotenv import load_dotenv
from myfunction.myfuncction import weatherAPI

# 載入 .env 檔案中的環境變數
load_dotenv()

# 建立新的 asyncio 事件迴圈
asyncio.set_event_loop(asyncio.new_event_loop())

# 設定 Discord Bot 權限
intents = discord.Intents.default()

# 允許 Bot 讀取訊息內容
intents.message_content = True

# 建立 Discord Client 物件
bot = discord.Client(intents=intents)

# 建立 Slash Command 指令樹
tree = discord.app_commands.CommandTree(bot)

# 建立天氣 API 物件，並從環境變數讀取 API Key
weather_api = weatherAPI(os.getenv("WEATHER_API_KEY"))


# 建立天氣資訊用的 Discord Embed
def build_embed(weather_summary):
    embed = discord.Embed(
        # Embed 標題顯示城市名稱
        title=f"{weather_summary['city_name']}的天氣",
        # Embed 描述顯示天氣描述
        description=f"{weather_summary['description']}",
        # 設定 Embed 顏色
        color=discord.Colour.from_str("#0E90FF"),
    )

    # 取得天氣圖示網址
    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])

    # 設定 Embed 縮圖為天氣圖示
    embed.set_thumbnail(url=icon_url)

    # 新增溫度欄位
    embed.add_field(
        name="溫度",
        value=f"{weather_summary['temperature']}°C",
        inline=False,
    )

    # 回傳建立好的 Embed
    return embed
def build_forecast_embeds(forecast_summary):
    embeds = []
    for forecast in forecast_summary:
        embed = discord.Embed(
            title=f"{forecast['city_name']}的天氣",
            description=f"{forecast['description']}",
            color=discord.Colour.from_str("#1E90FF"),
        )
        icon_url = weather_api.get_icon_url(forecast["icon_code"])
        embed.set_thumbnail(url=icon_url)
        embed.add_field(
            name="溫度",
            value=f"{forecast['temperature_celsius']}°C",
            inline=False,
        )
        embeds.append(embed)

    return embeds

# 當 Bot 成功登入 Discord 時會執行
@bot.event
async def on_ready():
    # 在終端機顯示登入成功訊息
    print(f"({bot.user}) 已登入！")

    # 同步 Slash Commands 到 Discord
    await tree.sync()


# 當 Discord 頻道中有訊息時會執行
@bot.event
async def on_message(message):
    # 如果訊息是 Bot 自己發的，就忽略，避免自動回覆自己
    if message.author == bot.user:
        return

    # 如果使用者輸入 hello
    if message.content == "hello":
        # Bot 回覆你好
        await message.channel.send("你好！")


# 建立 /hello Slash Command
@tree.command(name="hello", description="say hello to the bot")
async def hello(interaction: discord.Interaction):
    # 回覆使用者
    await interaction.response.send_message("你好！")


# 建立 /weather Slash Command
@tree.command(name="weather", description="get weather info")
async def weather(interaction: discord.Interaction, city_str: str, forecast: bool = False):
    # 先延後回應，避免 API 查詢太久導致 Discord 判定互動逾時
    await interaction.response.defer()

    # 去除使用者輸入城市名稱前後的空白
    city = city_str.strip()

    # 檢查是否有設定 OpenWeatherMap API Key
    if not weather_api.api_key:
        await interaction.followup.send("請先設定 OpenWeatherMap API 金鑰！")
        return


    try:
        if not forecast:
            weather_summary = weather_api.get_weather_summary(city)
            if weather_summary is None:
                await interaction.followup.send("找不到該城市的天氣資訊！")
                return
            embed = build_embed(weather_summary)
            await interaction.followup.send(embed=embed)
            return
        forecast_summary = weather_api.get_forecast_summary(city)
        
    except (requests.RequestException, ValueError) :
        await interaction.followup.send("查詢天氣資訊失敗！")
        return

    if forecast_summary is None:
        await interaction.followup.send("找不到該城市的天氣預報！")
        return
    embeds = build_forecast_embeds(forecast_summary)
    await interaction.followup.send(embeds=embeds[:10])


# 程式進入點
def main():
    # 使用 .env 中的 Discord Bot Token 啟動 Bot
    bot.run(os.getenv("DC_BOT_TOKEN"))


# 如果這個檔案是直接執行，就呼叫 main()
if __name__ == "__main__":
    main()
