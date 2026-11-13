import os
import re
from telethon import TelegramClient, events

# Apni details yahan directly bhi daal sakte hain ya JustRunMy.app ke Environment Variables mein
API_ID = int(os.getenv("API_ID", "33698486"))
API_HASH = os.getenv("API_HASH", "61e4a7c1b861b141eede9901dbf6935b")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL", "@tradddingsigggnals")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL", "@TradeXManagement")
CUSTOM_FOOTER = os.getenv("CUSTOM_FOOTER", "Contact: @Mr_tradern")

client = TelegramClient("signal_userbot", API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        text = event.raw_text or ""
        
        # 1. Skip Promotions & Ads (Agar sirf VIP channel ki ad ho aur koi signal na ho to skip karein)
        if re.search(r'(?:https?://|www\.|t\.me|telegram\.me|vip channel|join|subscribe)', text, flags=re.IGNORECASE):
            if "t.me/" in text and not ("TP" in text or "SL" in text or "ENTRY" in text):
                return
        
        # 2. Smart Username Replacement: Channel wala koi bhi @username dega, bot usko replace kar dega
        # Lekin agar link remove karna ho to wo neechay ho ga
        text = re.sub(r'@\w+', '@Mr_tradern', text)
        
        # Baqi general links remove karna (agar signal ke ilawa hon)
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        text = re.sub(r'\+?[0-9][0-9()\-\s]{8,}[0-9]', '', text)
        
        text = text.strip()
        
        # Custom footer / contact info add karna
        if CUSTOM_FOOTER and CUSTOM_FOOTER not in text:
            text += f"\n\n{CUSTOM_FOOTER}"
            
        # Target channel par bhejna (Media ya Text)
        if event.media:
            await client.send_file(TARGET_CHANNEL, event.media, caption=text)
        elif text:
            await client.send_message(TARGET_CHANNEL, text)
            
    except Exception as e:
        print(f"Error: {e}")

print("Bot is running and listening for signals...")
client.start()
client.run_until_disconnected()
