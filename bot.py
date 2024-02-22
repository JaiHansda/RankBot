from pyrogram import Client, filters
from pymongo import MongoClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
from datetime import datetime, timedelta

API_ID = os.environ.get("17271772")
API_HASH = os.environ.get("897542330c90728e4e7fef57f42f9c79")
BOT_TOKEN = os.environ.get("6800038806:AAHWUqskk6A0Ht2vhRhk-kN3_OmFAERpGIQ")
MONGO_URL = os.environ.get("mongodb+srv://Aditya:Aditya@cluster0.c3pct2l.mongodb.net/?retryWrites=true&w=majority")

bot = Client("GroupStatsBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

mongo_client = MongoClient(MONGO_URL)
db = mongo_client["GroupStatsBotDB"]

@bot.on_message(filters.group)
async def track_messages(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    user_data = db.users.find_one({"user_id": user_id, "chat_id": chat_id})
    if user_data:
        # Update user's message count
        db.users.update_one({"user_id": user_id, "chat_id": chat_id}, {"$inc": {"message_count": 1}})
    else:
        # Create user profile if it doesn't exist
        db.users.insert_one({"user_id": user_id, "chat_id": chat_id, "message_count": 1, "level": 1, "xp": 0, "labels": []})

@bot.on_message(filters.command(["profile"]))
async def view_profile(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    user_data = db.users.find_one({"user_id": user_id, "chat_id": chat_id})
    if user_data:
        level = user_data["level"]
        xp = user_data["xp"]
        message_count = user_data["message_count"]
        labels = user_data["labels"]
        await message.reply_text(f"Level: {level}\nXP: {xp}\nMessages: {message_count}\nLabels: {', '.join(labels)}", reply_markup=get_profile_buttons())
    else:
        await message.reply_text("You haven't sent any messages in this group yet.")

async def get_profile_buttons():
    keyboard = [
        [InlineKeyboardButton("Level Up", callback_data="level_up")],
        [InlineKeyboardButton("Leaderboard", callback_data="leaderboard")],
        [InlineKeyboardButton("Labels Locker", callback_data="labels_locker")],
        [InlineKeyboardButton("Challenges", callback_data="challenges")]
    ]
    return InlineKeyboardMarkup(keyboard)

@bot.on_callback_query()
async def handle_button_click(client, callback_query):
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id

    if callback_query.data == "level_up":
        # Handle level-up button click
        # Add logic for level-up rewards or actions
        pass
    elif callback_query.data == "leaderboard":
        # Handle leaderboard button click
        # Add logic to display the leaderboard
        pass
    elif callback_query.data == "labels_locker":
        # Handle labels locker button click
        # Add logic to display and manage labels
        pass
    elif callback_query.data == "challenges":
        # Handle challenges button click
        # Add logic to display and monitor challenges
        pass

# Add more commands, such as leaderboard, labels, challenges, etc.

bot.run()
  
