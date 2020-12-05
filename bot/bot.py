import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', description="The bot for all your BeamMP needs.", help_command = None, case_insensitive = True)

print("Bot is starting...")

@bot.event
async def on_ready():
    print('\n\nLogged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------------')

#########################################COMMANDS#####################################################################

@bot.command(name="help", description = "Learn What each command does.") #help command
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


@bot.command(name = "save", description = "Can be run by admins only.\n\nThis command sets the server that can be reached by doing the `!check` command\n\n**Impemetation:**\n`!save <ip>:<port>")
@commands.has_permissions(administrator=True)
async def save(ctx, server_ip, server_port):
    save_embed = discord.Embed(title="Server Save:", color = 0x8a3f0a)

    if 1 == 0: #must add implemetation
        save_embed.add_field(name='success!', value="The discord's BeamMP server has been set to:\n{server_ip}:{server_port}")
    else:
        save_embed.add_field(name='ERROR', value="Please enter a valid ip and port\n`!save <ip>:<port>`")

    await ctx.send(embed=save_embed)


######################################################################################################################


bot.run(TOKEN)