import discord 
from discord.ext import commands
from config import*
import os

class aclient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='test ',
                         intents=discord.Intents.all())
        self.synced=False
        
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await client.tree.sync(guild=discord.Object(id=942405042697277502))
            self.synced=True
        print('Staging Bot Online and Well')
        
    async def setup_hook(self):
     for filename in os.listdir('./commands'):
      if filename.endswith('.py'):
        await self.load_extension(f'commands.{filename[:-3]}')
        
client=aclient()
client.run(token)
        