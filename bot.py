import discord
from discord.ext import commands
from discord.ext import ipc
import json
import os

class ClientBot(commands.Bot):
    def __init__(self, *args , **kwargs):
        super().__init__(*args,**kwargs)
        self.ipc = ipc.Server(self,secret_key="dashmod")

    async def on_ipc_read(self):
        print("We are ready!")
    
    async def on_ipc_error(self,endpoint,error):
        print(f"{endpoint} Raised {error}")

    async def on_ready(self):
        print("ready to launch babbbby")
        print(client.guilds)

client = ClientBot(command_prefix="d!",strip_after_prefix=True)

@client.ipc.route()
async def to_check_whether_im_in_it(data):

    for guild in client.guilds:
        if guild.id == data.idbruh:
            return True
        else:
            continue

    return False

for filename in os.listdir():
    pass
    

client.ipc.start()
client.run("BRO IM STOKED FOR TOMMOROW")
