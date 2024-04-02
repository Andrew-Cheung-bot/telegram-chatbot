# this file is based on version 13.7 of python telegram chatbot
# and version 1.26.18 of urllib3
# chatbot.py
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
from storenote import StoreNote
import os

global chatgpt
def main():
    # Load your token and create an Updater for your Bot
    # config = configparser.ConfigParser()
    # config.read('config.ini')
    updater = Updater(
        token=(os.environ['TELEGRAM_ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    sn = StoreNote()


    global chatgpt
    chatgpt = HKBU_ChatGPT()
    chatgpt_handler = MessageHandler(
        Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("books", books))
    dispatcher.add_handler(CommandHandler("movies", movies))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler(
        "booknote", sn.store_book_notes))
    dispatcher.add_handler(CommandHandler(
        "movienote", sn.store_movie_notes))
    dispatcher.add_handler(CommandHandler("listbooks", sn.list_books))
    dispatcher.add_handler(CommandHandler("listmovies", sn.list_movies))

    # To start the bot:
    updater.start_polling()
    # updater.start_webhook(listen='127.0.0.1',port=80,cert=None,key=None,url_path='/')
    updater.idle()


def help(update: Update, context: CallbackContext) -> None:
    reply_message = "🤖 **Recommandtion Chatbot**\n" \
                    "🔹 **Version:** 0\.1\n" \
                    "🔹 **Commands:**\n" \
                    "   /books \- Get a list of recommended books by ChatGPT\.\n" \
                    "      \[arg0\] \- Type of book, otherwise GPT will return 4 different types of books\.\n" \
                    "   /movies \- Get a list of recommended movies by ChatGPT\.\n" \
                    "      \[arg0\] \- Type of movie, otherwise GPT will return 4 different types of movies\.\n" \
                    "   /booknote \- Save a booknote to Cloud Database\.\n" \
                    "      \[arg0\] \- Book name\.\n" \
                    "      \[arg1\] \- Book author\.\n" \
                    "      \[arg2\] \- note\.\n" \
                    "   /movienote \- Save a movienote to Cloud Database\.\n" \
                    "      \[arg0\] \- Movie name\.\n" \
                    "      \[arg1\] \- Movie author\.\n" \
                    "      \[arg2\] \- note\.\n" \
                    "   /listbooks \- List all the book notes\.\n" \
                    "   /listmovies \- List all the movie notes\.\n" 
    context.bot.send_message(
        chat_id=update.message.from_user.id, text=reply_message, parse_mode=ParseMode.MARKDOWN_V2)


def books(update: Update, context: CallbackContext) -> None:
    if (context.args == []):
        context.bot.send_message(
            chat_id=update.effective_chat.id, text='Tips: You can input the book type or leave it unspecified.')
        book_type = 'unspecified'
    else:
        book_type = context.args[0]

    global chatgpt
    reply_message = chatgpt.submit_books(book_type)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)
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
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)


def equiped_chatgpt(update: Update, context: CallbackContext) -> None:
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)


if __name__ == '__main__':
    main()
