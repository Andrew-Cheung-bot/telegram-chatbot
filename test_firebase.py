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


res = json.dumps(db.reference("/").get(),indent=4)
print(res)