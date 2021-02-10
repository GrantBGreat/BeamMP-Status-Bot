import os
import random
import discord
import sqlite3
import urllib.request
import json
from datetime import datetime
import time

from discord.ext import commands
from dotenv import load_dotenv
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=commands.when_mentioned_or("b! "), description="The bot for all your BeamMP needs.", help_command = None, case_insensitive = True)

print("Bot is starting...")


conn = sqlite3.connect("main.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS main (
        guild_id integer,
        owner_id integer,
        prefix text
    )''')

conn.commit()

start_time = datetime.now()
command_uses = 0

@bot.event
async def on_ready():

    # Set bot status:
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="b! help"))

    print('\n\nLogged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-------------------\n')

#########################################COMMANDS#####################################################################

@bot.command(name="help", description = "Learn what each command does.", pass_context=True) #help command
@commands.cooldown(1, 5, commands.BucketType.guild)
async def help(ctx, args=None):
    global command_uses
    command_uses += 1

    help_embed = discord.Embed(title="Stuck? Join the Support Server!", color = 0x8a3f0a, url='https://discord.gg/vhGhEsDyCf')
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
            value="The prefix for this bot is \"`b!`\" -- Remember the space between the prefix and command!\n\nType `b! help <command name>` for more details about a command.",
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




@bot.command(name = "save", description = "Can be run by admins only.\n\nThis command sets the server that can be reached by doing the `b! check` command.\n\n**Impemetations:**\n`b! save server <user>`\n`b! save info`", pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.guild)
@has_permissions(administrator=True)
async def save(ctx, change=None, val=None):
    global command_uses
    command_uses += 1

    # get guild in db
    gid = ctx.message.guild.id
    print(f"contacted guild {gid}:")
    c.execute("SELECT * FROM main WHERE guild_id=?", (gid,))
    if c.fetchone() is None:
        c.execute("INSERT INTO main (guild_id) VALUES (?)", (gid,))
        c.execute("SELECT * FROM main WHERE guild_id=?", (gid,))
        print(f"added guild {gid} to database")
    else:
        print(f"guild {gid} was found in db")



    save_embed = discord.Embed(title="Settings:", color = 0x8a3f0a)
    if change == "server":
        try:
            raw = val
            uid = (await commands.UserConverter().convert(ctx, val)).id
            save_embed.add_field(name='Success!', value=f"The BeamMP server owner for this guild has been set to:\n`{raw}`\nid: `{uid}`\n\nIf this is not the correct user then simply run the command again. Remember that users are caps sensitive.")

            # add uid to db:
            c.execute("UPDATE main SET owner_id = ? WHERE guild_id = ?", (uid, gid))
            print(f"Set server owner to {uid} for guild {gid}\n")

        except commands.UserNotFound:
            save_embed.add_field(name='ERROR', value="Please enter a valid user\n`b! save server <user>`\n\nExample:\n`b! save server dummy#1234`")


    elif change == "info":

        try:
            c.execute("SELECT * FROM main WHERE guild_id=?", (gid,))
            result = c.fetchone()
            content = f"Guild id: `{result[0]}`\n"
            print(f"Printing information into guild {gid}\n")
            

            # create embed:
            if result[1] is None:
                content += "id of BeamMP server owner: `Not Set`\n"
            else:
                content += f"id of BeamMP server owner: `{result[1]}`\n"
            
            save_embed.add_field(name='Information for this Guild:', value=content)
            

        except sqlite3.Error as error:
            print(f"Failed to read data from sqlite table for guild {gid}", error)
            save_embed.add_field(name='ERROR', value='There was a problem contatcting the database, if you are seeing this message then please notify GrantBGreat#1165 on discord via the support server.')


    else:
        save_embed.add_field(name='ERROR', value="Please enter a valid syntax\n`b! save <type>...`\n\nFor more info, do `b! help save`")
        print("No syntax was given.\n")
    
    conn.commit()
    await ctx.send(embed=save_embed)



@bot.command(name = "check", description = "Checks the status of the BeamMP server(s) set for this guild.", pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.guild)
async def check(ctx):
    global command_uses
    command_uses += 1
    await ctx.channel.trigger_typing()

    # get guild in db
    gid = ctx.message.guild.id
    print(f"contacted guild {gid}:")
    c.execute("SELECT * FROM main WHERE guild_id=?", (gid,))

    if c.fetchone() is None:
        c.execute("INSERT INTO main (guild_id) VALUES (?)", (gid,))
        conn.commit()
        c.execute("SELECT * FROM main WHERE guild_id=?", (gid,))
        print(f"added guild {gid} to database")
    else:
        print(f"guild {gid} was found in db")

    print("checking if a user has been set for the guild")
    c.execute("SELECT * FROM main WHERE guild_id=?", (gid,))
    result = c.fetchone()

    if result[1] is None:
        check_embed = discord.Embed(title="Server Status:", color = 0x8a3f0a)
        check_embed.add_field(name="ERROR", value="No Server has been set for this guild.\n\nTo set the server have an admin run the `b! save server` command.\nYou can also do the `b! status <user>` command to get the status of servers run by a user")
        await ctx.send(embed=check_embed)
        return
    else:
        oid = result[1]
        print(f"guild {gid} and server owner {oid} were found in the db")
    
    oid = result[1]

    username = await bot.fetch_user(oid)

    print(f"Finding servers for user {username} in {gid}")

    try:
        req = urllib.request.Request('https://beammp.com/servers-info')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        data = urllib.request.urlopen(req)
        result = data.read()
        result = result.decode('utf-8')
        dictionary = json.loads(result)
    except Exception as e:
        check_embed = discord.Embed(title="Server Status:", color = 0x8a3f0a)
        check_embed.add_field(name="ERROR", value="There was an error contacting BeamMP servers. This is most likely a problem on BeamMP's end.")
        await ctx.send(embed=check_embed)
        print(f"error contacting servers:\n{e}\n")
        return

    print(f"checking {len(dictionary)} servers...")
    print(f"Sending server information to {gid} for:")
    times = 0
    name = ''
    players = ''
    max_players = ''
    mods_total = ''
    player_list = ''
    try:
        for d in dictionary:
            for key, value in d.items():
                if isinstance(value, dict) and 'owner' in value and value['owner'] == str(username):
                    times += 1
                    raw_name = value['sname']
                    players = value['players']
                    max_players = value['maxplayers']
                    mods_total = value['modstotal']
                    raw_player_list = value['playerslist']
                    player_list = '\n'.join(list(raw_player_list.split(";")))

                    # remove name decorators:
                    name = ''.join([raw_name[i] for i in range(len(raw_name)) if raw_name[i] != '^' and (i == 0 or raw_name[i-1] != '^')])
                    print(name)

                    status_embed = discord.Embed(title="Server Status:", color = 0x8a3f0a)
                    if int(players) <= 4 and int(players) != 0:
                        print('using player names')
                        status_embed.add_field(name=f"Status of: {name}", value=f"\nMods: {mods_total}\nPlayers:\n{player_list}")
                    else:
                        print('using player count')
                        status_embed.add_field(name=f"Status of: {name}", value=f"\nMods: {mods_total}\nPlayers: {players} / {max_players}")
                    await ctx.send(embed=status_embed)
        print('\n')

    except Exception as e:
        print(f"ERROR: {e}\n")

    if times == 0:
        check_embed = discord.Embed(title="Server Status:", color = 0x8a3f0a)
        check_embed.add_field(name='ERROR', value='No online BeamMP servers could be found that are owned by the given user')
        await ctx.send(embed=check_embed)
        return



@bot.command(name = "status", description = "Checks the status of the BeamMP server(s) associated with the user provided.", pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.guild)
async def status(ctx, val=None):
    global command_uses
    command_uses += 1
    await ctx.channel.trigger_typing()

    gid = ctx.message.guild.id
    print(f"running status command in guild {gid}")

    print('checking if a user was provided...')
    if val is None:
        print("no user provided\n")
        status_embed = discord.Embed(title="Server Status:", color = 0x8a3f0a)
        status_embed.add_field(name='ERROR', value='No user specifyed.\nCorrect syntax: `b! status <user>`')
        await ctx.send(embed=status_embed)
        return

    print("Checking if user is valid...")
    username = ''
    try:
        username = (await commands.UserConverter().convert(ctx, val))
    except commands.UserNotFound:
        print("User not found error\n")
        status_embed = discord.Embed(title="Server Status:", color = 0x8a3f0a)
        status_embed.add_field(name='ERROR', value="Please enter a valid user\n`b! status <user>`\n\nExample:\n`b! status dummy#1234`\n\nRemember, users are capital sensitive!")
        await ctx.send(embed=status_embed)
        return

    print(f"Finding servers for user {username} in {gid}")

    try:
        req = urllib.request.Request('https://beammp.com/servers-info')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        data = urllib.request.urlopen(req)
        result = data.read()
        result = result.decode('utf-8')
        dictionary = json.loads(result)
    except Exception as e:
        status_embed = discord.Embed(title="Server Status:", color = 0x8a3f0a)
        status_embed.add_field(name="ERROR", value="There was an error contacting BeamMP servers. This is most likely a problem on BeamMP's end.")
        await ctx.send(embed=status_embed)
        print(f"error contacting servers:\n{e}\n")
        return

    print(f"checking {len(dictionary)} servers...")
    print(f"Sending server information to {gid} for:")
    times = 0
    name = ''
    players = ''
    max_players = ''
    mods_total = ''
    player_list = ''
    try:
        for d in dictionary:
            for key, value in d.items():
                if isinstance(value, dict) and 'owner' in value and value['owner'] == str(username):
                    times += 1
                    raw_name = value['sname']
                    players = value['players']
                    max_players = value['maxplayers']
                    mods_total = value['modstotal']
                    raw_player_list = value['playerslist']
                    player_list = '\n'.join(list(raw_player_list.split(";")))

                    # remove name decorators:
                    name = ''.join([raw_name[i] for i in range(len(raw_name)) if raw_name[i] != '^' and (i == 0 or raw_name[i-1] != '^')])
                    print(name)

                    status_embed = discord.Embed(title="Server Status:", color = 0x8a3f0a)
                    if int(players) <= 4 and int(players) != 0:
                        print('using player names')
                        status_embed.add_field(name=f"Status of: {name}", value=f"\nMods: {mods_total}\nPlayers:\n{player_list}")
                    else:
                        print('using player count')
                        status_embed.add_field(name=f"Status of: {name}", value=f"\nMods: {mods_total}\nPlayers: {players} / {max_players}")
                    await ctx.send(embed=status_embed)
        print('\n')

    except Exception as e:
        print(f"ERROR: {e}\n")

    if times == 0:
        status_embed = discord.Embed(title="Server Status:", color = 0x8a3f0a)
        status_embed.add_field(name='ERROR', value='No online BeamMP servers could be found that are owned by the given user')
        await ctx.send(embed=status_embed)
        return


@bot.command(name = "beamstats", description = "Show the stats for BeamMP servers as a whole.", pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.guild)
async def beamstats(ctx):
    global command_uses
    command_uses += 1
    await ctx.channel.trigger_typing()

    try:
        req = urllib.request.Request('https://beammp.com/servers-info')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        data = urllib.request.urlopen(req)
        result = data.read()
        result = result.decode('utf-8')
        dictionary = json.loads(result)
    except Exception as e:
        beamstats_embed = discord.Embed(title="Server Status:", color = 0x8a3f0a)
        beamstats_embed.add_field(name="ERROR", value="There was an error contacting BeamMP servers. This is most likely a problem on BeamMP's end.")
        await ctx.send(embed=beamstats_embed)
        print(f"error contacting servers:\n{e}\n")
        return

    beam_server_count = len(dictionary)
    player_count = 0
    mod_count = 0

    try:
        for d in dictionary:
            for key, value in d.items():
                if isinstance(value, dict):
                    players = value['players']
                    player_count += int(players)
                    mods_total = value['modstotal']
                    mod_count += int(mods_total)

    except Exception as e:
        print(f"ERROR in beamstats command: {e}\n")

    beamstats_embed = discord.Embed(title="BeamMP Server Stats:", color = 0x8a3f0a)
    beamstats_embed.add_field(name='Public Servers:', value=f'Server count: {beam_server_count}\nPlayer count: {player_count}\nMod count: {mod_count}', inline=False)
    beamstats_embed.add_field(name='All Servers:', value=f'The bot is currently only able to grab information about public BeamMP servers. To get informaiton on all servers visit the [stats page](https://beamng-mp.com/stats) on BeamMP\'s website.', inline=False)
    await ctx.send(embed=beamstats_embed)


@bot.command(name='support', description="Sends a link to the support server")
@commands.cooldown(1, 15, commands.BucketType.guild)
async def support(ctx):
    global command_uses
    command_uses += 1

    support_embed = discord.Embed(title="Join the Support Server!", color = 0x8a3f0a, url='https://discord.gg/vhGhEsDyCf') # link to support server
    await ctx.send(embed = support_embed)
    gid = ctx.message.guild.id
    print(f"Sent support server invite to guild {gid}\n")



@bot.command(name='invite', description="Sends a link to invite the bot")
@commands.cooldown(1, 15, commands.BucketType.guild)
async def invite(ctx):
    global command_uses
    command_uses += 1

    invite_embed = discord.Embed(title='Invite the bot!', color = 0x8a3f0a, url='https://discord.com/api/oauth2/authorize?client_id=784631695902375956&permissions=2048&scope=bot') # link to invite bot.
    await ctx.send(embed = invite_embed)
    gid = ctx.message.guild.id
    print(f"Sent bot invite to guild {gid}\n")



@bot.command(name = "botstats", description = "Checks the uptime & number of commands run for the bot.", pass_context=True)
@commands.cooldown(1, 10, commands.BucketType.guild)
async def botstats(ctx):
    global command_uses
    command_uses += 1

    # find uptime
    current_time = datetime.now()
    diff = current_time - start_time
    seconds = diff.total_seconds()
    intervals = (
        ('Days', 86400),    # 60 * 60 * 24
        ('Hours', 3600),    # 60 * 60
        ('Minutes', 60),
        ('Seconds', 1),
        )

    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(round(value), name))
    uptime = ', '.join(result)

    # create embed
    bot_embed = discord.Embed(name="BeamMP Status Bot", colour=0x8a3f0a)
    # add Uptime
    bot_embed.add_field(name="Uptime", value=uptime, inline=False)
    # add commands run
    bot_embed.add_field(name="Commands run", value=str(command_uses), inline=False)



    # send the embed:
    try:
        await ctx.send(embed=bot_embed)
    except discord.HTTPException:
        await ctx.send("Current uptime: " + text)


########################################CATCH-ERRORS##################################################################

@save.error
async def save_error(ctx, error):
    if isinstance(error, MissingPermissions):
        error_embed = discord.Embed(title="ERROR", color = 0x8a3f0a)
        error_embed.add_field(name='No permission', value="Sorry {}, you do not have permissions to do that!".format(ctx.message.author.name))
        await ctx.send(embed=error_embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        error_embed = discord.Embed(title="ERROR", color = 0x8a3f0a)
        error_embed.add_field(name='Command on Cooldown:', value="Please retry in %s seconds" % int(error.retry_after))
        await ctx.send(embed=error_embed)

bot.run(TOKEN)
