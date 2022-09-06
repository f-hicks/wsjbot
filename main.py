from discord.ext import tasks
from discord import default_permissions
from discord.commands import Option
import discord
import os
from dotenv import load_dotenv
from datetime import datetime
import random
from events import events
import time


load_dotenv()

socials = {
    "instagram": "https://www.instagram.com/unit68wsj/",
    "TikTok": "https://www.tiktok.com/@unit68wsj",
    "Facebook": "https://www.facebook.com/Berkshire25WSJ/",
    "Website": "https://unit68.ml",
    "Youtube": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}


colours_ = [
    discord.Color.teal(),
    discord.Color.dark_teal(),
    discord.Color.green(),
    discord.Color.dark_green(),
    discord.Color.blue(),
    discord.Color.dark_blue(),
    discord.Color.purple(),
    discord.Color.dark_purple(),
    discord.Color.magenta(),
    discord.Color.dark_magenta(),
    discord.Color.gold(),
    discord.Color.dark_gold(),
    discord.Color.orange(),
    discord.Color.dark_orange(),
    discord.Color.red(),
    discord.Color.dark_red(),
    discord.Color.lighter_grey(),
    discord.Color.darker_grey(),
    discord.Color.light_grey(),
    discord.Color.dark_grey(),
    discord.Color.blurple(),
    discord.Color.greyple(),
    discord.Color.default()
]

def daysuntilkorea():
    now = datetime.now()
    korea=datetime(day=1,month=8,year=2023)
    return korea-now





colours = {"red": discord.Colour.red(),"green": discord.Colour.green(),"blue": discord.Colour.blue(),"purple": discord.Colour.purple(),"magenta": discord.Colour.magenta(),"gold": discord.Colour.gold(),"orange": discord.Colour.orange(),"teal": discord.Colour.teal(),"dark_teal": discord.Colour.dark_teal(),"dark_green": discord.Colour.dark_green(),"dark_blue": discord.Colour.dark_blue(),"dark_purple": discord.Colour.dark_purple(),"dark_magenta": discord.Colour.dark_magenta(),"dark_gold": discord.Colour.dark_gold(),"dark_orange": discord.Colour.dark_orange(),"dark_red": discord.Colour.dark_red(),"lighter_grey": discord.Colour.lighter_grey(),"darker_grey": discord.Colour.darker_grey(),"light_grey": discord.Colour.light_grey(),"dark_grey": discord.Colour.dark_grey(),"black": discord.Colour.default(),"white": discord.Colour.from_rgb(255,255,255),"default": discord.Colour.default(),"blurple": discord.Colour.blurple(),"greyple": discord.Colour.greyple(),}


bot = discord.Bot(debug_guilds=[])
discord.Intents.all()

class channelview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Private", style=discord.ButtonStyle.primary, custom_id="privatechannel")
    async def button_callback(self, button, interaction):
        channelname = f'{interaction.user.display_name}\'s question'
        channel = await interaction.guild.create_text_channel(name = channelname)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(bot.user, read_messages=True, send_messages=True)
        await channel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
        await interaction.response.send_message(f"Private channel created: <#{channel.id}>",ephemeral=True )
        await channel.send(view=questionchannel())

class questionchannel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="", style=discord.ButtonStyle.red, custom_id="closeprivatechannel")
    async def button_callback(self, button, interaction):
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Are you sure?",view=questionchannelconfirm(),ephemeral=True)


class questionchannelconfirm(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Confirm",style=discord.ButtonStyle.primary, custom_id="confirmdelete")
    async def button_callback(self, button, interaction):
        button.disabled = True
        button.style = discord.ButtonStyle.green
        await interaction.response.edit_message(view=self)
        await interaction.channel.delete()

class addeventconfirmdate(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="I understand",style=discord.ButtonStyle.primary, custom_id="addeventconfirmdate")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(addeventmodal(title="create an embed"))
        await interaction.delete_original_message()


class editevent_(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        global events

    
    @discord.ui.button(label="Edit",style=discord.ButtonStyle.primary, custom_id="editevent")
    async def editbutton_callback(self, button, interaction):
        await interaction.response.edit_message(view=editsevent_())
        #await interaction.delete_original_message()

    @discord.ui.button(label="Delete",style=discord.ButtonStyle.red, custom_id="deleteevent")
    async def deletebutton_callback(self, button, interaction):
        events.pop(editevents)
        #await interaction.delete_original_message()

class editeventname(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        global events
        
        self.add_item(discord.ui.InputText(label="please enter a title for the event", placeholder="title", custom_id="eventname"))
    async def callback(self, interaction: discord.Interaction):
        global events
        oldeventname = editevents
        neweventname = self.children[0].value
        keys = list(events.keys())
        index=keys.index(oldeventname)
        date = events[oldeventname]
        events.pop(oldeventname)
        events = insert(events,{neweventname:date},index)
        await interaction.response.edit_message(view=None)


class editsevent_(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        global events
    
    @discord.ui.button(label="Edit name",style=discord.ButtonStyle.primary, custom_id="editeventname")
    async def editbutton_callback(self, button, interaction):
        await interaction.response.send_modal(editeventname(title="edit the name of the event"))
        await interaction.delete_original_message()
    @discord.ui.button(label="Edit date",style=discord.ButtonStyle.primary, custom_id="editeventdate")
    async def editdatebutton_callback(self, button, interaction):
        pass

class editeventview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        global events
        
    options=[]
    now = datetime.now()
    for event in events:
        options.append(
            discord.SelectOption(
                label=event,
                description=f'{events[event]} | {(datetime.strptime(events[event], "%d %B, %Y")-now).days} days',

            )
        )

    @discord.ui.select(placeholder="Select event",options=options)
    async def select_callback(self, select, interaction):
        global editevents
        editevents = select.values[0]
        await interaction.response.edit_message(view=editevent_())


class createmessage(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label=" ", style=discord.ButtonStyle.primary, custom_id="add_embed_title_button")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(createmessagemodal(title="Modal via Button"))

class socialsview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
        for social in socials:
            socialbutton=discord.ui.Button(label=social,style=discord.ButtonStyle.link,url=socials[social])
            self.add_item(socialbutton)

    async def button_callback(self, button, interaction):
        await interaction.response.send_message(socials["instagram"])

class selectcolour(discord.ui.View):
    def __init__(self,embed):
        super().__init__(timeout=None)
    
    @discord.ui.select(placeholder="Select a colour", options = [
            discord.SelectOption(
                label="teal",
                value="discord.Color.teal",
                emoji="🟦"
            ),
            discord.SelectOption(
                label="dark teal",
                value="dark_teal",
                emoji="🟦"
            ),
            discord.SelectOption(
                label="green",
                value="green",
                emoji="🟩"
            ),
            discord.SelectOption(
                label="dark green",
                value="dark_green",
                emoji="🟩"
            ),
            discord.SelectOption(
                label="blue",
                value="blue",
                emoji="🟦"
            ),
            discord.SelectOption(
                label="dark blue",
                value="dark_blue",
                emoji="🟦"
            ),
            discord.SelectOption(
                label="purple",
                value="purple",
                emoji="🟪"
            ),
            discord.SelectOption(
                label="dark purple",
                value="dark_purple",
                emoji="🟪"
            ),
            discord.SelectOption(
                label="magenta",
                value="magenta",
                emoji="🟪"
            ),
            discord.SelectOption(
                label="dark magenta",
                value="dark_magenta",
                emoji="🟪"
            ),
            discord.SelectOption(
                label="gold",
                value="gold",
                emoji="🟨"
            ),
            discord.SelectOption(
                label="dark gold",
                value="dark_gold",
                emoji="🟨"
            ),
            discord.SelectOption(
                label="orange",
                value="orange",
                emoji="🟧"
            ),
            discord.SelectOption(
                label="dark orange",
                value="dark_orange",
                emoji="🟧"
            ),
            discord.SelectOption(
                label="red",
                value="red",
                emoji="🟥"
            ),
            discord.SelectOption(
                label="dark red",
                value="dark_red",
                emoji="🟥"
            ),
            discord.SelectOption(
                label="lighter gray",
                value="lighter_gray",
                emoji="⬜"
            ),
            discord.SelectOption(
                label="darker gray",
                value="darker_gray",
                emoji="⬛"
            ),
            discord.SelectOption(
                label="light gray",
                value="light_gray",
                emoji="⬜"
            ),
            discord.SelectOption(
                label="dark gray",
                value="dark_gray",
                emoji="⬛"
            ),
            discord.SelectOption(
                label="blurple",
                value="blurple",
                emoji="🟪"
            ),
            discord.SelectOption(
                label="greyple",
                value="greyple",
                emoji="🟪"
            ),
            discord.SelectOption(
                label="black",
                value="black",
                emoji="⬛"
            ),
            discord.SelectOption(
                label="white",
                value="white",
                emoji="⬜"
            ),
            discord.SelectOption(
                label="default",
                value="default",
                emoji="⬜"
            )

    ])
    async def select_callback(self, select, interaction):
        
        #embed = discord.Embed(title=f"{self.children[0].value} ",description=f"{self.children[1].value}",color=discord.Color[select.values[0]])
        embed = discord.Embed(title=title,description=description,color=colours[select.values[0]])
        select.disabled = True
        self.remove_item(select)
        await interaction.response.edit_message(embed=embed,view=channelview())

    
class createmessagemodal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.add_item(discord.ui.InputText(label="please enter a title for the embed"))
        self.add_item(discord.ui.InputText(label="please enter a description for the embed",style=discord.InputTextStyle.multiline))
    async def callback(self, interaction = discord.Interaction):
        embed = discord.Embed(title=f"{self.children[0].value}",description=f"{self.children[1].value}",color=random.choice(colours_))
        global title
        global description
        title = self.children[0].value
        description = self.children[1].value
        await interaction.response.send_message(view=selectcolour(embed))

class addeventmodal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        self.add_item(discord.ui.InputText(label="Please add the name of the event"))
        self.add_item(discord.ui.InputText(label="Please add the Date of the event"))
    async def callback(self, interaction = discord.Interaction):
        global events
        eventname = self.children[0].value
        date = self.children[1].value
        try:
            date_ = datetime.strptime(date, "%d %B, %Y")
        except Exception as e:
            #print(e)
            await interaction.response.send_message(f"{date} is not a valid date. Please use the format DD Month, YYYY. for example: 1 January, 2020",view=addeventconfirmdate())
        else:
            await interaction.response.send_message(f"{eventname}: {date}")
            for event in events:
                if datetime.strptime(events[event], "%d %B, %Y") < date_:
                    keys = list(events.keys())
                    index=keys.index(event)
                    if index == len(events)-1:
                        events = insert(events,{eventname:date},index+1)
                        with open("events.py","w") as f:
                            f.seek(0) 
                            f.truncate()
                            f.write(f"events = {events}")
                else:
                    keys = list(events.keys())
                    index=keys.index(event)
                    events = insert(events,{eventname:date},index)
                    with open("events.py","w") as f:
                            f.seek(0) 
                            f.truncate()
                            f.write(f"events = {events}")
                    break


insert = lambda _dict, obj, pos: {k: v for k, v in (list(_dict.items())[:pos] +
                                                    list(obj.items()) +
                                                    list(_dict.items())[pos:])}

presence = 0
@tasks.loop(hours=0.001)
async def changeactivity():
  global presence
  if presence == 0:
    presence = 1
    await bot.change_presence(activity=discord.Game(f'{daysuntilkorea().days} days until Jamboree'))
  else:
    now=datetime.now()
    await bot.change_presence(activity=discord.Game(f'Our next unit event is {list(events)[0]} on {events[list(events)[0]]} | {(datetime.strptime(events[list(events)[0]], "%d %B, %Y")-now).days} days'))
    presence = 0

@tasks.loop(hours=1)
async def hourly():
    global events
    now = datetime.now()
    for event in events:
        date = datetime.strptime(events[event], "%d %B, %Y")
        if date < now:
            events.pop(event)

@bot.event
async def on_ready():
    changeactivity.start()
    hourly.start()
    now = datetime.now()
    for event in events:
        date = datetime.strptime(events[event], "%d %B, %Y")
        if date < now:
            print(event)
            events.pop(event)
            

    print(f"{bot.user} is ready and online!")
    print(f'{daysuntilkorea().days} days until Jamboree')
    bot.add_view(channelview())
    bot.add_view(questionchannel())
    bot.add_view(questionchannelconfirm())
    bot.add_view(yutnoriplayer1view())

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def say_hello(ctx):
    await ctx.respond("Hey!")
    print(ctx.guild.emojis)


@bot.slash_command(name="createmessage", description = "create a message as the Bot",) # Create a slash command
@default_permissions(manage_messages=True)
async def create_message(ctx):
    await ctx.send_modal(createmessagemodal(title="create an embed")) # Send a message with our View class that contains the button

@bot.slash_command(name="addevent", description = "adds an events to the event list",) # Create a slash command
async def addevent(ctx):
    await ctx.send_modal(addeventmodal(title="add event"))

@bot.slash_command(name="editevent", description = "edits an events from the event list",) # Create a slash command
async def editevent(ctx):
    await ctx.respond(view=editeventview())

@bot.slash_command(name="daysuntiljamboree",description="whispers to you the days until the jamboree starts")
async def DaysUntilJamboree(ctx):
    await ctx.respond(f'There are {daysuntilkorea().days} days until the World Scout Jamboree',ephemeral=True)

@bot.slash_command(name="nextevent",description="whispers to you the next unit event")
async def nextevent(ctx):
    now = datetime.now()
    await ctx.respond(f'The next event is {list(events)[0]}. It is on {events[list(events)[0]]} which is in {(datetime.strptime(events[list(events)[0]], "%d %B, %Y")-now).days} days time.',ephemeral=True)

@bot.slash_command(name="events",description="all events")
async def nextevent(ctx):
    now = datetime.now()
    embed = discord.Embed(title="Events",description="",color=random.choice(colours_))
    for event in events:
        embed.add_field(name=event,value=f'{events[event]} | {(datetime.strptime(events[event], "%d %B, %Y")-now).days} days',inline=False)
    await ctx.respond(embed=embed,ephemeral=True)
    
@bot.slash_command(name="socials",description="gives you a list of all our official social medias")
async def socialscmd(ctx):
    embed = discord.Embed(title="Socials",description="",color=random.choice(colours_))
    for social in socials:
        embed.add_field(name=social,value=f'[{social}]({socials[social]})',inline=True)

    await ctx.respond(embed=embed,view=socialsview(),ephemeral=True)

############         Yut Nori game         ############
board = {
    10:"⚪","gap9":"    ",9:"◽","gap8":"    ",8:"◽","gap7":"    ",7:"◽","gap6":"    ",6:"◽","gap5":"    ",5:"⚪","return5":"\n",
    "gap10":"\n",
    11:"◽","gap22":"      ",10.1:"◽","gap22_":"                   ", 5.1:"◽","gap4":"      ",4:"◽","return4":"\n",
    "gap11":"\n",
    12:"◽","gap23":"            ",10.2:"◽","gap23_":"       ",5.2:"◽","gap21":"            ",3:"◽","return3":"\n",
    "gap12":"                        ",(5.3,10.2):"⚪","gap28":"                         ","return28":"\n",
    13:"◽","gap13":"            ",5.4:"◽","gap24":"       ",26:"◽","gap26":"            ",2:"◽","return2":"\n",
    "gap2":"\n",
    14:"◽","gap14":"      ",5.5:"◽","gap25":"                   ",27: "◽","gap27":"      ",1:"◽","return1":"\n",
    "gap1":"\n",
    15:"⚪","gap15":"    ",16:"◽","gap16":"    ",17:"◽","gap17":"    ",18:"◽","gap18":"    ",19:"◽","gap19":"    ",0:"⚪","startfinish":"<-- START/FINISH",None:'\n',
    "return6":"\n",
    "player1home":"🔵🔵🔵🔵","gap30":"    ","player2home":"🔴🔴🔴🔴","gap31":"                        ","player1finish":"","gap32":"    ","player2finish":""
}

def roll():
    stick1 = bool(random.getrandbits(1))
    stick2 = bool(random.getrandbits(1))
    stick3 = bool(random.getrandbits(1))
    stick4 = bool(random.getrandbits(1))
    return stick1, stick2, stick3, stick4

def score(stick1, stick2, stick3, stick4):
    sticksup = sum([stick1,stick2,stick3,stick4])
    if sticksup == 0:
        return 5
    elif sticksup == 1:
        if stick4:
            return -1
        else:
            return 1
    elif sticksup == 2:
        return 2
    elif sticksup == 3:
        return 3
    else:
        return 4

async def playyutnori(ctx,player1,player2,board,boardstring):
    await ctx.respond(f'{ctx.author.mention} has started a game of yut nori with {player2.mention}')
    await ctx.send(f'Throw the sticks to decide who goes first!')
    await ctx.send(f"\n {ctx.author.mention}'s go to throw",view=yutnoriplayer1view())


@bot.slash_command(name="yutnori",description="starts a game of yut nori with whoever you ping")
async def yutnorigame(ctx,opponent: Option(discord.Member, "opponent") ):
    global player1pieces
    global player2pieces
    player1pieces = [0,0,0,0]
    player2pieces = [0,0,0,0]
    global player2
    player2 = opponent
    global player1
    player1 = ctx.author
    global boardstring
    boardstring = ""
    for item in list(board.values()):
        boardstring += item 
    await playyutnori(ctx,player1,player2,board,boardstring)
    
    
class yutnoriplayer1view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Throw",custom_id="player1throw")
    async def throw(self, button, interaction):
        global board
        global player1
        global player2
        
        if interaction.user == player2:
            await interaction.response.send_message("It is not your turn to throw!",view=None,ephemeral=True)
        else:
            button.disabled = True
            button.style = discord.ButtonStyle.green
            #await interaction.response.edit_message(view=self)
            playerthrow = roll()
            global playerscore
            playerscore = score(playerthrow[0],playerthrow[1],playerthrow[2],playerthrow[3])
            emojis = []

            if playerthrow[0]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[1]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[2]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[3]:
                emojis.append('<:upcross_:1014501307052216411>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            emojistring = " ".join(emojis)
            await interaction.channel.send(content=emojistring)
            await interaction.channel.send(f'{player2.mention}\'s go to throw',view=yutnoriplayer2view())
            global player1score
            player1score = playerscore
        
class yutnoriplayer2view(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label="Throw",custom_id="player1throw")
    async def throw(self, button, interaction):
        global board
        global player1
        global player2
        if interaction.user == player1:
            await interaction.followup.send("It is not your turn to throw!",view=None,ephemeral=True)
        else:
            button.disabled = True
            button.style = discord.ButtonStyle.green
            await interaction.response.edit_message(view=self)
            playerthrow = roll()
            global playerscore
            playerscore = score(playerthrow[0],playerthrow[1],playerthrow[2],playerthrow[3])
            emojis = []

            if playerthrow[0]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[1]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[2]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[3]:
                emojis.append('<:upcross_:1014501307052216411>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            emojistring = " ".join(emojis)
            await interaction.followup.send(content=emojistring)
            global player1score
            player2score = playerscore
            global move
            if player1score > player2score:
                move = await interaction.channel.send(f"{player1.mention} will start first")
            elif player2score > player1score:
                move = await interaction.channel.send(f"{player2.mention} will start first")
                tmp = player1
                player1 = player2
                player2 = tmp
            else:
                await interaction.channel.send(f'DRAW!. Throw again \n {player1.mention}:',view=yutnoriplayer1view())
                return
            boardstring = ""
            for item in list(board.values()):
                boardstring += item 
            await interaction.channel.send('The board: \n' + boardstring,view = yutnoriplayer1move1view())
            

class yutnoriplayer1move1view(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label="Throw",custom_id="player1move")
    async def move(self, button, interaction):
        global board
        global player1
        global player2
        global numplayer1pieces
        global player1pieces
        if interaction.user == player2:
            await interaction.response.send_message("It is not your turn to move!",view=None,ephemeral=True)
        else:
            button.disabled = True
            button.style = discord.ButtonStyle.green
            await interaction.response.edit_message(view=self)
            playerthrow = roll()
            playerscore = score(playerthrow[0],playerthrow[1],playerthrow[2],playerthrow[3])
            emojis = []

            if playerthrow[0]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[1]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[2]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[3]:
                emojis.append('<:upcross_:1014501307052216411>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            emojistring = " ".join(emojis)
            playerscoremessage = await interaction.followup.send(content=f'{player1.mention} threw a {playerscore}')
            playerscoreimagemessage = await interaction.followup.send(content=emojistring)
            originalmessage = await interaction.original_message()
            if playerscore == -1:
                board[1] = "🔵"
                player1pieces[0] = 1
            else:
                board[playerscore]="🔵"
                player1pieces[0] = playerscore
            numplayer1pieces = 0
            for piece in player1pieces:
                if piece != 0:
                    numplayer1pieces += 1
            board["player1home"]="🔵"*(4-numplayer1pieces)
            boardstring = ""
            for item in list(board.values()):
                boardstring += item 
            await move.edit(f"{player2.mention}'s go")
            await originalmessage.edit(content=boardstring,view=yutnoriplayer2move1view())
            await playerscoremessage.delete()
            await playerscoreimagemessage.delete()

class yutnoriplayer2move1view(discord.ui.View):
    def __init__(self):
        super().__init__()
    
    @discord.ui.button(label="Throw",custom_id="player1move")
    async def move(self, button, interaction):
        global board
        global player1
        global player2
        global numplayer2pieces
        global player1pieces
        if interaction.user == player1:
            await interaction.response.send_message("It is not your turn to move!",view=None,ephemeral=True)
        else:
            button.disabled = True
            button.style = discord.ButtonStyle.green
            await interaction.response.edit_message(view=self)
            playerthrow = roll()
            playerscore = score(playerthrow[0],playerthrow[1],playerthrow[2],playerthrow[3])
            emojis = []

            if playerthrow[0]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[1]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[2]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[3]:
                emojis.append('<:upcross_:1014501307052216411>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            emojistring = " ".join(emojis)
            playerscoremessage = await interaction.followup.send(content=f'{player1.mention} threw a {playerscore}')
            playerscoreimagemessage = await interaction.followup.send(content=emojistring)
            originalmessage = await interaction.original_message()
            
            global player1pieces
            global numplayer1pieces
            if playerscore == -1:
                if board[1] == "🔵":
                    player1pieces[0] = 0
                    numplayer1pieces -= 1
                    
                board[1] = "🔴"
                player2pieces[0] = 1
            else:
                if board[1] == "🔵":
                    player1pieces[0] = 0
                    numplayer1pieces -= 1
                board[playerscore]="🔴"
                player2pieces[0] = playerscore
            numplayer2pieces = 0
            for piece in player2pieces:
                if piece != 0:
                    numplayer2pieces += 1
            board["player2home"]="🔴"*(4-numplayer2pieces)
            board["player1home"] = "🔵"*(4-numplayer1pieces)
            boardstring = ""
            for item in list(board.values()):
                boardstring += item 
            await originalmessage.edit(content=boardstring,view=yutnoriplayer1move2view())
            await playerscoremessage.delete()
            await playerscoreimagemessage.delete()
            await move.edit(f"{player1.mention}'s go")

class yutnoriplayer1move2view(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Throw",custom_id="player1move")
    async def move(self, button, interaction):
        global board
        global player1
        global player2
        global player1pieces
        global player2pieces

        if interaction.user == player2:
            await interaction.response.send_message("It is not your turn to move!",view=None,ephemeral=True)
        else:
            button.disabled = True
            button.style = discord.ButtonStyle.green
            await interaction.response.edit_message(view=self)
            playerthrow = roll()
            playerscore = score(playerthrow[0],playerthrow[1],playerthrow[2],playerthrow[3])
            emojis = []
            if playerthrow[0]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[1]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[2]:
                emojis.append('<:up_:1014501305814880286>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            if playerthrow[3]:
                emojis.append('<:upcross_:1014501307052216411>')
            else:
                emojis.append('<:down_:1014501304321708093>')
            emojistring = " ".join(emojis)
            global player1score
            player1score = playerscore
            playerscoremessage = await interaction.followup.send(content=f'{player1.mention} threw a {playerscore}')
            playerscoreimagemessage = await interaction.followup.send(content=emojistring)
            originalmessage = await interaction.original_message()
            time.sleep(2)
            await playerscoremessage.delete()
            await playerscoreimagemessage.delete()
            global player1pieces
            view = yutnoriplayer1DefaultView()
            if 0 in player1pieces:
                view.add_item(yutnoriplayer1DefaultButton(label="get a new piece out",custom_id="player1newpiece"))
            for piece in (piece for piece in player1pieces if piece != 0):
                view.add_item(yutnoriplayer1DefaultButton(label=f"Move piece at location {piece}",custom_id=f"player1piece{piece}"))
            await originalmessage.edit(view=view)


class yutnoriplayer1DefaultButton(discord.ui.Button):
    def __init__(self, custom_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_id = custom_id

    async def callback(self, interaction: discord.Interaction):
        
        self.view.custom_id = interaction.custom_id
        print(interaction.custom_id)
        global player2
        if interaction.user == player2:
            await interaction.response.send_message("It is not your turn to move!",view=None,ephemeral=True)
        else:
            global player1pieces
            global numplayer1pieces
            global numplayer2pieces
            global board
            global player1
            global player2pieces
            global player1score
            await interaction.response.defer()
            if interaction.custom_id == "player1newpiece":
                print("new piece")

                print(board[player1score])
                if board[player1score].__contains__("🔵"):
                    print('contains blue')
                    board[player1score]+="🔵"
                    for piece in player1pieces:
                        if piece == 0:
                            player1pieces[piece] = player1score
                            break
                    numplayer1pieces += 1
                elif board[player1score].__contains__("🔴"):
                    print('contains red')
                    board[player1score] = "🔵"
                    for piece in [piece for piece in player2pieces if piece == player1score]:
                        player2pieces[piece] = 0
                        numplayer2pieces -= 1
                else:
                    print('does not contain blue or red')
                    board[player1score] = "🔵"
                    for piece in player1pieces:
                        if piece == 0:
                            print(player1pieces.index(piece))
                            player1pieces[player1pieces.index(piece)] = player1score
                            print(player1pieces)
                            break
            elif interaction.custom_id.__contains__("player1piece"):
                num = int(interaction.custom_id[12:])
                newplace = player1pieces[num] + player1score
                if board[player1score+player1pieces[num]].__contains__("🔵"):
                    print('contains blue')
                    board[player1score]+="🔵"
                    for piece in player1pieces:
                        if piece == 0:
                            player1pieces[piece] = player1score
                            break
                elif board[player1score].__contains__("🔴"):
                    print('contains red')
                    board[player1score] = "🔵"
                    for piece in [piece for piece in player2pieces if piece == player1score]:
                        player2pieces[piece] = 0
                        numplayer2pieces -= 1
                

            board["player2home"]="🔴"*(4-numplayer2pieces)
            board["player1home"] = "🔵"*(4-numplayer1pieces)
            boardstring = ""
            for item in list(board.values()):
                boardstring += item 
            originalmessage = await interaction.original_message()
            await originalmessage.edit(content=boardstring,view=None)
                
            self.view.disable_all_items()
            self.view.stop()
            return

class yutnoriplayer1DefaultView(discord.ui.View):
    def __init__(self, custom_id=None):
        super().__init__()
        self.custom_id = custom_id

    async def on_timeout(self):
        self.disable_all_items()
        self.stop()
        await self.message.interaction.followup.send("Timed out.", ephemeral=True)
        return

    

#class yutnoriplayer2moveview(discord.ui.View):


bot.run(os.getenv('TOKEN'))