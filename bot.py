import asyncio
# FIX for Render Python 3.12+ : No current event loop error
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

import sys, glob, importlib, logging, os
from pathlib import Path
import pytz
from datetime import date, datetime
from pyrogram import idle
from aiohttp import web
from config import LOG_CHANNEL, ON_HEROKU, CLONE_MODE
from Script import script 
from TechVJ.server import web_server
from plugins.clone import restart_bots
from TechVJ.bot import StreamBot
from TechVJ.utils.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

PORT = int(os.environ.get("PORT", 8080))

async def start():
    print('\nInitalizing Tech VJ Bot')
    await StreamBot.start()
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    print(f"Bot: {bot_info.username}")
    await initialize_clients()
    
    files = glob.glob("plugins/*.py")
    for name in files:
        patt = Path(name)
        plugin_name = patt.stem
        spec = importlib.util.spec_from_file_location(f"plugins.{plugin_name}", f"plugins/{plugin_name}.py")
        load = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(load)
        sys.modules[f"plugins.{plugin_name}"] = load
        print(f"Imported => {plugin_name}")

    if ON_HEROKU:
        asyncio.create_task(ping_server())

    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    time = datetime.now(tz).strftime("%H:%M:%S %p")
    
    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", PORT).start()
    print(f"Web Server Started on 0.0.0.0:{PORT}")
    
    try:
        await StreamBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    except Exception as e:
        print(f"LOG_CHANNEL Error: {e}")

    if CLONE_MODE:
        await restart_bots()
    print("Bot Started Powered By @VJ_Bots")
    await idle()
    await StreamBot.stop()

if __name__ == '__main__':
    asyncio.run(start())
