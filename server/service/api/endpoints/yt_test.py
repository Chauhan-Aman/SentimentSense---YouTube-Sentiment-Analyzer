from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.core.logic.youtube_comments import fetch_comments, process_comments, fetch_videodetails
from service.core.logic.sentiments import analyze_sentiment, plot_sentiment_summary

yt_router = APIRouter()


class VideoRequest(BaseModel):
    url: str


@yt_router.post("/analyze_comments/")
async def fetch_and_process_comments(request: VideoRequest):
    try:
        video_details = fetch_videodetails(request.url)
        comments = fetch_comments(request.url)
        relevant_comments = process_comments(comments)

        sentiment_summary = analyze_sentiment(relevant_comments)
        charts = plot_sentiment_summary(sentiment_summary)
        sentiment_summary.update(charts)
        return {
            "videoDetails": video_details,
            "sentimentData": sentiment_summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
