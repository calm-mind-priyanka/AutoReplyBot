import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Add your own credentials here
API_ID = 12345678  # Replace with your API ID
API_HASH = "your_api_hash"  # Replace with your API Hash
SESSION = "your_session_string"  # Replace with your session string

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

GROUP_FILE = "groups.txt"
MESSAGE_FILE = "message.txt"

def load_groups():
    if not os.path.exists(GROUP_FILE):
        return set()
    with open(GROUP_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_groups(groups):
    with open(GROUP_FILE, "w") as f:
        f.write("\n".join(groups))

def load_message():
    if not os.path.exists(MESSAGE_FILE):
        return "Default auto-reply message"
    with open(MESSAGE_FILE, "r") as f:
        return f.read()

def save_message(msg):
    with open(MESSAGE_FILE, "w") as f:
        f.write(msg)

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    groups = load_groups()
    msg_text = load_message()

    # Admin commands
    if event.text.startswith("/addgroup") and sender.is_self:
        group_id = str(event.chat_id)
        groups.add(group_id)
        save_groups(groups)
        await event.reply("✅ This group has been added to auto-reply list.")

    elif event.text.startswith("/removegroup") and sender.is_self:
        group_id = str(event.chat_id)
        groups.discard(group_id)
        save_groups(groups)
        await event.reply("❌ Group removed from auto-reply list.")

    elif event.text.startswith("/setmsg") and sender.is_self:
        new_msg = event.text.split(" ", 1)[1] if " " in event.text else ""
        if new_msg:
            save_message(new_msg)
            await event.reply("✏️ Auto-reply message updated.")
        else:
            await event.reply("⚠️ Usage: /setmsg your message here")

    elif event.text.startswith("/viewmsg") and sender.is_self:
        await event.reply(f"📩 Current Message:

{msg_text}")

    # Auto reply
    elif str(event.chat_id) in groups and not sender.is_self:
        await event.reply(msg_text)

print("Bot is starting...")
client.start()
client.run_until_disconnected()
