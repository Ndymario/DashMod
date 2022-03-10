import discord
from quart import  Quart , render_template , url_for , redirect
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import asyncio
import os
import random
from discord.ext import ipc , commands

secret_file = open("secret_dash.txt", "r")
secret = secret_file.read()
secret_file.close()

client_id_file = open("client_id.txt", "r")
client_id = client_id_file.read()
client_id_file.close()

client_secret_file = open("client_secret.txt", "r")
client_secret = client_secret_file.read()
client_secret_file.close()

redirect_uri_file = open("redirect_uri.txt", "r")
redirect_uri = redirect_uri_file.read()
redirect_uri_file.close()

app = Quart(__name__)

app.secret_key = b"shhh"
app.config["SECRET_KEY"] = secret
app.config["DISCORD_CLIENT_ID"] = client_id
app.config["DISCORD_CLIENT_SECRET"] = client_secret
app.config["DISCORD_REDIRECT_URI"] = redirect_uri 

discord = DiscordOAuth2Session(app)
myipc = ipc.Client(secret_key="dashmod")


@app.route("/")
async def main_page():
    return await render_template("index.html")

@app.route("/dashboard")
@requires_authorization
async def dashboard():
    welcomes = ["We've Been waiting",'What is cooking?','How has your day been?']
    user = await discord.fetch_user()
    choice = random.choice(welcomes)
    try:
        guilds = await discord.fetch_guilds()
    except:
        return redirect(url_for("login"))

    userguilds = []
    for guild in guilds:
        idbruh = guild.id
        if guild.permissions.manage_guild:
            req_thingy = await myipc.request("to_check_whether_im_in_it",idbruh=idbruh)
            if req_thingy == True:
                userguilds.append(guild)
            else:
                continue


    return await render_template("dashboard.html",user=user , choice=choice , guilds = userguilds)


@app.route("/login")
async def login():
    return await discord.create_session()

@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except Exception:
        return redirect(url_for("login"))
    
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run())
