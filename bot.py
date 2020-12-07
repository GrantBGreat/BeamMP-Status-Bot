import os
import random
import discord
import sqlite3

from discord.ext import commands
from dotenv import load_dotenv
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', description="The bot for all your BeamMP needs.", help_command = None, case_insensitive = True)

print("Bot is starting...")





@bot.event
async def on_ready():
    conn = sqlite3.connect("main.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS main (
            guild_id integer,
            owner_id integer,
            prefix text
        )''')

    conn.commit()

    conn.close()


    print('\n\nLogged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------------')

#########################################COMMANDS#####################################################################

@bot.command(name="help", description = "Learn what each command does.", pass_context=True) #help command
@commands.cooldown(1, 5, commands.BucketType.guild)
async def help(ctx, args=None):
    help_embed = discord.Embed(title="BeamMP Status Commands:", color = 0x8a3f0a)
    command_names_list = [i.name for i in bot.commands]

    # If there are no arguments, just list the commands:
    if not args:
        help_embed.add_field(
            name="List of supported commands:",
            value="\n".join([i.name for i in bot.commands]),
            inline=False
        )
        help_embed.add_field(
            name="Details",
            value="Type `!help <command name>` for more details about a command.",
            inline=False
        )

    # If is a valid command:
    elif args in command_names_list:
        help_embed.add_field(
            name=args,
            value=bot.get_command(args).description
        )

    # If else:
    else:
        help_embed.add_field(
            name="ERROR",
            value="That is not a valid command!"
        )

    await ctx.send(embed=help_embed)




@bot.command(name = "save", description = "Can be run by admins only.\n\nThis command sets the server that can be reached by doing the `!check` command\n\n**Impemetations:**\n`!save server <user>`\n`!save prefix <prefix>`", pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.guild)
@has_permissions(administrator=True)
async def save(ctx, change=None, val=None):
    save_embed = discord.Embed(title="Settings:", color = 0x8a3f0a)
    if change == "server":
        if 1 == 0: #must add implemetation
            save_embed.add_field(name='Success!', value=f"The discord's BeamMP server has been set to:\n{val}")
        else:
            save_embed.add_field(name='ERROR', value="Please enter a valid user\n`!save server <user>`\n\nExample:\n`!save server dummy#1234`")
    elif change == "prefix":
        return #must add implemetation
    else:
        save_embed.add_field(name='ERROR', value="Please enter a valid syntax\n`!save <type>...`")

    await ctx.send(embed=save_embed)


########################################CATCH-ERRORS##################################################################


@save.error
async def save_error(ctx, error):
    if isinstance(error, MissingPermissions):
        error_embed = discord.Embed(title="Settings:", color = 0x8a3f0a)
        error_embed.add_field(name='No perms', value="Sorry {}, you do not have permissions to do that!".format(ctx.message.author))
        await ctx.send(embed=error_embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        error_embed = discord.Embed(title="ERROR", color = 0x8a3f0a)
        error_embed.add_field(name='Command on Cooldown:', value="Please retry in %s seconds" % int(error.retry_after))
        await ctx.send(embed=error_embed)

bot.run(TOKEN)