import discord, asyncio
from discord.ext import commands
import praw
import random
import datetime
import asyncio

client = commands.Bot(command_prefix='/')
    
@client.command(description="Sends a meme.")
async def meme(ctx):
    reddit = praw.Reddit(client_id='k2jNQuxn7ZSLRw',
    client_secret='eCbP5Xg8NMlZBjLR5xHVK76WXkhv5g',
    user_agent='New Brain')
    
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 100)
    for _ in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)

    await ctx.send(submission.url)
    
 

@client.command(name='purge', description="Purges the given number of messages.")
@commands.has_permissions(administrator=True)
async def purge(ctx, amount, arg:str=None):
    await ctx.message.delete()
    await ctx.channel.purge(limit=int(amount))
    message_to_delete = await ctx.send(f'{amount} messages have been deleted!')
    await asyncio.sleep(1)
    await message_to_delete.delete()

@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    
    if member == None or member == ctx.message.author:
        embed = discord.Embed(title = "**YOU CANNOT MUTE YOURSELF!**", color = 0x00ffff)
        await ctx.send(embed=embed)
        await ctx.message.delete()
        return
    
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
    embed = discord.Embed(title="Muted", description=f"{member.mention} was Muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" You have been muted from: **{guild.name}** | reason: **{reason}**")

@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   guild = ctx.guild
   await member.remove_roles(mutedRole)
   await member.send(f" You have been unmuted from: **{guild.name}**")
   embed = discord.Embed(title="Unmute", description=f" Unmuted: {member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)

@client.command()
async def tempmute(ctx, member: discord.Member, time: int, d, *, reason=None):
    guild = ctx.guild

    for role in guild.roles:
        if role.name == "Muted":
            await member.add_roles(role)

            if member == None or member == ctx.message.author:
                embed = discord.Embed(title = "**YOU CANNOT MUTE YOURSELF!**", color = 0x00ffff)
                await ctx.send(embed=embed)
                await ctx.message.delete()
                return

            embed = discord.Embed(title="muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.light_gray())
            embed.add_field(name="reason:", value=reason, inline=False)
            embed.add_field(name="time left for the mute:", value=f"{time}{d}", inline=False)
            await ctx.send(embed=embed)

            if d == "s":
                await asyncio.sleep(time)

            if d == "m":
                await asyncio.sleep(time*60)

            if d == "h":
                await asyncio.sleep(time*60*60)

            if d == "d":
                await asyncio.sleep(time*60*60*24)

            await member.remove_roles(role)

            embed = discord.Embed(title="Unmute ", description=f"unmuted: {member.mention} ", colour=discord.Colour.light_gray())
            await ctx.send(embed=embed)

            return

@client.command(description="Bans a specific user.", aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason=None):
     
    if member == None or member == ctx.message.author:
        embed = discord.Embed(title = "**YOU CANNOT BAN YOURSELF!**", color = 0x00ffff)
        await ctx.send(embed=embed)
        await ctx.message.delete()
        return
     
    embed = discord.Embed(title="Ban", description=f"{member.mention} was Banned", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.ban(reason=reason)

@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        embed = discord.Embed(title = "**YOU DONT HAVE THE PERMISSION TO DO THAT!**", color = 0x00ffff)
        await ctx.send(embed=embed)
        await ctx.message.delete()

@client.command(aliases=['k'])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason=None):
     
    if member == None or member == ctx.message.author:
        embed = discord.Embed(title = "**YOU CANNOT KICK YOURSELF!**", color = 0x00ffff)
        await ctx.send(embed=embed)
        await ctx.message.delete()
        return
     
    embed = discord.Embed(title="Kick", description=f"{member.mention} was kicked", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.kick(reason=reason)

@client.command(name='avatar', aliases=['av'], description="View avatar of a specific user.")
async def av_cmd(ctx, user: discord.Member):
    embed = discord.Embed(
        color=0xffff,
        title=f"{user}"
    )
    embed.set_image(url=f"{user.avatar_url}")
    await ctx.send(embed=embed)

@av_cmd.error
async def av_error(ctx, error):
    if isinstance (error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            color=0xffff,
            title=f"{ctx.author}" 
        )
    embed.set_image(url=f"{ctx.author.avatar_url}")
    await ctx.send(embed=embed)

@client.command(name='serverinfo', aliases=['ServerInfo'])
async def si_cmd(ctx):
    embed = discord.Embed(
        color=0xffff,
        title=f"{ctx.guild.name}"
    )
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    embed.add_field(name='Region', value=f"`{ctx.guild.region}`")
    embed.add_field(name='Member Count', value=f"{ctx.guild.member_count}")
    embed.set_footer(icon_url=f"{ctx.guild.icon_url}", text=f"Guild ID: {ctx.guild.id}")
    await ctx.send(embed=embed)

@client.command(description="Warns the specified user.")
@commands.has_permissions(administrator=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    
    if member == None or member == ctx.message.author:
        embed = discord.Embed(title = "**YOU CANNOT WARN YOURSELF!**", color = 0x00ffff)
        await ctx.send(embed=embed)
        await ctx.message.delete()
        return
    
    guild = ctx.guild

    embed = discord.Embed(title="Warn", description=f"{member.mention} was Warned ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.send(f" You have been warned from: **{guild.name}** | reason: **{reason}**")

@client.command(description="Says what you say.")
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(f"{message}" .format(message))

@client.event
async def on_message(message):

    if message.content.startswith("hello"):
        await message.channel.send("Bye.")
    
    await client.process_commands(message)

def convert(time):
    pos = ["s","m","h","d"]

    time_dict    = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

@client.command(description="Hosts a giveaway!", aliases = ['giveaway'])
@commands.has_permissions(administrator=True)
async def gstart(ctx):
    await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds")

    questions = ["Which channel should it be hosted in?",
                "What should be the duration of the giveaway? (s|m|h|d)",
                "What is the prize of the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return
    prize = answers[2]

    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")
    
    embed = discord.Embed(title = "Giveaway! 🎉", color = 0x00FFFF)
    embed.add_field(name= 'Time left to end:', value= answers[1], inline=False)
    embed.add_field(name= 'Prize:', value= prize, inline=False)
    embed.add_field(name = "Hosted By:", value = ctx.author.mention)
    embed.set_footer(text = f"Ends {answers[1]} minutes from now!")

    my_msg = await ctx.send(embed = embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(time)

    new_msg = await ctx.channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)


    await ctx.send(f"Congratulations! {winner.mention} won {prize}!")

@client.command(description="rerolls the giveaway giving you a new winner!", aliases = ['reroll'])
@commands.has_permissions(administrator=True)
async def groll(ctx, channel : discord.TextChannel, id_ : int):
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was entered incorrectly.")
        return

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! The new winner is {winner.mention}!")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Hello There!'))

@client.command(name='8ball', description='Let the 8 Ball Predict!\n')
async def _8ball(ctx, *, question):
    responses = ['As I see it, yes.',
             'Yes.',
             'Positive',
             'From my point of view, yes',
             'Convinced.',
             'Most Likley.',
             'Chances High',
             'No.',
             'Negative.',
             'Not Convinced.',
             'Perhaps.',
             'Not Sure',
             'May be',
             'I cannot predict now.',
             'Im to lazy to predict.',
             'I am tired. *proceeds with sleeping*',
             'It is certain',
             'It is decidedly so.',
             'Without a doubt.',
             'Yes - definately',
             'You may rely on it.',
             'As i see it, Yes.',
             'Outlook good',
             'Signs point to yes',
             'Reply hazy, try again',
             'Better not to tell you now',
             'Concentrate and ask again',
             'Don\'t count on it',
             'My reply is no',
             'My sources say no.',
             'Outlook not so good.',
             'Very doubtfull']
    response = random.choice(responses)
    embed=discord.Embed(title="The Magic 8 Ball has Spoken!", color = 0x00FFFF)
    embed.add_field(name='Question: ', value=f'{question}', inline=True)
    embed.add_field(name='Answer: ', value=f'{response}', inline=False)
    embed.set_footer(text="Requested by {}".format(ctx.message.author.name))
    await ctx.send(embed=embed)

@client.command(description="Tells how cool are you!")
@commands.has_permissions(send_messages=True)
async def coolmetre(ctx):
    values = ['1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '11',
            '12',
            '13',
            '14',
            '15',
            '16',
            '17',
            '18',
            '19',
            '20',
            '21',
            '22',
            '23',
            '24',
            '25',
            '26',
            '27',
            '28',
            '29',
            '30',
            '31',
            '32',
            '33',
            '34',
            '35',
            '36',
            '37',
            '38',
            '39',
            '40',
            '41',
            '42',
            '43',
            '44',
            '45',
            '46',
            '47',
            '48',
            '49',
            '50',
            '51',
            '52',
            '53',
            '54',
            '55',
            '56',
            '57',
            '58',
            '59',
            '60',
            '61',
            '62',
            '63',
            '64',
            '65',
            '66',
            '67',
            '68',
            '69',
            '70',
            '71',
            '72',
            '73',
            '74',
            '75',
            '76',
            '77',
            '78',
            '79',
            '80',
            '81',
            '82',
            '83',
            '84',
            '85',
            '86',
            '87',
            '88',
            '89',
            '90',
            '91',
            '92',
            '93',
            '94',
            '95',
            '96',
            '97',
            '98',
            '99',
            '100',
            '500']
    value = random.choice(values)
    embed=discord.Embed(title=f"{ctx.message.author.name}'s Cool Metre: {value}%", color = 0x00FFFF)
    embed.set_footer(text="Requested by {}".format(ctx.message.author.name))
    await ctx.send(embed=embed)
    
client.remove_command("help")

@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title = "New Brain Bot help", color = 0x00FFFF) 
    embed.add_field(name = "Moderation", value = "/ban - ban a player. \n/unban - Unban a player. \n/kick - Kick a player.\n/mute - Mute a player.\n/unmute - unmutes a player.\n/purge - Clears the chat.\n/tempmute - tempmutes a player", inline=False)
    embed.add_field(name = "Actions", value = "/punch - Punch a player.\n/wave - Wave at a player.\n/avatar - Shows the avatar of player\n/thank - Thanks a player", inline=False)
    embed.add_field(name = "Memes", value = "/meme - Meme from r/memes.\n/cats - Cat from r/catpictures\n/dogs - Dog from r/dogpictures\n/coolmetre - How cool are you.", inline=False)
    embed.add_field(name = "Fun", value = "/joke - Tells a joke.\n/roll - Rolls a six sided dice.\n/coinflip - Flips a coin.\n/wyr - Would you rather?\n/8ball - A simple 8ball.\n /giveway - Start a giveaway!", inline=False)
    embed.add_field(name = "Misc", value = "/ping - Displays the ping.\n/say - Make me talk.\n/credits - The credits.\n/stats - User stats\n/invite - Invite the bot.\n/vote - Support me!\n/bug - Report a bug", inline=False)
    embed.set_footer(text="Requested by {}".format(ctx.message.author.name))
    await ctx.send(embed = embed)

@client.command(name='punch', aliases=['p'], description="Punch a player.")
async def punch(ctx, user: discord.Member):
    embed = discord.Embed(
        color=0xffff,
        title=f"**Punched {user} 👊**"
        )
    embed.set_thumbnail(url=f"{user.avatar_url}")
    await ctx.send(embed=embed)

@client.command(name='Wave', aliases=['wave'], description="Wave at a player.")
async def wave(ctx, user: discord.Member):
    embed = discord.Embed(
        color=0xffff,
        title=f"**You waved to {user} 👋**"
        )
    embed.set_thumbnail(url=f"{user.avatar_url}")
    await ctx.send(embed=embed)

@client.command(name='Thank', aliases=['thanks', 'thank'], description="thank at a player.")
async def thank(ctx, user: discord.Member):
    embed = discord.Embed(
        color=0xffff,
        title=f"**You thanked {user} 🙏**"
        )
    embed.set_thumbnail(url=f"{user.avatar_url}")
    await ctx.send(embed=embed)

@client.command(name='Credits', aliases = ['credit', 'credits'], description="Shows who made me.")
async def credits(ctx):
    embed = discord.Embed(
        color=0xffff,
        title=f"**Developer: MOLECULE**"
        )
    embed.set_footer(text="Requested by {}".format(ctx.message.author.name))
    await ctx.send(embed=embed)

@client.command(name='Ping' , aliases=['ping'])
async def ping(ctx):
    pings = ['1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '11',
            '12',
            '13',
            '14',
            '15',
            '16',
            '17',
            '18',
            '19',
            '20',
            '21',
            '22',
            '23',
            '24',
            '25',
            '26',
            '27',
            '28',
            '29',
            '30',
            '31',
            '32',
            '33',
            '34',
            '35',
            '36',
            '37',
            '38',
            '39',
            '40',
            '41',
            '42',
            '43',
            '44',
            '45',
            '46',
            '47',
            '48',
            '49',
            '50',
            '51',
            '52',
            '53',
            '54',
            '55',
            '56',
            '57',
            '58',
            '59',
            '60',
            '61',
            '62',
            '63',
            '64',
            '65',
            '66',
            '67',
            '68',
            '69',
            '70',
            '71',
            '72',
            '73',
            '74',
            '75',
            '76',
            '77',
            '78',
            '79',
            '80',
            '81',
            '82',
            '83',
            '84',
            '85',
            '86',
            '87',
            '88',
            '89',
            '90',
            '91',
            '92',
            '93',
            '94',
            '95',
            '96',
            '97',
            '98',
            '99']
    value = random.choice(pings)

    embed = discord.Embed( color=0x00FFFF, title=f"Ping: **{value}ms**")
    await ctx.send(embed=embed)

@client.command(name='Roll', aliases = ['roll'])
async def roll(ctx):
    roll = ['1',
            '2',
            '3',
            '4',
            '5',
            '6']

    value = random.choice(roll)

    embed = discord.Embed(
        color=0xffff,
        title=f"You Rolled: **{value}** 🎲"
        )
    embed.set_footer(text="Requested by {}".format(ctx.message.author.name))
    await ctx.send(embed=embed)

@client.command(name='Coinflip', aliases = ['coinflip'])
async def coinflip(ctx):
    coinflip = ['Tails',
                'Heads']

    value = random.choice(coinflip)
    embed = discord.Embed(
        color=0xffff,
        title=f"**You flipped: {value}!**"
        )
    embed.set_footer(text="Requested by {}".format(ctx.message.author.name))
    await ctx.send(embed=embed)



client.run('ODMyNTAwMDczODMzMDM3ODQ1.YHksHA.3HNsElqA9kETlhSpOLiGsrm7lsk')