from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import re
import emoji
import model as m

text_data = m.df['comment_text'].astype(str).values
m.vectorizer.adapt(text_data)

load_dotenv()
API_KEY = os.getenv('API_KEY')
if API_KEY is None:
    raise ValueError("API_KEY not found. Please check your .env file.")

youtube = build('youtube', 'v3', developerKey=API_KEY)

def fetch_videodetails(video_url: str):
    video_id = video_url.split('v=')[-1][:11]  # Extract video ID from URL

    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    video_snippet = video_response['items'][0]['snippet']
    uploader_channel_id = video_snippet['channelId']
    uploader_channel_title = video_snippet['channelTitle']
    uploader_video_title = video_snippet['title']

    return uploader_channel_id, uploader_channel_title, uploader_video_title

def fetch_comments(video_url: str, max_comments: int = 6000):
    video_id = video_url.split('v=')[-1][:11]  # Extract video ID from URL

    comments = []
    nextPageToken = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            maxResults=100,
            pageToken=nextPageToken
        )
        response = request.execute()
        
        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append(comment['textDisplay'])

        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break

    return comments[:max_comments]  # Return only up to max_comments


def process_comments(comments):
    hyperlink_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    threshold_ratio = 0.65
    relevant_comments = []

    for comment_text in comments:
        comment_text = comment_text.lower().strip()
        emojis_count = emoji.emoji_count(comment_text)
        text_characters = len(re.sub(r'\s', '', comment_text))

        if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
            if emojis_count == 0 or (text_characters / (text_characters + emojis_count)) > threshold_ratio:
                relevant_comments.append(comment_text)

    return relevant_comments


def classify_comments(comments):
    rf_int = pd.DataFrame(columns=['index', 'comment_text', 'toxic',
                                   'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate'])

    rf_bool = pd.DataFrame(columns=['index', 'comment_text', 'is_toxic',
                                    'is_severe_toxic', 'is_obscene', 'is_threat', 'is_insult', 'is_identity_hate'])

    for index, item in enumerate(comments):
        input_text = m.vectorizer(item)
        res = m.model.predict(np.expand_dims(input_text, 0))

        toxic, severe_toxic, obscene, threat, insult, identity_hate = map(
            float, res[0])

        new_row_int = pd.DataFrame([{
            'index': index,
            'comment_text': item,
            'toxic': toxic,
            'severe_toxic': severe_toxic,
            'obscene': obscene,
            'threat': threat,
            'insult': insult,
            'identity_hate': identity_hate
        }])

        new_row_bool = pd.DataFrame([{
            'index': index,
            'comment_text': item,
            'is_toxic': toxic > 0.5,
            'is_severe_toxic': severe_toxic > 0.5,
            'is_obscene': obscene > 0.5,
            'is_threat': threat > 0.5,
            'is_insult': insult > 0.5,
            'is_identity_hate': identity_hate > 0.5
        }])

        # Concatenate the new rows into both dataframes
        rf_int = pd.concat([rf_int, new_row_int], ignore_index=True)
        rf_bool = pd.concat([rf_bool, new_row_bool], ignore_index=True)

    return rf_int, rf_bool