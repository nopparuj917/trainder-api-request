import os
import pymongo
from dotenv import load_dotenv
import requests

load_dotenv()
password = os.environ.get('MONGODB_PASSWORD')
api_key = os.environ.get('GOOGLE_MAPS_API_KEY')


def geocode(address):
    response = requests.get(
        f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}')
    if response.status_code == 200:
        data = response.json()
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        return 0, 0


dbname = 'trainder'
connstr = 'mongodb+srv://ta:' + password + \
    '@cluster0.vcni3ya.mongodb.net/' + dbname
client = pymongo.MongoClient(connstr)
collection = client[dbname]['users']
cursor = collection.find({})


def add_lat_lng():
    for document in cursor:
        address = document.get('address')
        lat, lng = geocode(address)
        collection.update_one(
            {'_id': document['_id']},
            {'$set': {'lat': lat, 'lng': lng}}
        )


def rename_lat_lng():
    collection.update_many(
        {}, {'$rename': {'latitude': 'lat', 'longitude': 'lng'}})


