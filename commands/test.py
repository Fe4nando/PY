import discord 
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
import random
import json
import PIL
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
from assets.presets import *

from numpy import int0


class Test(commands.Cog):
    def __init__(self,client):
        self.client=client 
    
    def perms(ctx):
     return ctx.author.id==738243110949355672
        
   
    @app_commands.command(name='setweekahead',description='Sets the weekeahead link')
    @app_commands.checks.has_role(979700065444712448)
    async def setweekahead(self,interaction:discord.Interaction,weeknumber:int,url:str):
     
     channel = discord.utils.get(interaction.guild.channels, name='testing-channel1')
     embed=discord.Embed(title=f'Week {weeknumber}',description=f"The Week ahead has been uploaded")
     embed.add_field(name='**Link**',value=f"[Click to View Week {weeknumber}]({url})")
     embed.set_thumbnail(url="https://preview.redd.it/hbxy0q8sbyf71.png?width=640&crop=smart&auto=webp&s=14e6b46c58c749a812547a9ecc5c7bed3d3d9a04")
     await interaction.response.send_message('Week ahead has been Set!')
     await channel.send(embed=embed)
     with open (r"./assets/week.json","r") as f:
        mhm=json.load(f)
        mhm[str("Week Ahead")]={}
        mhm[str("Week Ahead")]["url"]=url
        mhm[str("Week Ahead")]["number"]=weeknumber
     with open (r"./assets/week.json","w") as f:
        json.dump(mhm,f)
        
    @setweekahead.error
    async def setweekahead_commandError(self,interaction:discord.Interaction,error:app_commands.AppCommandError):
        if isinstance(error,app_commands.MissingRole):
            await interaction.response.send_message('Missing Permissions',ephemeral=True)
        
   
    @app_commands.command(name='view_weekahead',description='view this weeks weekahead with this command')
    async def view_weekahead(self,interaction:discord.Interaction):
     with open (r"./assets/week.json","r") as f:
         mhm=json.load(f)
         url=mhm[str("Week Ahead")]["url"]
         weeknumber=mhm[str("Week Ahead")]["number"]
     embed=discord.Embed(title=f'Week {weeknumber}')
     embed.add_field(name='**Link**',value=f"[Click to View Week {weeknumber}]({url})")
     embed.set_thumbnail(url="https://preview.redd.it/hbxy0q8sbyf71.png?width=640&crop=smart&auto=webp&s=14e6b46c58c749a812547a9ecc5c7bed3d3d9a04")
     await interaction.response.send_message(embed=embed)
     
    @app_commands.command(name='level_check',description="view your server level")
    async def level_check(self,interaction:discord.Interaction):
        await open_account(interaction.user)
        users=await get_level_data()
        eexp=users[str(interaction.user.id)]['xp']
        level=users[str(interaction.user.id)]['level']
        exp=eexp/10000
        exppre=exp*100
        exp=exppre*17
        exp=(int(exp))
        member=interaction.user
        pfp = member.avatar.with_size(1024)
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert("RGBA")
        pfp = pfp.resize((280,280))
        image=Image.open(r'./data/progressbar.png').convert('RGBA')
        image=image.resize((exp,80))
        background=Image.open(r'./data/blank.png').convert('RGBA')
        background.paste(image,(110,525),image)
        background.paste(pfp,(110,70),pfp)
        background.save(r'./data/bar.png')
        layer1=Image.open(r'./data/bar.png').convert('RGBA')
        layer2=Image.open(r'./data/level main card overlay.png').convert('RGBA')
        layer1.paste(layer2,(0,0),layer2)
        font=ImageFont.truetype(r'./data/pasti.otf',115)
        font1=ImageFont.truetype(r'./data/pasti.otf',64)
        write= ImageDraw.Draw(layer1)
        string=(f'Level-{level}')
        amount=f'{eexp}/10000'
        W, H = (1920,700)
        w, h = font.getsize(string)
        w1,h2=font1.getsize(amount)
        
        write.text(((W-w)/2,(H-h)/2),string,font=font,fill='white')
        write.text(((W-w1)/2,420),amount,font=font1,fill='white')
        layer1.save(r'./data/final1.png')
       
        
       
        await interaction.response.send_message(file = discord.File(r"./data/final1.png"))
        
    @app_commands.command(name='create_embed',description='creates a discord embed')
    @app_commands.choices(color= [
        Choice(name="White",value="White"),
        Choice(name="Black",value="Black"),
        Choice(name='Blue',value='Blue'),
        Choice(name='Red',value='Red'),
        Choice(name='Green',value='Green')
        
    ])
        
    async def Create_Embed(self,interaction:discord.Interaction,channel:discord.TextChannel,title:str,text:str,color:str):
            
        embed=discord.Embed(title=title,description=text,color=color)
        await channel.send(embed=embed)
        await interaction.response.send_message('Sent!')
       
                            

    

async def open_account(user):
    users= await get_level_data()
        
    if str(user.id)in users:
        return False
    else:
        users[str(user.id)]={}
        users[str(user.id)]['level']=1
        users[str(user.id)]['xp']=0
        
    with open(r'./data/level.json','w') as f:
        json.dump(users,f)
    return True
    
async def get_level_data():
    with open(r'./data/level.json','r') as f:
        users=json.load(f)
    return users
    
        
async def setup(client):
   await client.add_cog(Test(client),guilds=[discord.Object(id=942405042697277502)])
   
   

   