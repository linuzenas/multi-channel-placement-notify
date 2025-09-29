#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to get Telegram group ID for the placement group.
"""

import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '8462103585:AAE_oaonQCq2Dt9FncbpdIatjSaFSXnKlAM')

async def get_group_id():
    """Get the group ID by sending a test message."""
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        
        print("🤖 Telegram Bot Information:")
        print(f"Bot Token: {TELEGRAM_TOKEN[:10]}...")
        
        # Get bot info
        bot_info = await bot.get_me()
        print(f"Bot Username: @{bot_info.username}")
        print(f"Bot Name: {bot_info.first_name}")
        
        print("\n📋 Instructions:")
        print("1. Add this bot to your placement group")
        print("2. Make the bot an admin in the group")
        print("3. Send any message in the group")
        print("4. Run this script again to get the group ID")
        
        # Get updates to find group ID
        updates = await bot.get_updates()
        
        if updates:
            print("\n📨 Recent messages:")
            for update in updates[-5:]:  # Show last 5 updates
                if update.message:
                    chat = update.message.chat
                    print(f"Chat ID: {chat.id}")
                    print(f"Chat Type: {chat.type}")
                    print(f"Chat Title: {getattr(chat, 'title', 'N/A')}")
                    print(f"Message: {update.message.text[:50]}...")
                    print("-" * 40)
        else:
            print("\n❌ No recent messages found.")
            print("Please send a message in the group and try again.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if the bot token is correct")
        print("2. Make sure the bot is added to the group")
        print("3. Ensure the bot has permission to read messages")

if __name__ == '__main__':
    print("🔍 Getting Telegram Group ID...")
    print("=" * 50)
    asyncio.run(get_group_id())
