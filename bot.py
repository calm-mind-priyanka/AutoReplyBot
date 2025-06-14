from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import asyncio
import json

# Your credentials (hardcoded)
API_ID = 6046055058
API_HASH = "f5976eb15ac17891076075f76a9c312b"
SESSION = "1BVtsOJwBu1YysL2z1emSlrKzvUybF7uU6-VjgnQQVPUI53D-acAfsjaVCOhtcq26eoUESAUQ5XXSeAUJn6iR9OS93fC77DRysJOYy45CSSp3Y_m-pSf-kZ4Ueps7WfZouywJK0D8hXC7XgJDAYW0pkIJinKqDZ-n83VMm9H2diPEO-kAZ3FfUuDStN5xJSuakrzRC_XIi18nrYVI_oO5LJONRlC07V0RorPyuTdsw9G8TfPVUu0TwVU7kC2yyj-ZF6imqaktmzSScoen9npNMBZWn9C93G0cDeI1U1_KjP0fEeUeyQPFzg4KEhhP0uLHIHj7-duQObdPgFapN7QYiONCgIScRkM="

ADMINS = [123456789]  # Replace with your actual Telegram user ID

GROUPS_FILE = "groups.json"
SETTINGS_FILE = "settings.json"

# Load saved groups and settings
def load_data():
    try:
        with open(GROUPS_FILE, "r") as f:
            groups = set(json.load(f))
    except:
        groups = set()

    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            reply_msg = data.get("reply_msg", "SEARCH YOUR MOVIE HERE @Yourmovielinkk")
    except:
        reply_msg = "SEARCH YOUR MOVIE HERE @Yourmovielinkk"

    return groups, reply_msg

# Save current groups
def save_groups(groups):
    with open(GROUPS_FILE, "w") as f:
        json.dump(list(groups), f)

# Save current reply message
def save_settings(reply_msg):
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"reply_msg": reply_msg}, f)

TARGET_GROUPS, AUTO_REPLY_MSG = load_data()

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    if event.chat_id in TARGET_GROUPS and event.sender_id != (await client.get_me()).id:
        sent_msg = await event.reply(AUTO_REPLY_MSG)
        await asyncio.sleep(15)
        await sent_msg.delete()

@client.on(events.NewMessage(pattern="/add"))
async def add_group(event):
    if event.sender_id in ADMINS:
        try:
            group_id = int(event.message.text.split(" ", 1)[1])
            TARGET_GROUPS.add(group_id)
            save_groups(TARGET_GROUPS)
            await event.reply(f"✅ Added group: `{group_id}`")
        except:
            await event.reply("❌ Error: Provide a valid group ID.")

@client.on(events.NewMessage(pattern="/remove"))
async def remove_group(event):
    if event.sender_id in ADMINS:
        try:
            group_id = int(event.message.text.split(" ", 1)[1])
            TARGET_GROUPS.discard(group_id)
            save_groups(TARGET_GROUPS)
            await event.reply(f"❎ Removed group: `{group_id}`")
        except:
            await event.reply("❌ Error: Provide a valid group ID.")

@client.on(events.NewMessage(pattern="/setmsg"))
async def set_msg(event):
    global AUTO_REPLY_MSG
    if event.sender_id in ADMINS:
        try:
            AUTO_REPLY_MSG = event.message.text.split(" ", 1)[1]
            save_settings(AUTO_REPLY_MSG)
            await event.reply("✅ Reply message updated!")
        except:
            await event.reply("❌ Error: Provide a message.")

@client.on(events.NewMessage(pattern="/delmsg"))
async def del_msg(event):
    global AUTO_REPLY_MSG
    if event.sender_id in ADMINS:
        AUTO_REPLY_MSG = ""
        save_settings(AUTO_REPLY_MSG)
        await event.reply("🗑️ Auto reply message cleared.")

async def main():
    print("🤖 Bot is running...")
    await client.run_until_disconnected()

client.start()
client.loop.run_until_complete(main())
