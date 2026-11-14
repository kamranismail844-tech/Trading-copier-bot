import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

API_ID = int(os.getenv("API_ID", "33698486"))
API_HASH = os.getenv("API_HASH", "61e4a7c1b861b141eede9901dbf6935b")
SESSION_STRING = os.getenv("SESSION_STRING")

SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL", "@XAUUSD_GOLD_TRADING_FOREX")
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
        
        # 1. Agar message mein koi doosra channel link ya promotion ho, toh poora ignore kar do
        if re.search(r'(?:https?://|www\.|t\.me/|telegram\.me/|join|subscribe|vip channel)', text, flags=re.IGNORECASE):
            # Agar signal ke andar t.me link hai lekin sath TP/SL/ENTRY hai toh allow karein, warna skip
            if not ("t.me/" in text and ("TP" in text or "SL" in text or "ENTRY" in text)):
                return

        # 2. Check karein ke message mein koi contact ya username hai ya nahi
        has_contact = bool(re.search(r'(@\w+|\bcontact\b|\badmin\b|\bmanager\b)', text, flags=re.IGNORECASE))
        
        if has_contact:
            # Purane usernames/contacts hata kar apna contact set karein
            text = re.sub(r'@\w+', CUSTOM_CONTACT, text)
            text = re.sub(r'(?:Contact|Admin|Manager)[\s:]*@?\w+', f"Contact: {CUSTOM_CONTACT}", text, flags=re.IGNORECASE)
            
            # Agar footer mein contact nahi hai toh end mein add kar dein
            if CUSTOM_CONTACT not in text:
                text += f"\n\nContact: {CUSTOM_CONTACT}"
        else:
            # Agar message mein pehle se koi contact nahi tha, toh apni taraf se nahi lagana
            pass

        # Baqi fazool links ya phone numbers saaf karna
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
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

print("Bot is running with refined link/contact filters...")
client.start()
client.run_until_disconnected()
