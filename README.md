# BeamMP Status Bot
A bot for all your BeamMP needs!

This is an open source bot developed in discord.py
 
Disclaimer:

This bot was developed to aid in checking the status of BeamMP servers. However, it is not at all related to the BeamMP game or any of its developers. Instead, it is open source and run by discord user GrantBGreat#1165 to allow easier communication with BeamMP servers from discord.

For more help & update announcements, [join the discord](https://discord.gg/dX34pgyHzp)!

![Discord Banner 2](https://discordapp.com/api/guilds/789657841895735337/widget.png?style=banner2)

# About the bot:

The BeamMP Status Bot allows the admin of a discord server to do a `b! save <discord user>` command to save a discord user to the bots database. After this setup is done, any member of the discord server will be able to run the `b! check` command to check the status of all servers owned by the saved user. Any member of a discord server can also do `b! status <discord user>` to get the status of servers owned by that user.

**Command List:**
```
help - shows the list of commands and their usage.

status <user> - inputs a discord user to get the information about servers owned by them.

support - sends a link to the support server.

invite - sends a link to invite the bot.

save <type> - A command that can only be run by server administrators where the type can be 'server' to save a server owner for the 'b! check' command or 'info' to get the current settings for the guild.

check - like the 'b! status' command, but returns the information for servers owned by the set user for the guild.

botstats - Checks the uptime & number of commands run for the bot.

beamstats - Show the stats for BeamMP servers as a whole.
```

**Format of output information:** *this is subject to change*
```
Server name
Mod count
Players (if is less than 5 then it states the player names, if is greater than 4 then it states the count)
```

**Screenshot Examples:**

![Output with over 4 people online](https://github.com/GrantBGreat/BeamMP-Status-Bot/blob/main/Screenshots/over4.JPG?raw=true "Output with over 4 people online")
![Output with under 5 people online](https://github.com/GrantBGreat/BeamMP-Status-Bot/blob/main/Screenshots/under5.JPG?raw=true "Output with under 5 people online")

<br><br><br>
# TODO:
* more error handling
* up max player count on embed
* add ability to have args on `check` command
