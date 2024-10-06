# SentimentSense---YouTube-Sentiment-Analyzer
  
SentimentSense is a YouTube sentiment analysis tool that fetches comments from a given video URL and classifies them as positive, negative, or neutral. It provides a clear visual representation of audience reactions using bar and pie charts. Additionally, users can analyze the toxicity of specific comments, offering insights into both general sentiment and individual feedback.

#### Key features include:

- YouTube Comment Sentiment Analysis: Fetch comments from any YouTube video and classify them into positive, negative, or neutral categories.

- Sentiment Visualization: Display the sentiment distribution using bar charts and pie charts for a clear overview of audience reactions.

- Toxicity Analysis: Enter a specific comment to analyze its toxicity parameters such as Toxic, Severe Toxic, Obscene, Threat, Insult, and Identity Hate.

- Versatile Insights: Understand overall audience sentiment while also providing detailed analysis for individual user comments.
  
This project demonstrates the potential of AI-driven emotion detection, allowing for more intuitive interaction between humans and machines.

## Technologies Used
- Python
- YouTube Data API
- FastAPI
- TensorFlow

## Demo

https://github.com/user-attachments/assets/8e9567d1-3d2e-4354-8f39-8ceaca83424b

## How to Run This Project

1. Clone the repository:
```
git clone https://github.com/Chauhan-Aman/SentimentSense---YouTube-Sentiment-Analyzer.git
cd SentimentSense
```
2. Set up a virtual environment:
```
python -m venv venv
source venv/bin/activate.ps1   # On Windows use `venv\Scripts\activate.ps1`
```
3. Install required dependencies:
```
Install required dependencies:
```
4. Run the FastAPI server:
```
uvicorn main:app --reload
```
5. Access the API: Open your browser and go to http://127.0.0.1:8000 to see the Human Emotion Detection API running.
6. Frontend Interaction:
   - To interact with the API from the frontend, ensure CORS settings allow access from your frontend domain.
   - You can upload images through the frontend to classify emotions.

This setup will allow you to run the Human Emotion Detection system locally.
