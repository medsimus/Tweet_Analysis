import os
from datetime import datetime, timedelta
import time
import pandas as pd
from monfun import cnx,set_ip
from twifun import get_data,get_data2
from keep_run import keep_alive

mongod_connect = os.environ['cnx']
consumer_key        =os.environ['api_key']
consumer_secret     =os.environ['api_secret']
access_token        =os.environ['access_token']
access_token_secret =os.environ['access_secret']
bearer_token        =os.environ['bearer_token']
atlas_group_id = os.environ['project_id']
atlas_api_key_public = os.environ['public_key']
atlas_api_key_private = os.environ['private_key']

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
while since_id_new != since_id_old:
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
    #time.sleep(10800)
  #for document in ctweet.find():
  #  clx_old[document['id']]=document
  #  del clx_old[document['id']]['_id']
  #clx_old.update(clx_new)
  



      