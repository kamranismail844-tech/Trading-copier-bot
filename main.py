import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.getenv("API_ID", "33698486"))
API_HASH = os.getenv("API_HASH", "61e4a7c1b861b141eede9901dbf6935b")
SESSION_STRING = os.getenv("SESSION_STRING")

SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL", "@FxSpaceGlobal")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL", "@TradeXManagement")
CUSTOM_FOOTER = os.getenv("CUSTOM_FOOTER", "Contact: @Mr_tradern")

if not SESSION_STRING:
    print("ERROR: SESSION_STRING environment variable is missing!")
    exit(1)

# Session string ke sath client start karna
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        text = event.raw_text or ""
        
        # 1. Skip Promotions & Ads
        if re.search(r'(?:https?://|www\.|t\.me|telegram\.me|vip channel|join|subscribe)', text, flags=re.IGNORECASE):
            if "t.me/" in text and not ("TP" in text or "SL" in text or "ENTRY" in text):
                return
        
        # 2. Smart Username Replacement
        text = re.sub(r'@\w+', '@Mr_tradern', text)
        
        # Baqi links remove karna
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'\+?[0-9][0-9()\-\s]{8,}[0-9]', '', text)
        
        text = text.strip()
        
        # Custom footer add karna
        if CUSTOM_FOOTER and CUSTOM_FOOTER not in text:
            text += f"\n\n{CUSTOM_FOOTER}"
            
        # Target channel par bhejna
        if event.media:
            await client.send_file(TARGET_CHANNEL, event.media, caption=text)
        elif text:
            await client.send_message(TARGET_CHANNEL, text)
            
    except Exception as e:
        print(f"Error: {e}")

print("Bot is running and listening for signals...")
client.start()
client.run_until_disconnected()
