""" Настройки сервиса.
"""
from os import getenv
from pymongo import MongoClient

from database import date_base, date_base_mongo


SERVICE_HOST = getenv("SERVICE_HOST", "127.0.0.1")
SERVICE_PORT = getenv("SERVICE_PORT", "5000")

MONGO_HOST = getenv('MONGO_HOST')
MONGO_PORT = getenv('MONGO_PORT')
MONGO_DB = getenv('MONGO_DB')

DB_NAME = "rolgroup"



db = date_base(DB_NAME)


client = MongoClient(MONGO_HOST, int(MONGO_PORT))
db_mongo = date_base_mongo(client, mongo_db=MONGO_DB)


