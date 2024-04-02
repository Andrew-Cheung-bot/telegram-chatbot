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
from tabulate import tabulate
import json
import os


class StoreNote():
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config.ini')
        cred_object = firebase_admin.credentials.Certificate(
            '/etc/secrets/firebase.json')
        # cred_object = firebase_admin.credentials.Certificate(
        #     './firebase.json')
        default_app = firebase_admin.initialize_app(cred_object, {
            'databaseURL': os.environ['URL']
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

    def list_books(self, update: Update, context: CallbackContext) -> None:
        getbooks = db.reference(f'{update.message.from_user.id}/books/')
        data = getbooks.get()
        # print(data)
        # parsed_data = json.load(getbooks.get())
        table_data = [["Author", 'Name', "Note"]]
        for author in data:
            # print(author)
            for bookname in data.get(author):
                # print(bookname)
                table_data.append([author, bookname, data.get(
                    author).get(bookname).get('note')])
        table = tabulate(table_data, headers='firstrow', tablefmt='pipe')
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)

    def list_movies(self, update: Update, context: CallbackContext) -> None:
        getmovies = db.reference(f'{update.message.from_user.id}/movies/')
        data = getmovies.get()
        # print(data)
        # parsed_data = json.load(getbooks.get())
        table_data = [["Director", 'Name', "Note"]]
        for director in data:
            # print(author)
            for moviename in data.get(director):
                # print(bookname)
                table_data.append([director, moviename, data.get(
                    director).get(moviename).get('note')])
        table = tabulate(table_data, headers='firstrow', tablefmt='pipe')
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2)
