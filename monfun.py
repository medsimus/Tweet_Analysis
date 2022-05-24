import pymongo
from pymongo import MongoClient
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]
def cnx(mongod_connect):
    client = MongoClient(mongod_connect)
    db = client.dbt 
    ctweet = db.clx
    #ctweet.drop()
    ctweet.create_index([("id", pymongo.ASCENDING)],unique = True)
    return ctweet

def set_ip(atlas_group_id, atlas_api_key_public, atlas_api_key_private, deleteAfterDate):
  resp = requests.post( "https://cloud.mongodb.com/api/atlas/v1.0/groups/{atlas_group_id}/accessList".format(atlas_group_id=atlas_group_id),
      auth=HTTPDigestAuth(atlas_api_key_public, atlas_api_key_private),
      json=[{'ipAddress': get_ip(), 
             'deleteAfterDate': deleteAfterDate,
             'comment': 'replit :'+str(datetime.now().strftime("%Y-%m-%dT%H"))}])
  if resp.status_code in (200, 201):
        print("MongoDB Atlas accessList request successful", flush=True)
  else:
      print("Request problem: status code : {status_code}, content : {content}".format(status_code=resp.status_code, content=resp.content),flush=True)
