import os
import pandas as pd
from datetime import datetime, timedelta
from monfun import cnx,set_ip
from twifun import get_data,get_data2
from keep_run import keep_alive

mongod_connect = os.environ['CNX']
consumer_key        =os.environ['API_KEY']
consumer_secret     =os.environ['API_SECRET']
access_token        =os.environ['ACCESS_TOKEN']
access_token_secret =os.environ['ACCESS_SECRET']
bearer_token        =os.environ['BEARER_TOKEN']
atlas_group_id = os.environ['PROJECT_ID']
atlas_api_key_public = os.environ['PUBLIC_KEY']
atlas_api_key_private = os.environ['PRIVATE_KEY']

#twitter arg 
keyword = "inwi (lang:fr OR lang:ar)"
max_results = 100

keep_alive()
#cnx to mongodb
deleteAfterDate=(datetime.now()+timedelta(hours=3,minutes=5)).isoformat()
set_ip(atlas_group_id, atlas_api_key_public, atlas_api_key_private,deleteAfterDate)
ctweet=cnx(mongod_connect)
#get twitter data:
end_time= datetime.now().strftime("%Y-%m-%dT%H:")+"00:00Z"
tweets_data = get_data(keyword,end_time,max_results,bearer_token)
df = pd.json_normalize(tweets_data) 
since_id_new = tweets_data[-1]['id']

clx={}
for i in tweets_data:
    try:
        clx[i["id"]]=i
      #print(i["created_at"])
    except Exception as e:
        print(e)
        pass

since_id_old = 0
while(since_id_new != since_id_old):
    try:
        since_id_old = since_id_new
        tweets_data = get_data2(keyword,since_id_new,max_results,bearer_token)
        since_id_new = tweets_data[-1]['id']
        for i in tweets_data:
            try:
              clx[i["id"]]=i
              #print(i["created_at"])
            except:
                pass
    except:
        pass

print('New records',len(clx))

for x in clx:
  ctweet.delete_one({ "id": x })
  ctweet.insert_one(clx[x])

print('collection',ctweet.count_documents({}))
print('Done at ',datetime.now().strftime("%Y-%m-%dT%H:%M"))