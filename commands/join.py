
import discord 
from discord.ext import commands
import io
from io import BytesIO
import PIL
from PIL import Image,ImageDraw,ImageFont

class Join(commands.Cog):
    
    def __init__(self,client):
        self.client=client
        
    @commands.Cog.listener()
    async def on_member_join(self,member):
     W,H=(1920,800)
     guild=member.guild
     channel = discord.utils.get(guild.channels, name='pick-this-one')
     pfp = member.avatar.with_size(1024)
     data = BytesIO(await pfp.read())
     pfp = Image.open(data).convert("RGBA")
     pfp = pfp.resize((199,213))
     background=Image.open(r'./data/blank2.png').convert('RGBA')
     background.paste(pfp,(1171,92),pfp)
     layer1=Image.open(r'./data/templatecard.png').convert('RGBA')
     font=ImageFont.truetype(r'./data/pasti.otf',100)
     background.paste(layer1,(0,0),layer1)
     write= ImageDraw.Draw(background)
     string=(f'{member.display_name}')
     w, h = font.getsize(string)
     write.text(((W-w)/2,(H-h)/2),string,font=font,fill='white')
     background.save(r'./data/on_join.png')
     await channel.send(file=discord.File(r'./data/on_join.png'))
    
    
    @commands.command()
    async def test(self,ctx):
        embed=discord.Embed(title="test")
        file = discord.File(r"./data/final.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await ctx.send(file=file,embed=embed)
        
async def setup(client):
   await client.add_cog(Join(client))