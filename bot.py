import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot_token = '6800038806:AAHWUqskk6A0Ht2vhRhk-kN3_OmFAERpGIQ'
bot = telebot.TeleBot(bot_token)

users_exp = {}
users_level = {}
users_rewards = {}
users_guild = {}

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    if user_id not in users_exp:
        users_exp[user_id] = 0
        users_level[user_id] = 0
        users_rewards[user_id] = []
        users_guild[user_id] = 'No Guild'

    users_exp[user_id] += 10
    if users_exp[user_id] >= 1000:
        users_exp[user_id] = 0
        users_level[user_id] += 1
        users_rewards[user_id].append("Naruto Headband")
    
    if "spam" in message.text.lower():
        users_exp[user_id] -= 50
        if users_exp[user_id] < 0:
            users_exp[user_id] = 0

@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    user_id = call.message.chat.id
    action = call.data.split(':')[0]
    target_user_id = int(call.data.split(':')[1])

    if action == 'give_exp':
        users_exp[target_user_id] += 50
    elif action == 'take_exp':
        users_exp[target_user_id] -= 50
        if users_exp[target_user_id] < 0:
            users_exp[target_user_id] = 0

@bot.message_handler(commands=['profile'])
def profile(message):
    user_id = message.from_user.id
    level = users_level[user_id]
    guild = users_guild[user_id]
    rewards = ', '.join(users_rewards[user_id])
    bot.reply_to(message, f"Level: {level}\nGuild: {guild}\nRewards: {rewards}")

@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
    sorted_users = sorted(users_exp, key=lambda x: users_exp[x], reverse=True)
    leaderboard_text = "Leaderboard:\n"
    for i, user_id in enumerate(sorted_users[:10]):
        username = bot.get_chat_member(message.chat.id, user_id).user.username
        leaderboard_text += f"{i+1}. {username} - Level {users_level[user_id]}\n"
    
    bot.reply_to(message, leaderboard_text)

@bot.message_handler(commands=['guild'])
def set_guild(message):
    guild_name = message.text.split()[-1]
    user_id = message.from_user.id
    users_guild[user_id] = guild_name
    bot.reply_to(message, f"You have joined the guild: {guild_name}")

@bot.message_handler(commands=['help'])
def help(message):
    help_text = "Available commands:\n/profile - View your profile\n/leaderboard - View the leaderboard\n/guild [name] - Join a guild\n/help - Show this help message"
    bot.reply_to(message, help_text)

bot.polling()
