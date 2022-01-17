"""Module to extract the dataframe of comments from a youtube url.

Raises:
    error_utils.InvalidURLException: Occurs when the url is not valid.

Returns:
    dataframe -- A pandas dataframe which contains 100 rows and following columns:
                'user_id', 'comment', 'likes', 'last_update_time'
"""

import os
import googleapiclient.discovery

import pandas as pd

import error_utils

MAX_RESULTS = 100
DEVELOPER_KEY = "AIzaSyCPNnBpoMxuNhpVQq8qikF58DT26CuFvBk"


def extract_video_id(url):
    """Extracts the video id from the input youtube url.

    Arguments:
        url {str} -- The input url from the user.
    """

    if "youtube" in url:
        # All the chars in "youtube" are found
        url_bits = url.split("watch?v=")
        if url_bits[1].find("&list="):
            # User has given a playlist url
            video_id = url_bits[1].split("&list=")[0]
        else:
            # A simple youtube url
            video_id = url_bits[1]
    elif "youtu.be" in url:
        # All the chars in "youtu.be" are found
        video_id = url.split(".be/")[1]

    else:
        message = "The url is not from youtube. Please try again!"
        raise error_utils.InvalidURLException(message)

    return video_id


def extract_from_ytube_api(video_id):
    """Returns a dictionary of nested hierarchy of youtube data.

    Arguments:
        video_id {str} -- The video id (extracted from the url)

    Returns:
        dict -- A youtube response object, which contains a lot of metadata.
    """

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    ytube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = ytube.commentThreads().list(
        part="snippet",
        videoId=video_id,  # Example: _VB39Jo8mAQ
        maxResults=MAX_RESULTS,
        order="relevance"
    )
    response = request.execute()
    return response


def return_df_from_data(url):
    """Returns a clean dataframe containing 100 rows of youtube comments.

    Arguments:
        url {str} -- A youtube url (either short or long)

    Returns:
        dataframe -- A pandas dataframe containing these columns :
                        'user_id', 'comment', 'likes', 'last_update_time'
    """
    video_id = extract_video_id(url)
    data = dict(extract_from_ytube_api(video_id))

    comment_id_list = []
    comment_list = []
    like_count_list = []
    latest_update_time = []

    for i in range(MAX_RESULTS):

        # See the youtube dict hierarchy in the notebook 'yTubeDemo.py' for more details.
        item_dict = data['items'][i]
        snippet = dict(item_dict['snippet'])
        comment_parent_dict = snippet['topLevelComment']
        comment_dict = comment_parent_dict['snippet']
        comment_id_list.append(comment_dict['authorChannelId']['value'])
        comment_list.append(comment_dict['textOriginal'])
        like_count_list.append(comment_dict['likeCount'])
        latest_update_time.append(comment_dict['updatedAt'])

    extracted_data = {'user_id': comment_id_list, 'comment': comment_list,
                      'likes': like_count_list, 'last_update_time': latest_update_time}
    dataframe = pd.DataFrame(extracted_data)
    return dataframe
