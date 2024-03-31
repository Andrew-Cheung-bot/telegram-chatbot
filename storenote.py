import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import re
from firebase_admin import firestore
import configparser
from telegram import ParseMode, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)
from datetime import datetime


class StoreNote():
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        cred_object = firebase_admin.credentials.Certificate('./firebase.json')
        default_app = firebase_admin.initialize_app(cred_object, {
            'databaseURL': config['FIREBASE']['URL']
        })

    def store_book_notes(self, update: Update, context: CallbackContext) -> None:
        try:
            book_name, book_author, note = context.args
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            set_date = db.reference(
                f'{update.message.from_user.id}/books/{book_author}/{book_name}/modify_date')
            set_note = db.reference(
                f'{update.message.from_user.id}/books/{book_author}/{book_name}/note')
            set_date.set(current_time)
            set_note.set(note)
            context.bot.send_message(
                chat_id=update.message.from_user.id, text='Note has been uploaded.')
        except:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='Usage: /booknote <Name> <Author> <note>')
            
    def store_movie_notes(self, update: Update, context: CallbackContext) -> None:
        try:
            movie_name, movie_author, note = context.args
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            set_date = db.reference(
                f'{update.message.from_user.id}/movies/{movie_author}/{movie_name}/modify_date')
            set_note = db.reference(
                f'{update.message.from_user.id}/movies/{movie_author}/{movie_name}/note')
            set_date.set(current_time)
            set_note.set(note)
            context.bot.send_message(
                chat_id=update.message.from_user.id, text='Note has been uploaded.')
        except:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text='Usage: /moviecomment <Name> <Author> <note>')
