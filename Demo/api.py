from pymongo import MongoClient
from bson.objectid import ObjectId
import time

import settings

client = MongoClient('mongodb://localhost:27017/')
mydb = client.mydatabase
account = mydb.account
customers = mydb.customers
list_people = mydb.list_people
user = mydb.user
list_project =mydb.list_project
list_team =mydb.list_team



