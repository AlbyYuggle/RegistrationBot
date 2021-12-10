import discord
from discord.ext import commands

attendance = {}
joinedlist = []
leftlist = []
signin = []
serverid = 743550548871217172

checkattend = False


client = commands.Bot(command_prefix = '!')
token = 'NzUwODczNTQwOTg2Nzk4MjIw.X1A3eg.NXVmeCMxDNszpju8TqsLk586hL0'

@client.event
async def on_ready():
    print('Bot is ready to go!')

@client.event
async def on_member_remove(member):
    global attendance
    global joinedlist
    global leftlist
    global checkattend
    leftlist.append(member.nick)

@client.event
async def on_member_join(member):
    global attendance
    global joinedlist
    global leftlist
    global checkattend
    num = client.get_guild(serverid)
    welcome = client.get_channel(750879622593380382)
    await welcome.send(f"Welcome to Absolute Coding, {member.mention}!")
    await welcome.send(f"Please tell us your full name and grade, {member.mention}. (Format: Firstname Lastname Grade): Example: Albert Xiao 12")
    author = member.name
    def check(m):
        arr = m.content.split(" ")
        try:
            if not (int(arr[-1]) >= 9 and int(arr[-1]) <= 12):
                return False
        except:
            return False    
        return len(arr) == 3 and author == m.author.name
        
        
    msg = await client.wait_for('message', check=check)
    arr = msg.content.split(" ")
    arr[0] = arr[0].capitalize()
    arr[1] = arr[1].capitalize()
    nick = arr[0] + " " + arr[1] + " - \'" + str(33 - int(arr[2]))
    attendance[nick] = 0
    await member.edit(nick=nick)
    await member.add_roles(num.get_role(750883472528113716))
    joinedlist.append(nick)
    await welcome.send("Membership processed. Thank you! Don't forget to sign up for the mailing list!")

@client.event
async def on_message(message):
    global attendance
    global joinedlist
    global leftlist
    global checkattend
    global signin
    welcome = client.get_channel(750879622593380382)
    att = client.get_channel(750833068679364659)
    bot = client.get_channel(750926513087709224)
    idnum = client.get_guild(serverid)
    message.content.lower()
    valid = ["bottesting", "planning"]
    validrole = ["Officer", "Junior Officer", "Ambassador"]
    if '!here' == message.content and checkattend and message.channel.name == "attendance" and message.author.nick not in signin:
        await message.channel.send('Checked in! Thanks!')
        if not message.author.nick in attendance:
            attendance[message.author.nick] = 1
            signin.append(message.author.nick)
        else:
            attendance[message.author.nick] = attendance[message.author.nick] + 1
            signin.append(message.author.nick) 
        
    elif '!count' == message.content and message.channel.name in valid:
        await message.channel.send(f'Number of members: {idnum.member_count}')

    elif '!startattend' == message.content and message.author.roles[1].name in validrole:
        await att.send("<@&750883472528113716> Attendance is open. Please check in by sending !here.")       
        checkattend = True
        signin = []
        
        
    elif '!endattend' == message.content and message.author.roles[1].name in validrole:
        checkattend = False
        await att.send("<@&750883472528113716> Attendance is now closed")
        
    elif '!att' == message.content and message.author.roles[1].name in validrole:
        await bot.send(str(attendance))
        
    elif '!joined' == message.content and message.author.roles[1].name in validrole:
        await bot.send(joinedlist)
        
    elif '!left' == message.content and message.author.roles[1].name in validrole:
        await bot.send(leftlist)
       
        
client.run(token)
