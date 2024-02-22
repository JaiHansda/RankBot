import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot_token = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(bot_token)
webhook_url = os.environ.get('WEBHOOK_URL')

users_exp = {}
users_level = {}
users_guild = {}

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.from_user.id
    if user_id not in users_exp:
        users_exp[user_id] = 0
        users_level[user_id] = 0
        users_guild[user_id] = 'No Guild'
    
    users_exp[user_id] += 10
    if users_exp[user_id] >= 1000:
        users_exp[user_id] = 0
        users_level[user_id] += 1
    
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
    bot.reply_to(message, f"Level: {level}\nGuild: {guild}")

...

if __name__ == '__main__':
    bot.remove_webhook()
    bot.polling(none_stop=True)
