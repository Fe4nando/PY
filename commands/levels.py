import discord 
from discord.ext import commands
import json
import random
import PIL
from PIL import Image,ImageDraw,ImageFont
import io
from io import BytesIO

class Level(commands.Cog):
    def __init__(self,client):
        self.client=client
        
    @commands.Cog.listener()
    async def on_message(self,ctx):
        xp=random.randint(150,300)
        max=10000
        await open_account(ctx.author)
        users=await get_level_data()
        user=ctx.author  
        users[str(user.id)]['xp']+=xp
        with open(r'./data/level.json','w') as f:
         json.dump(users,f)
        await open_account(ctx.author)
        users=await get_level_data()
        xp=users[str(user.id)]['xp']
        if xp >= max:
            currentxp=xp-max
            users[str(user.id)]['level']+=1
            users[str(user.id)]['xp']=currentxp
            with open(r'./data/level.json','w') as f:
              json.dump(users,f)
            channel = discord.utils.get(ctx.guild.channels, name='pick-this-one')
            level=users[str(user.id)]['level']
            await channel.send(f'{ctx.author.display_name} has leveled up to {level}')
            
    @commands.command()
    async def level(self,ctx):
        await open_account(ctx.author)
        users=await get_level_data()
        eexp=users[str(ctx.author.id)]['xp']
        level=users[str(ctx.author.id)]['level']
        exp=eexp/10000
        exppre=exp*100
        exp=exppre*17
        exp=(int(exp))
        member=ctx.author
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
        layer1.save(r'./data/final.png')
        await ctx.send(file=discord.File(r'./data/final.png'))
              
        
              
            
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def view_levels(self,ctx):
        await ctx.send(file=discord.File(r'./data/level.json'))
            
        
    
    
    
        
        
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
    await client.add_cog(Level(client))