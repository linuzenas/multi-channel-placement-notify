#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Telegram connection with the correct group ID.
"""

import asyncio
from telegram import Bot
from telegram.error import TelegramError

# Configuration
TELEGRAM_TOKEN = ""
TELEGRAM_GROUP_ID = ""

async def test_telegram():
    """Test sending a message to the Telegram group."""
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        
        # Test message
        test_message = "🧪 **Test Message**\n\nThis is a test to verify the bot can send messages to the group.\n\n✅ If you see this message, Telegram is working properly!"
        
        print(f"🤖 Sending test message to group: {TELEGRAM_GROUP_ID}")
        print(f"📝 Message: {test_message}")
        
        # Send message
        await bot.send_message(chat_id=TELEGRAM_GROUP_ID, text=test_message)
        
        print("✅ SUCCESS: Message sent successfully to Telegram group!")
        print("📱 Check your 'Placement Updates' group for the test message.")
        
    except TelegramError as e:
        print(f"❌ ERROR: Failed to send message: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure the bot is added to the group")
        print("2. Make sure the bot is an admin in the group")
        print("3. Check if the group ID is correct")
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")

if __name__ == '__main__':
    print("🔍 Testing Telegram Connection...")
    print("=" * 50)
    asyncio.run(test_telegram())
