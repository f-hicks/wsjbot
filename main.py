from discord.ext import tasks
from discord import default_permissions
import discord
import os
from dotenv import load_dotenv
from datetime import datetime
import random
from events import events

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


bot = discord.Bot(debug_guilds=[947173792826941460])
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

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def say_hello(ctx):
    await ctx.respond("Hey!")


@bot.slash_command(name="createmessage", description = "create a message as the Bot",) # Create a slash command
@default_permissions(manage_messages=True)
async def create_message(ctx):
    await ctx.send_modal(createmessagemodal(title="create an embed")) # Send a message with our View class that contains the button

@bot.slash_command(name="addevent", description = "adds an events to the event list",) # Create a slash command
async def addevent(ctx):
    await ctx.send_modal(addeventmodal(title="add event"))

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


bot.run(os.getenv('TOKEN'))