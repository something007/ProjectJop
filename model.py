import base64
from datetime import date
import uuid
import matplotlib.pyplot as plt
import pandas as pd
import requests
import tweepy
from wordcloud import WordCloud, STOPWORDS
import os

consumer_key = 'fJnRMw94tSkeHtYGuhsNGMC67'
consumer_secret = '33DhsTyu82f3cbB2KQgrwgIV7uDEQaLbGMe0z1dYLGp1AmxNvn'
access_token = '1241963014208684032-the0kiD7BHE0WmvfG5IIwU3cZsRqxP'
access_token_secret = 'aGlAKc104IXX73MDqB3ion0jhglB9LaNXOLDWAWf3soNF'

key_secret = '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)
auth_headers = {
    'Authorization': 'Basic {}'.format(b64_encoded_key),
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
}
auth_data = {
    'grant_type': 'client_credentials'
}
auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
print(auth_resp.status_code)
access_token = auth_resp.json()['access_token']


trend_headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}
#Globel = 1
#Thailand WOEID = 23424960
trend_params = {
    'id' : 23424960,
}

trend_url = 'https://api.twitter.com/1.1/trends/place.json'
trend_resp = requests.get(trend_url,headers = trend_headers,params= trend_params)

tweet_data = trend_resp.json()


list2 = []
for i in range(0,10):
    list2.append(tweet_data[0]['trends'][i])
    dftop10 = pd.DataFrame(list2)
print(dftop10)

top = os.path.abspath(os.path.join('output','Top10','Top10_')) + str(date.today()) + '.csv'
print(top)
dftop10.to_csv(top, encoding="utf-8")


api = tweepy.API(auth, wait_on_rate_limit=True)

print(dftop10.iloc[:,[0,4]])

for x in range(0, 10):
    query = dftop10.iloc[x, 0]
    print(query)

    df = pd.DataFrame(columns=["create_at", "text", "hashtag", "retweet_count", "favourite_count"])

    for tweet in tweepy.Cursor(api.search, q=query, count=100, result_type="recent", tweet_mode='extended').items(1000):
        entity_hashtag = tweet.entities.get('hashtags')
        hashtag = ""
        for i in range(0, len(entity_hashtag)):
            hashtag = hashtag + "/" + entity_hashtag[i]["text"]
        re_count = tweet.retweet_count
        create_at = tweet.created_at
        try:
            text = tweet.retweeted_status.full_text
            fav_count = tweet.retweeted_status.favorite_count
        except:
            text = tweet.full_text
            fav_count = tweet.favorite_count
        new_column = pd.Series([create_at, text, hashtag, re_count, fav_count], index=df.columns)
        df = df.append(new_column, ignore_index=True)

        ra = os.path.abspath(os.path.join( 'output', 'Hashtag','Hashtag_')) + str(date.today()) + '_{}.csv'
        ra = ra.format(query)
        ra = ra.replace('#','')
        df.to_csv(ra, encoding="utf-8")

    data = pd.read_csv(ra, header=0)
    print(data)
    path = os.path.abspath(os.path.join('13ThaiFonts','THSarabun.ttf'))
    # path = r'C:\Users\JED\PycharmProjects\web_browser\13ThaiFonts\THSarabun.ttf'
    regexp = r"[ก-๙a-zA-Z']+"
    comment_words = ''
    stop_words = ["https", "co", "RT", "T", "#"] + list(STOPWORDS)

    for i in data.text:
        i = str(i)
        separate = i.split()
        for j in range(len(separate)):
            separate[j] = separate[j].lower()

        comment_words += " ".join(separate) + " "

    final_wordcloud = WordCloud(width=800, height=800, font_path=path, regexp=regexp,
                                background_color='white',
                                stopwords=stop_words,
                                min_font_size=10).generate(comment_words)

    ru = os.path.abspath(os.path.join( 'output','Wordcloud','Wordcloud' )) + str(date.today()) + "_" + '{}.png'
    ru = ru.format(query)
    ru = ru.replace('#', '')

    final_wordcloud.to_file(ru)
    plt.figure(figsize=(7, 10), facecolor=None)
    plt.imshow(final_wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)


    df = pd.DataFrame(None)
