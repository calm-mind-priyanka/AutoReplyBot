from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")  # This is your string session

ADMINS = [123456789]  # 👈 Replace with your Telegram user ID

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

TARGET_GROUPS = set()
AUTO_REPLY_MSG = "SEARCH YOUR MOVIE HERE @Yourmovielinkk"

@client.on(events.NewMessage)
async def handler(event):
    if event.chat_id in TARGET_GROUPS and event.sender_id != (await client.get_me()).id:
        sent_msg = await event.reply(AUTO_REPLY_MSG)
        await asyncio.sleep(15)  # Delete after 15 seconds
        await sent_msg.delete()

@client.on(events.NewMessage(pattern="/add"))
async def add_group(event):
    if event.sender_id in ADMINS:
        try:
            group_id = int(event.message.text.split(" ", 1)[1])
            TARGET_GROUPS.add(group_id)
            await event.reply(f"✅ Added group: `{group_id}`")
        except:
            await event.reply("❌ Error: Provide a valid group ID.")

@client.on(events.NewMessage(pattern="/remove"))
async def remove_group(event):
    if event.sender_id in ADMINS:
        try:
            group_id = int(event.message.text.split(" ", 1)[1])
            TARGET_GROUPS.discard(group_id)
            await event.reply(f"❎ Removed group: `{group_id}`")
        except:
            await event.reply("❌ Error: Provide a valid group ID.")

@client.on(events.NewMessage(pattern="/setmsg"))
async def set_msg(event):
    global AUTO_REPLY_MSG
    if event.sender_id in ADMINS:
        try:
            AUTO_REPLY_MSG = event.message.text.split(" ", 1)[1]
            await event.reply("✅ Reply message updated!")
        except:
            await event.reply("❌ Error: Provide a message.")

@client.on(events.NewMessage(pattern="/delmsg"))
async def del_msg(event):
    global AUTO_REPLY_MSG
    if event.sender_id in ADMINS:
        AUTO_REPLY_MSG = ""
        await event.reply("🗑️ Auto reply message cleared.")

async def main():
    print("🤖 Bot is running...")
    await client.run_until_disconnected()

client.start()
client.loop.run_until_complete(main())
