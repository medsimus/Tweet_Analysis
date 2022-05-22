import requests

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(keyword, end_date, max_results = 100):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {'query': keyword,
                    #'start_time': start_date,
                    'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,geo.place_id',
                    'media.fields': 'duration_ms,type,url,public_metrics',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
                    #'sort_order': 'recency,relevancy',
                    'next_token': {}}
    return (search_url, query_params)

def create_url2(keyword, last_tweet, max_results = 100):
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {'query': keyword,
                    #'start_time': start_date,
                    'until_id': last_tweet,
                    #'end_time': end_date,
                    'max_results': max_results,
                    'expansions': 'author_id,geo.place_id',
                    'media.fields': 'duration_ms,type,url,public_metrics',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
                    #'sort_order': 'recency,relevancy',
                    'next_token': {}}
    return (search_url, query_params)
  

def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_data(keyword,end_time,max_results,bearer_token):
  headers = create_headers(bearer_token)
  url = create_url(keyword, end_time, max_results)
  tweets = connect_to_endpoint(url[0], headers, url[1])
  return tweets['data']

def get_data2(keyword,last_tweet,max_results,bearer_token):
  headers = create_headers(bearer_token)
  url = create_url2(keyword, last_tweet, max_results)
  tweets = connect_to_endpoint(url[0], headers, url[1])
  return tweets['data'] 