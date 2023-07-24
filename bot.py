import os

import telebot
import requests
import pickle
import json

# https://smhri.com/oeccrm/api/enquiries/

BOT_TOKEN = os.environ.get("BOT_TOKEN")

TOKEN = "5868277941:AAFEzdZhlae1gMLso5LPj-NHmuH0-TxM_10"

bot = telebot.TeleBot(TOKEN)

def read_token():
    pass

def get_token(username, password):
    endpoint = "https://smhri.com/oeccrm/api/user/login/"

    request = requests.post(endpoint, data={"username": username, "password": password})

    if request.status_code == 200:
        return request.json().get("token")
    else:
        raise Exception("Failed to get token. Invalid response from the server.")




# Handler function for the /login command
@bot.message_handler(commands=["login"])
def start(message):
    bot.send_message(message.chat.id, "Hi! I am your bot. Please enter your username.")
    bot.register_next_step_handler(message, receive_username)


def receive_username(message):
    username = message.text
    bot.send_message(message.chat.id, "Thanks! Now, please enter your password.")
    bot.register_next_step_handler(message, receive_password, username)


def receive_password(message, username):
    password = message.text

    bot.send_message(message.chat.id, f"Username: {username}\nPassword: {password}")
    bot.send_message(message.chat.id, "Logging you please wait.....")
    # bot.register_next_step_handler(message, login, username, password)
    login(message, username, password)
    



def login(message, username, password):
    try:
        token = get_token(username, password)
        if len(token.get("access")) > 0:
            access_token = token.get("access")
            with open(f"{message.chat.id}.pkl", "wb") as file:
                pickle.dump(access_token, file)
            bot.send_message(message.chat.id, "Login Successful!")

        else:
            bot.send_message(message.chat.id, "Login unccessful Please check your username and password......")

    except:
        bot.reply_to(message, "Failed to connect to the server!")
        
@bot.message_handler(commands=["logout"])
def logout(message):
    file_name = f"{message.chat.id}.pkl"
    if os.access(file_name, os.F_OK):
        os.remove(file_name)
        bot.send_message(message.chat.id, " Logout Successfully!.")
    bot.send_message(message.chat.id, "You are not logged In.")
    
        
@bot.message_handler(commands='view_all')

def show_enquiries():
    headers = {
        'Authorization': 'Bearer ',
        'Content-Type': 'application/json'
    }
    url = 'https://www.smhri.com/api/enquiries/'
    # data = None
    
    requests.post(url,headers=headers)
# You can perform authentication or any other logic here


@bot.message_handler(commands=["hello"])
def handle_start(message):
    web_link = "https://startup.anantsoftcomputing.com/oeccrm"
    web_app = telebot.types.WebAppInfo(url=web_link)
    reply_markup = telebot.types.InlineKeyboardMarkup()
    web_app_button = telebot.types.InlineKeyboardButton(text="Hello", web_app=web_app)
    # web_app_button = telebot.types.InlineKeyboardButton(text="Web App", url=telebot.types.InlineKeyboardUrl(web_link))
    reply_markup.add(web_app_button)
    bot.send_message(message.chat.id, "Welcome :)))))", reply_markup=reply_markup)


@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    bot.send_message(
        message.chat.id, "I don't understand that command. Please use /login and then try other commands."
    )


bot.infinity_polling()
