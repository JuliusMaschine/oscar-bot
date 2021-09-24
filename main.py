from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_NAME')
FFMPEG_OPTIONS = {'before_options': '''-reconnect 1 -reconnect_streamed 1
                  -reconnect_delay_max 5''', 'options': '-vn'}

bot = commands.Bot(command_prefix='-')
cogfolder = os.listdir('cogs')

py_extentions = [file for file in cogfolder if file.endswith('.py')]

if __name__ == '__main__':
    for file in py_extentions:
        file = "cogs." + file[:-3]
        bot.load_extension(file)

bot.run(TOKEN)
