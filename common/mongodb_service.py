from pymongo import MongoClient, errors
from pymongo.collection import Collection
from pymongo.database import Database

from common import log

MAX_POOL_SIZE = 5


def get_client(host: str, port: int) -> MongoClient:
	try:
		client = MongoClient(host, port, maxPoolSize=MAX_POOL_SIZE)
		log.info("Mongodb Connected successfully!!!")
		return client
	except errors.ConnectionFailure as e:
		log.error(e)


def get_db(client: MongoClient, db_name: str) -> Database:
	try:
		db = Database(client, db_name)
		return db
	except Exception as e:
		log.error(e)


def get_collection(db: Database, name: str) -> Collection:
	collection = Collection(db, name)
	return collection


def insert(collection: Collection, data):
	collection.insert_one(data)


def insert_all(collection: Collection, data):
	collection.insert_many(data)


def delete_all_data(collection: Collection):
	collection.delete_many({})
