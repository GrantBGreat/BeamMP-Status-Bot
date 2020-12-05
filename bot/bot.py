import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', description="The bot for all your BeamMP needs.", help_command = None)

@bot.command() #help command
async def help(ctx, args=None):
    help_embed = discord.Embed(title="BeamMP Status Commands:", color = 0x8a3f0a)
    command_names_list = [x.name for x in bot.commands]

    # If there are no arguments, just list the commands:
    if not args:
        help_embed.add_field(
            name="List of supported commands:",
            value="\n".join([x.name for x in bot.commands]),
            inline=False
        )
        help_embed.add_field(
            name="Details",
            value="Do `!help <command name>` for more details about a command.",
            inline=False
        )

    # If is a valic command:
    elif args in command_names_list:
        help_embed.add_field(
            name=args,
            value=bot.get_command(args).help
        )

    # If else:
    else:
        help_embed.add_field(
            name="Nope.",
            value="That is not a valid command!"
        )

    await ctx.send(embed=help_embed)


#@bot.command()
#def Set():
#    return

######################################################################################################################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------------')


bot.run(TOKEN)