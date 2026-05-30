#######################模組#######################
import requests
import asyncio
import discord
import os
from dotenv import load_dotenv
from myfunction.myfuncction import weatherAPI

#######################初始化#######################
load_dotenv()

asyncio.set_event_loop(asyncio.new_event_loop())

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(bot)


weather_api = weatherAPI(os.getenv("WEATHER_API_KEY"))


def build_embed(weather_summary):
    embed = discord.Embed(
        title=f"{weather_summary['city_name']}",
        description=f"{weather_summary['description']}",
        color=discord.Color.from_str("#0E90FF"),
    )

    icon_url = weather_api.get_icon_url(weather_summary["icon_code"])
    embed.set_thumbnail(url=icon_url)

    embed.add_field(
        name="溫度",
        value=f"{weather_summary['temperature']}°C",
        inline=False,
    )

    return embed


#######################事件#######################
@bot.event
async def on_ready():
    print(f"({bot.user}) 已登入！")
    await tree.sync()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "hello":
        await message.channel.send("你好！")


#######################指令#######################
@tree.command(name="hello", description="say hello to the bot")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("你好！")
@tree.command(name="weather", description="get weather info")
async def weather(interaction: discord.Interaction, city_str):
    await interaction.response.defer()

city=city.strip()

if not weather_api.api_key:
    await interaction.response.send_message("請先設定 OpenWeatherMap API 金鑰！")
    return
#######################啟動#######################
   def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()
