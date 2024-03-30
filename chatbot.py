## this file is based on version 13.7 of python telegram chatbot
## and version 1.26.18 of urllib3
## chatbot.py
import telegram
from telegram import Update
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

global redis1
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

    global db
    db.reference("/book").set({"Book_name": "Author"})
    db.reference("/movie").set({"Movie_name": "Director"})

    global ref
    ref = db.reference("/")
    print(ref.get())


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
    dispatcher.add_handler(CommandHandler("records", records))
    # To start the bot:
    updater.start_polling()
    updater.idle()


def books(update, context):
    global chatgpt
    reply_message = chatgpt.submit_books(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
    # print(reply_message)
    book_name = re.search(r'"(.*?)"', reply_message, re.DOTALL).group(0)
    author = re.search(r'\[(.*?)\]', reply_message, re.DOTALL).group(0)
    # print(book_name, author)
    book_name = book_name.replace("\"", "")
    author = author.replace("[", "").replace("]", "")
    print(book_name, author)
    global db
    if book_name:
        db.reference(f"/book/{book_name}").set(f"{author}")
    print(ref.get())

def movies(update, context):
    global chatgpt
    reply_message = chatgpt.submit_movies(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
    movie_name = re.search(r'"(.*?)"', reply_message, re.DOTALL).group(0)
    author = re.search(r'\[(.*?)\]', reply_message, re.DOTALL).group(0)
    # print(book_name, author)
    movie_name = movie_name.replace("\"", "")
    author = author.replace("[", "").replace("]", "")
    print(movie_name, author)
    global db
    if movie_name:
        db.reference(f"/movie/{movie_name}").set(f"{author}")
    print(ref.get())

def records(update, context):
    dict_db = ref.get()
    books = dict_db['book']
    movies = dict_db['movie']
    reply_message = f'You have search {len(books)-1} books and {len(movies)-1} movies. They are'
    for book in books:
        if book == 'Book_name':
            continue
        reply_message += f', {book} directed by {books[book]}'
    for movie in movies:
        if movie == "Movie_name":
            continue
        reply_message += f', {movie} directed by {movies[movie]}'
    reply_message += '.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

#

def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

    
if __name__ == '__main__':
    main()