## this file is based on version 13.7 of python telegram chatbot
## and version 1.26.18 of urllib3
## chatbot.py
import telegram
from telegram import ParseMode, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
CallbackContext)
import configparser
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import re
from firebase_admin import firestore

global chatgpt
def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('./firebase.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': config['FIREBASE']['URL']
    })


    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("books", books))
    dispatcher.add_handler(CommandHandler("movies", movies))
    # dispatcher.add_handler(CommandHandler("records", records))
    dispatcher.add_handler(CommandHandler("help",help))
    
    # To start the bot:
    updater.start_polling()
    updater.idle()


def help(update: Update, context: CallbackContext) -> None:
    reply_message = "🤖 **Recommandtion Chatbot**\n" \
                    "🔹 **Version:** 0\.1\n" \
                    "🔹 **Commands:**\n" \
                    "   /books \- Get a list of recommended books by ChatGPT\.\n" \
                    "      \[arg0\] \- Type of book, otherwise GPT will return 4 different types of books\.\n" \
                    "   /movies \- Get a list of recommended movies by ChatGPT\.\n" \
                    "      \[arg0\] \- Type of movie, otherwise GPT will return 4 different types of movies\."
    context.bot.send_message(
        chat_id=update.message.from_user.id, text=reply_message, parse_mode=ParseMode.MARKDOWN_V2)


def books(update: Update, context: CallbackContext) -> None:
    if(context.args == []):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Tips: You can input the book type or leave it unspecified.')
        book_type = 'unspecified'
    else:
        book_type = context.args[0]
    
    global chatgpt
    reply_message = chatgpt.submit_books(book_type)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
    # print(reply_message)
    # book_name = re.search(r'"(.*?)"', reply_message, re.DOTALL).group(0)
    # author = re.search(r'\[(.*?)\]', reply_message, re.DOTALL).group(0)
    # print(book_name, author)
    # print('this is user_id: ',update.message.from_user.id)
    # book_name = book_name.replace("\"", "")
    # author = author.replace("[", "").replace("]", "")
    # print(book_name, author)


def movies(update: Update, context: CallbackContext) -> None:
    if (context.args == []):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Tips: You can input the movie type or leave it unspecified.')
        movie_type = 'unspecified'
    else:
        movie_type = context.args[0]

    global chatgpt
    reply_message = chatgpt.submit_movies(movie_type)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# def records(update, context):
#     dict_db = ref.get()
#     books = dict_db['book']
#     movies = dict_db['movie']
#     reply_message = f'You have search {len(books)-1} books and {len(movies)-1} movies. They are'
#     for book in books:
#         if book == 'Book_name':
#             continue
#         reply_message += f', {book} directed by {books[book]}'
#     for movie in movies:
#         if movie == "Movie_name":
#             continue
#         reply_message += f', {movie} directed by {movies[movie]}'
#     reply_message += '.'
#     context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def equiped_chatgpt(update: Update, context: CallbackContext) -> None:
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

    
if __name__ == '__main__':
    main()