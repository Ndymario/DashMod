from quart_discord import DiscordOAuth2Session
import  quart
from quart import  Quart , render_template , websocket
import asyncio


app = Quart(__name__)

@app.route("/")
async def main_page():
    return render_template("main.html")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app.run())
