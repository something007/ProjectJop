import os
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd
import tweepy
from wordcloud import WordCloud, STOPWORDS

consumer_key = 'fJnRMw94tSkeHtYGuhsNGMC67'
consumer_secret = '33DhsTyu82f3cbB2KQgrwgIV7uDEQaLbGMe0z1dYLGp1AmxNvn'
access_token = '1241963014208684032-the0kiD7BHE0WmvfG5IIwU3cZsRqxP'
access_token_secret = 'aGlAKc104IXX73MDqB3ion0jhglB9LaNXOLDWAWf3soNF'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

query = input("Hashtag : ")
querun = query
query = "#"+query

df = pd.DataFrame(columns=["create_at","text","hashtag","retweet_count","favourite_count"])

for tweet in tweepy.Cursor(api.search,q=query,count=100,result_type="recent",tweet_mode='extended').items(1000):
    entity_hashtag = tweet.entities.get('hashtags')
    hashtag = ""
    for i in range(0,len(entity_hashtag)):
        hashtag = hashtag +"/"+entity_hashtag[i]["text"]
    re_count = tweet.retweet_count
    create_at = tweet.created_at
    try:
        text = tweet.retweeted_status.full_text
        fav_count = tweet.retweeted_status.favorite_count
    except:
        text = tweet.full_text
        fav_count = tweet.favorite_count
    new_column = pd.Series([create_at,text,hashtag,re_count,fav_count], index=df.columns)
    df = df.append(new_column,ignore_index=True)

ra = os.path.abspath(os.path.join( 'output', 'hashtag_man','hashtag_man')) + str(date.today()) + '_{}.csv'

ra = ra.format(querun)
df.to_csv(ra,encoding="utf-8")
print("ra",ra)

data = pd.read_csv(ra,header=0)
print(data)
path = os.path.abspath(os.path.join('13ThaiFonts','THSarabun.ttf'))
regexp = r"[ก-๙a-zA-Z']+"
comment_words = '' 
stop_words = ["https", "co", "RT","T"] + list(STOPWORDS)


for i in data.text:
    i = str(i) 
    separate = i.split()
    for j in range(len(separate)): 
        separate[j] = separate[j].lower() 

    comment_words += " ".join(separate)+" "

final_wordcloud = WordCloud(width = 800, height = 800,font_path=path,regexp=regexp,
                background_color ='white', 
                stopwords = stop_words,
                min_font_size = 10).generate(comment_words)

ru = os.path.abspath(os.path.join( 'output','Wordcloud_man','Wordcloud_man' ))+(str(date.today())+"_"+'{}.png'.format(querun))
final_wordcloud.to_file(ru)
plt.figure(figsize = (7, 10), facecolor = None) 
plt.imshow(final_wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 

plt.show()