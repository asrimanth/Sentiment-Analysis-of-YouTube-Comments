#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import googleapiclient.discovery
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import textblob
get_ipython().run_line_magic('matplotlib', 'inline')
max_results = 100


# In[2]:


def fetch_from_api(video_id):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    """A method which returns the data from the youtube api based on the video ID.
    
    Returns:
        dict -- A response object which contains comments along with metadata regarding the actual comments.
    """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCPNnBpoMxuNhpVQq8qikF58DT26CuFvBk"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,#_VB39Jo8mAQ
        maxResults=max_results,
        order="relevance"
    )
    response = request.execute()
    return response


# In[3]:


data = dict(fetch_from_api(video_id = "IBe2o-cZncU"))
print(data.keys()) 


# In[4]:

"""A procedure which takes response as input and extracts the comments along with the date and time.

Returns:
    dataframe -- A pandas dataframe containing coment , like count and update time.
"""
video_id_list = ["IBe2o-cZncU", "pl-tBjAM9g4", "Wo5dMEP_BbI", "vu8ZsKK6AWA", "kVPPzi5ZGts", 
                 "lZAoFs75_cs", "DQDLbl8sTtg", "eN9Lb3vXsAw", "eMtHmKO8GsA", "4R0uqG4NXPA",
                 "PArFP7ZJrtg", "bGUVQaBdxKw", "s_L-fp8gDzY", "IHZwWFHWa-w", "TnUYcTuZJpM"]      
total_video_list = []
comment_id_list = []
comment_list = []
like_count_list = []
latest_update_time = []
for i in range(len(video_id_list)):
    v_list = [video_id_list[i]] * max_results
    total_video_list.extend(v_list)
    data = dict(fetch_from_api
(video_id = video_id_list[i]))
    
    for j in range(max_results):
        try:
            item_dict = data['items'][j]
            snippet = dict(item_dict['snippet'])
            comment_parent_dict = snippet['topLevelComment']
            comment_dict = comment_parent_dict['snippet']
            comment_id_list.append(comment_dict['authorChannelId']['value'])
            comment_list.append(comment_dict['textOriginal'])
            like_count_list.append(comment_dict['likeCount'])
            latest_update_time.append(comment_dict['updatedAt'])
        except Exception as e:
            print("ID : {}\nMax res : {}\nj : {}".format(video_id_list[i], max_results, j))


# In[5]:


extracted_data = {'video_id':total_video_list,'user_id':comment_id_list, 'comment':comment_list, 'likes':like_count_list, 'last_update_time': latest_update_time}
df = pd.DataFrame(extracted_data)
df


# In[6]:


def remove_next_line_chars(input_text):
    input_text = ' '.join([i.strip() for i in input_text.split('\n')])
    return input_text


# In[7]:


df_work = df.copy()
df_work['comment'] = df_work['comment'].apply(remove_next_line_chars)
df_work.head()


# In[8]:


from textblob import TextBlob
sentiment_list = []
for comment in df_work['comment']:
    blob = TextBlob(comment)
    sentiment_list.append(blob.sentiment.polarity)

print(sentiment_list)


# In[9]:


sentiment_df = pd.DataFrame({'sentiment':sentiment_list})
sentiment_df.head()


# In[10]:


df_work['sentiment'] = sentiment_df


# In[11]:


def labeler(polarity):
    if(polarity > 0.3):
        return "positive"
    elif(polarity < -0.3):
        return "negative"
    else:
        return "neutral"


# In[12]:


df_work['sentiment_label'] = df_work['sentiment'].apply(labeler)
df_work.head()


# In[13]:

# Saving the work
df_work.to_csv('ytube_dataset.csv')
