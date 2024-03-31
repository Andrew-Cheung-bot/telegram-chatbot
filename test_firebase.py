import firebase_admin
from firebase_admin import db
import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')

cred_object = firebase_admin.credentials.Certificate('./firebase.json')
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL': config['FIREBASE']['URL']
})

def remove_all():
    ref = db.reference("/")
    ref.delete()
    print('Database is empty now!')

def init_db():
    # this id is fake, just for testing.
    telegram_user_id = '541221345'
    # replace {author},{director}, {book_name}, {movie_name} by actual values.
    books = db.reference(f'{telegram_user_id}/books/author/book_name/note')
    movies = db.reference(f'{telegram_user_id}/movies/director/movie_name/note')
    books.set('')
    movies.set('')

if __name__ == '__main__':
    # init_db()
    # remove_all()
    res = json.dumps(db.reference("/").get(), indent=4)
    print(res)
