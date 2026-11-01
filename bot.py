# Don't Remove Credit @VJ_Bots - Fixed by @KingVJ01
import sys
import glob
import importlib
from pathlib import Path
import logging
import asyncio
import pytz
from datetime import date, datetime

from pyrogram import Client, __version__, idle
from pyrogram.raw.all import layer
from aiohttp import web

from config import LOG_CHANNEL, ON_HEROKU, CLONE_MODE
from Script import script 
from TechVJ.server import web_server
from plugins.clone import restart_bots
from TechVJ.bot import StreamBot
from TechVJ.utils.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

# Logging - Safe mode
logging.basicConfig(level=logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

import os
PORT = int(os.environ.get("PORT", 8080))  # FIX 1: Render er PORT env use korbe, int e

ppath = "plugins/*.py"
files = glob.glob(ppath)

async def start():
    print('\nInitalizing Tech VJ Bot')
    
    await StreamBot.start()
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    print(f"Bot: {bot_info.username}")
    
    await initialize_clients()
    
    for name in files:
        patt = Path(name)
        plugin_name = patt.stem.replace(".py", "")
        plugins_dir = Path(f"plugins/{plugin_name}.py")
        import_path = "plugins.{}".format(plugin_name)
        spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
        load = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(load)
        sys.modules["plugins." + plugin_name] = load
        print("Tech VJ Imported => " + plugin_name)

    if ON_HEROKU:
        asyncio.create_task(ping_server())

    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")
    
    # Web Server - FIX 2: PORT int
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    await web.TCPSite(app, bind_address, PORT).start()
    print(f"Web Server Started on {bind_address}:{PORT}")
    
    try:
        await StreamBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
    except Exception as e:
        print(f"LOG_CHANNEL Error: {e} - Check -100")

    if CLONE_MODE:
        await restart_bots()
        
    print("Bot Started Powered By @VJ_Bots")
    await idle()
    await StreamBot.stop()

if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
