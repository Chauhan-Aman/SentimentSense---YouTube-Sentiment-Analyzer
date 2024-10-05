from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.core.logic.youtube_comments import classify_comments
from typing import List

comment_router = APIRouter()


class CommentRequest(BaseModel):
    comments: List[str]

# POST endpoint to analyze sentiments on input comments
@comment_router.post("/comment_analyze/")
async def analyze_sentiment_endpoint(request: CommentRequest):
    try:
        comment = request.comments

        predictionINT, predictionBool = classify_comments(comment)

        resultBool = predictionBool.to_dict(orient='records')
        resultINT = predictionINT.to_dict(orient='records')

        result = {
            "resultINT": resultINT,
            "resultBool": resultBool
        }

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
