import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.getenv("API_ID", "33698486"))
API_HASH = os.getenv("API_HASH", "61e4a7c1b861b141eede9901dbf6935b")
SESSION_STRING = os.getenv("SESSION_STRING")

SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL", "@tradddingsigggnals")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL", "@TradeXManagement")
CUSTOM_CONTACT = os.getenv("CUSTOM_FOOTER", "@Mr_tradern")

if not SESSION_STRING:
    print("ERROR: SESSION_STRING environment variable is missing!")
    exit(1)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        text = event.raw_text or ""
        
        # 1. Agar message mein koi bhi link, t.me ya promotion ho, toh poora message ignore kar do
        if re.search(r'(?:https?://|www\.|t\.me|telegram\.me|join|subscribe|channel|vip)', text, flags=re.IGNORECASE):
            return  # Poora message skip ho jaye ga

        # 2. Check karo ke message mein koi contact/username ya phone number mojood hai ya nahi
        has_contact = bool(re.search(r'(@\w+|\bcontact\b|\badmin\b|\bmanager\b|\+?[0-9][0-9()\-\s]{8,}[0-9])', text, flags=re.IGNORECASE))
        
        if has_contact:
            # Agar original message mein contact tha, toh usay replace kar ke aapka contact laga do
            text = re.sub(r'@\w+', CUSTOM_CONTACT, text)
            text = re.sub(r'(?:Contact|Admin|Manager)[\s:]*@?\w+', f"Contact: {CUSTOM_CONTACT}", text, flags=re.IGNORECASE)
            
            # Agar footer format mein likhna ho
            if CUSTOM_CONTACT not in text:
                text += f"\n\nContact: {CUSTOM_CONTACT}"
        else:
            # Agar message mein koi contact nahi tha, toh apna contact BILKUL NAHI LAANA (jaise simple "150$" wala msg)
            pass

        text = text.strip()
        
        if not text:
            return

        # Target channel par bhejna
        if event.media:
            await client.send_file(TARGET_CHANNEL, event.media, caption=text)
        elif text:
            await client.send_message(TARGET_CHANNEL, text)
            
    except Exception as e:
        print(f"Error: {e}")

print("Bot is running with smart filtering...")
client.start()
client.run_until_disconnected()
