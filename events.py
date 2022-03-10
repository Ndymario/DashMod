import discord
from discord.ext import commands
import aiosqlite

class Events(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    @commands.Cog.listener("on_ready")
    async def on_ready():
        async with aiosqlite.connect("./cogs/databases/triggers.db") as db:
            async with db.cursor() as cur:
                await cur.execute("""
                    CREATE TABLE IF NOT EXISTS triggers(
                        id int,
                        word string,
                        reaction string
                    )
                """)

            await db.commit()
    

    @commands.Cog.listener("on_message")
    async def on_message(msg):
        async with aiosqlite.connect("./cogs/databases/triggers.db") as db:
            async with db.cursor() as cur:
                await cur.execute("SELECT * FROM triggers WHERE id=?",(msg.guild.id,))  
                data = cur.fetchone()

            await db.commit()
        
        if msg.content.lower() == data[1].lower():
            await msg.reply(data[2])