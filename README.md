# 🎥 YouTube Video Summarizer (FastAPI + Gemini)

This is a FastAPI-based application that summarizes the transcript of a YouTube video using Google's Gemini model (`gemini-2.0-flash`). It extracts the transcript of a given YouTube video, sends it to Gemini for summarization, and returns a structured JSON output with the topic and its summary.

## 🚀 Features
- Extracts transcript from any public YouTube video with available subtitles.
- Sends the transcript to Gemini AI via the Google Generative AI SDK.
- Returns a clean, JSON-formatted summary.
- Built with FastAPI for fast and asynchronous performance.

## 📦 Tech Stack
- **Python 3.10+**
- **FastAPI**
- **YouTube Transcript API**
- **Google Generative AI SDK (Gemini)**
- **dotenv**
- **Uvicorn (for local server)**

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Krishna3575/YT_SummarAIze.git
cd YT_SummarAIze
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables 
Create a .env file in the project root directory and add your Gemini API key as follows:
GEMINI_API_KEY=your_gemini_api_key_here (from google ai studios)

### 5. Run the FastAPI Server Locally 
```bash
uvicorn app:app --reload
```

## USE 
Send a GET request to the /summarize endpoint with a YouTube video URL as a query parameter.
```bash
http://127.0.0.1:8000/summarize?url=https://www.youtube.com/watch?v=exampleID
```
The API respods with a JSON containing the topic name and summary extracted from the video transcript.

## ⚠️ Notes
● This tool works only with YouTube videos that have publicly available subtitles.
● The Gemini API key is required and should be kept private.
● This project is intended for educational and demonstration purposes.

Feel free to open issues or submit pull requests!
