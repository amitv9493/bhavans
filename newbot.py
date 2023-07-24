import logging
from telegram import Update
import requests
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler, filters

TOKEN = "5868277941:AAFEzdZhlae1gMLso5LPj-NHmuH0-TxM_10"

def get_token(username, password):
    
    endpoint = "https://smhri.com/oeccrm/api/user/login/"

    request = requests.post(endpoint, data={"username":username, "password":password})
    
    if request.status_code == 200:
        return request.json().get("token")
    else:
        raise Exception("Failed to get token. Invalid response from the server.")
        
    
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

'''
            login system
'''
users = {}

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(chat_id)
    if chat_id in users:
        await context.bot.send_message(chat_id=chat_id, text="You are already logged in!")
        return

    await context.bot.send_message(chat_id=chat_id, text="Please enter your username:")
    context.user_data['login_step'] = 1  # Setting the login step to 1
    
async def process_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.message.text.strip().lower()  # Convert username to lowercase for case-insensitivity

    if context.user_data.get('login_step') == 1:
        context.user_data['username'] = username
        context.user_data['login_step'] = 2 
        await context.bot.send_message(chat_id=chat_id, text="Please enter your password:")
        
async def process_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    password = update.message.text.strip()

    # if context.user_data.get('login_step') == 2:
    #     username = context.user_data.get('username')
    #     # Replace the following logic with your actual login authentication logic
    #     token = get_token(username, password)
    #     if token:
    #         users[chat_id] = context.user_data[token]  # Store the user as logged in
    await context.bot.send_message(chat_id=chat_id, text="Login successful!")
    # else:
        # await context.bot.send_message(chat_id=chat_id, text="Login failed. Invalid username or password.")

        # context.user_data.clear()  #

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    
async def caps(Update:Update, context: ContextTypes.DEFAULT_TYPE ):
    
    print(context.args)
    chat_id = Update.effective_chat.id
    print(chat_id)
    
    if not chat_id in users:
        username = context.args[0].strip()
        password = context.args[1].strip()
        
        token = get_token(username, password)
        
    else:
        await context.bot.send_message(chat_id=chat_id, text="You are already logged in!")
        return
    # await context.bot.send_message(chat_id=Update.effective_chat.id, text=text) 
    
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('caps', caps)
    login_handler = CommandHandler('login', login)
    process_password_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), process_password)
    process_username_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), process_username)

    
    application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(login_handler)
    application.add_handler(process_username_handler)
    application.add_handler(process_password_handler)

    application.add_handler(unknown_handler) # Lways put this handler to the las
    
    application.run_polling()   
    
'''
    
login - Login 
add_enquiry - Add Enquiry
view_all-enquiries - View all enquiries
add_application - Add Application
search_university - Search University
logout - Logout
'''