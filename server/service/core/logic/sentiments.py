from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import io
import base64
from typing import List, Dict
import os


def analyze_sentiment(comments: List[str]) -> Dict:
    sentiment_object = SentimentIntensityAnalyzer()
    polarity = []
    positive_comments = []
    negative_comments = []
    neutral_comments = []

    for comment in comments:
        sentiment_dict = sentiment_object.polarity_scores(comment)
        polarity.append(sentiment_dict['compound'])

        if sentiment_dict['compound'] > 0.05:
            positive_comments.append(comment)
        elif sentiment_dict['compound'] < -0.05:
            negative_comments.append(comment)
        else:
            neutral_comments.append(comment)

    avg_polarity = sum(polarity) / len(polarity) if polarity else 0

    sentiment_summary = {
        "average_polarity": avg_polarity,
        "most_positive_comment": comments[polarity.index(max(polarity))] if polarity else "",
        "most_negative_comment": comments[polarity.index(min(polarity))] if min(polarity) < 0.2 else "No Negative Comments",
        "positive_count": len(positive_comments),
        "negative_count": len(negative_comments),
        "neutral_count": len(neutral_comments)
    }

    return sentiment_summary


def plot_sentiment_summary(sentiment_summary: Dict) -> str:
    labels = ['Positive', 'Negative', 'Neutral']
    counts = [sentiment_summary['positive_count'],
              sentiment_summary['negative_count'], sentiment_summary['neutral_count']]

    # Bar chart
    plt.bar(labels, counts, color=['blue', 'red', 'grey'])
    plt.xlabel('Sentiment')
    plt.ylabel('Comment Count')
    plt.title('Sentiment Analysis of Comments')

    # Save to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    bar_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.clf()

    # Pie chart
    plt.pie(counts, labels=labels, autopct='%1.1f%%')
    plt.title('Sentiment Distribution')

    # Save to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    pie_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.clf()

    return {"bar_chart": bar_chart, "pie_chart": pie_chart}


def load_processed_comments(file_path: str) -> List[str]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r', encoding='utf-8') as f:
        comments = f.readlines()

    # Strip out any leading/trailing whitespace characters
    comments = [comment.strip() for comment in comments if comment.strip()]

    return comments
