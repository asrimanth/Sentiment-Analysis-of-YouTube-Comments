# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import googleapiclient.discovery

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCPNnBpoMxuNhpVQq8qikF58DT26CuFvBk"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId="IBe2o-cZncU", #_VB39Jo8mAQ
        maxResults=50,
        order="relevance"
    )
    response = request.execute()

    return response

if __name__ == "__main__":
    data = dict(main())
    comment_list = []
    for i in range(len(data)):
        item_dict = data['items'][i]
        snippet = dict(item_dict['snippet'])
        comment_dict = snippet['topLevelComment']
        comment_list.append(comment_dict['snippet']['textOriginal'])
        
    print(comment_list)
