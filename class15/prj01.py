# 匯入 requests 套件，用來發送 HTTP 請求呼叫天氣 API
import requests

# 匯入 asyncio 套件，提供 Python 非同步程式功能
import asyncio

# 匯入 discord.py 套件，用來建立 Discord Bot
import discord

# 匯入 os 模組，用來讀取環境變數
import os

# 匯入 load_dotenv，用來載入 .env 檔案中的環境變數
from dotenv import load_dotenv

# 匯入自訂 weatherAPI 類別，負責查詢天氣資訊
from myfunction.myfuncction import weatherAPI, AIAssistant

# 載入 .env 檔案中的環境變數
load_dotenv()

# 建立 Discord Bot 需要的 Intents
intents = discord.Intents.default()

# 開啟讀取訊息內容的權限
# 若要使用 on_message 接收使用者訊息，必須設為 True
intents.message_content = True

# 建立 Discord Client
bot = discord.Client(intents=intents)

# 建立 Slash Command 指令樹
tree = discord.app_commands.CommandTree(bot)

# 建立天氣 API 物件
# API Key 從 .env 的 WEATHER_API_KEY 讀取
weather_api = weatherAPI(os.getenv("WEATHER_API_KEY"))
ai_assistant = AIAssistant(os.getenv("OPENAI_API_KEY"))


# 限制讀取的歷史訊息數量，避免一次把整個頻道都交給 AI。
CHANNEL_HISTORY_LIMIT = 15

# system_prompt 像是給 AI 的角色卡，會影響 AI 回覆的語氣和工作方式。
CHAT_SYSTEM_PROMPT = """
你是一個在 Discord 群組頻道中協助大家的 AI 助手。
請根據頻道歷史判斷大家正在討論什麼，再回答最新提到你的問題。
回覆請使用繁體中文，語氣自然、簡短、適合國小學生閱讀。
如果頻道歷史不足以判斷答案，請說明你還需要哪一個資訊。
如果需要提到特定使用者或其他 bot，請複製歷史訊息裡的 mention：<@使用者ID>。
使用 mention 時，請直接放在一般文字中，不要寫成 @名字，也不要加反斜線、反引號或程式碼區塊。
不要使用 @everyone、@here 或角色標記，也不要自己編造 mention ID。
"""

# 允許 AI 回覆中提到「使用者或 bot」，但不要讓 AI 觸發 @everyone、@here 或角色標記。
# bot 在 Discord 裡也屬於 user，所以 users=True 就可以提到其他 bot。
AI_REPLY_ALLOWED_MENTIONS = discord.AllowedMentions(
    everyone=False,
    users=True,
    roles=False,
    replied_user=True,
)
# 建立目前天氣資訊的 Embed
def build_embed(weather_summary):
    # 建立 Embed 物件
    embed = discord.Embed(
        # 標題顯示城市名稱
        title=f"{weather_summary['city_name']}的天氣",
        # 描述顯示天氣狀態
        description=f"{weather_summary['description']}",
        # Embed 顏色
        color=discord.Colour.from_str("#0E90FF"),
    )

    # 取得天氣圖示網址
    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])

    # 設定右上角縮圖
    embed.set_thumbnail(url=icon_url)

    # 新增溫度欄位
    embed.add_field(
        name="溫度",
        value=f"{weather_summary['temperature']}°C",
        inline=False,
    )

    # 回傳完成的 Embed
    return embed


# 建立天氣預報的多個 Embed
def build_forecast_embeds(forecast_summary):
    # 建立多個天氣預報 Embed
    # forecast_summary：由 get_forecast_summary() 回傳的天氣預報資料

    # 用來存放所有 Embed
    embeds = []

    # 逐筆處理預報資料
    for forecast in forecast_summary:
        # 建立單筆預報 Embed
        embed = discord.Embed(
            # Embed 標題
            title=f"{forecast['city_name']}的天氣",

            # 顯示天氣描述
            description=f"{forecast['description']}",

            # Embed 顏色
            color=discord.Colour.from_str("#1E90FF"),
        )

        # 取得該時段的天氣圖示網址
        icon_url = weather_api.get_icon_url(forecast["icon_code"])

        # 設定縮圖
        embed.set_thumbnail(url=icon_url)

        # 加入溫度資訊
        embed.add_field(
            name="溫度",
            value=f"{forecast['temperature_celsius']}°C",
            inline=False,
        )

        # 將 Embed 加入串列
        embeds.append(embed)

    # 回傳所有預報 Embed
    return embeds
async def get_channel_history(channel, bot_user, limit=15, before=None):
    """讀取 Discord 頻道中的舊訊息，整理成 OpenAI 可以使用的 messages。"""
    old_messages = []
    history_messages = []
    # Discord API 讀頻道訊息時，預設會先拿較新的訊息。
    # 這裡先明確抓「最近的幾則」，把「抓資料」和「排成對話順序」分成兩步。
    # oldest_first=False 代表先拿最接近 before 的新訊息。
    # 下面再反轉成「舊到新」交給 AI，比較像大家平常閱讀對話的順序。
    async for old_message in channel.history(
        limit=limit,
        before=before,
        oldest_first=False,
    ):
        old_messages.append(old_message)

    # Discord 抓回來的是「新到舊」，但 AI 閱讀對話時需要「舊到新」。
    for old_message in reversed(old_messages):
        # 這裡使用 message.content，而不是 clean_content。
        # message.content 會保留 <@使用者ID> 這種真正的 mention 格式。
        content = old_message.content.strip()
        if not content:
            continue  # 空白訊息不用交給 AI，避免浪費上下文空間

        if old_message.author.id == bot_user.id:
            # 機器人自己以前說過的話，用 assistant 角色放回歷史中。
            history_messages.append({"role": "assistant", "content": content})
        else:
            # 其他同學和其他 bot 都標上名字，AI 才知道是誰說的。
            speaker_type = "機器人" if old_message.author.bot else "同學"
            speaker_mention = old_message.author.mention
            user_content = (
                f"{old_message.author.display_name}"
                f"（{speaker_type}，mention：{speaker_mention}）說：{content}"
            )
            history_messages.append({"role": "user", "content": user_content})

    return history_messages
async def ask_with_discord_history(message):
    """當機器人被提到時，先取得頻道歷史訊息，然後再呼叫 AI。"""
    history_messages = await get_channel_history(
        channel=message.channel,
        bot_user=bot.user,
        limit=CHANNEL_HISTORY_LIMIT,
        before=message,
    )
    user_question=message.content.replace(f"<@{bot.user.id}>", "").strip()
    if not user_question:
        user_question ="請根據的頻道對話,接著回答大家。"
    user_message=(f"{message.author.display_name}"
    f"(mention：{message.author.mention}）提到你：{user_question}"
    )
    return ai_assistant.ask(
        system_prompt=CHAT_SYSTEM_PROMPT,
        user_prompt=user_message,
        history_messages=history_messages,
        temperature=0.5,
    )
    
# Bot 成功登入 Discord 後執行
@bot.event
async def on_ready():
    # 顯示登入成功訊息
    print(f"({bot.user}) 已登入！")

    # 同步 Slash Commands 到 Discord
    await tree.sync()


# 當頻道收到新訊息時執行
@bot.event
async def on_message(message):
    # 如果是 Bot 自己發送的訊息則忽略
    # 避免一直回覆自己形成無限迴圈
    if message.author == bot.user:
        return

    # 如果收到 hello
    if message.content == "hello":
        # 回覆你好
        await message.channel.send("你好！")
    elif bot.user in message.mentions:
        async with message.channel.typing():
            answer, error = await ask_with_discord_history(message)
        if error:
            await message.channel.send(error)
        else:
            await message.reply(
                answer,
                mention_author=True,
                allowed_mentions=AI_REPLY_ALLOWED_MENTIONS,
            )

# 建立 /hello Slash Command
@tree.command(name="hello", description="say hello to the bot")
async def hello(interaction: discord.Interaction):
    # interaction：Slash Command 的互動物件

    # 回覆使用者
    await interaction.response.send_message("你好！")


# 建立 /weather Slash Command
# city_str：查詢城市
# forecast：是否查詢天氣預報
# ai：是否使用 AI 分析預報內容
@tree.command(name="weather", description="get weather info")
async def weather(
    interaction: discord.Interaction,
    city_str: str,
    forecast: bool = False,
    ai: bool = False,
):
    # 先延後回應，避免 API 查詢超時
    await interaction.response.defer()

    # 去除城市名稱前後空白
    city = city_str.strip()

    # 檢查是否有 OpenWeatherMap API Key
    if not weather_api.api_key:
        await interaction.followup.send("請先設定 OpenWeatherMap API 金鑰！")
        return

    try:
        # 如果查詢目前天氣
        if not forecast:
            # 呼叫 API 取得目前天氣摘要
            weather_summary = weather_api.get_weather_summary(city)

            # 查無城市
            if weather_summary is None:
                await interaction.followup.send("找不到該城市的天氣資訊！")
                return

            # 建立目前天氣 Embed
            embed = build_embed(weather_summary)

            # 傳送 Embed
            await interaction.followup.send(embed=embed)
            return

        # 如果查詢預報但不使用 AI 分析
        if not ai:
            # 取得天氣預報摘要
            forecast_summary = weather_api.get_forecast_summary(city)

            # 查無城市
            if forecast_summary is None:
                await interaction.followup.send("找不到該城市的天氣預報！")
                return

            # 建立多個預報 Embed
            embeds = build_forecast_embeds(forecast_summary)

            # Discord 一次最多顯示 10 個 Embed
            await interaction.followup.send(embeds=embeds[:10])
            return

        # 如果需要 AI 分析
        # 取得完整的天氣預報 JSON 資料
        raw_forecast = weather_api.get_forecast(city)

    # 捕捉 API 或資料格式錯誤
    except (requests.RequestException, ValueError):
        # 回覆錯誤訊息
        await interaction.followup.send("查詢天氣資訊失敗！")
        return

    # 將完整預報資料交給 AI 分析
    analysis, error = ai_assistant.ask(
        # System Prompt：設定 AI 身分與任務
        system_prompt="你是一個天氣分析師，請根據以下的天氣預報資料，提供一個簡短的分析，包含天氣趨勢、可能的降雨情況、溫度變化等。請以中文回答。",

        # User Prompt：提供要分析的資料
        user_prompt=f"以下是{city}的未來天氣資料，請分析以下天氣預報資料：\n{raw_forecast}",
    )
    if error:
        await interaction.followup.send(error)
    else:
        await interaction.followup.send(f"**的天氣分析:\n{analysis}")

def main():
    # 主程式入口

    # 使用 .env 中的 Discord Bot Token 啟動 Bot
    bot.run(os.getenv("DC_BOT_TOKEN"))


# 如果此檔案直接執行
if __name__ == "__main__":
    # 執行主程式
    main()
