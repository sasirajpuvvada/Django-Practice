from pymongo import MongoClient
MONGO_DATABASE = "temp"
MONGO_ADMIN_PASSWORD = "test"
MONGO_ADMIN_USERNAME = "test"
MONGO_HOST = 'mongodb://' + MONGO_ADMIN_USERNAME + ':' + MONGO_ADMIN_PASSWORD + '@localhost:27017/'
MONGO_HOST_MASTER = 'mongodb://' + MONGO_ADMIN_USERNAME + ':' + MONGO_ADMIN_PASSWORD + '@localhost:27017/'


client = MongoClient(MONGO_HOST)
# db = client[MONGO_DATABASE]

# democlient = MongoClient()
# client = MongoClient('localhost',27017)