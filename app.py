import os
import json
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
from dotenv import load_dotenv
from fastapi import FastAPI


# Initialize Gemini client
load_dotenv()
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

app=FastAPI()

def get_youtube_transcript(video_id: str) -> str:
    """Fetch the transcript of a YouTube video using its video ID."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = "\n".join([entry['text'] for entry in transcript_list])
        return transcript_text
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"


def get_summary_from_transcript(transcript: str) -> str|None:
    """Send transcript to Gemini model and get JSON-formatted summary."""
    model = "gemini-2.0-flash"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text="""Based on the above YouTube transcript give me a brief summary of the topic in JSON format given below:
{
   "topic_name":"name of topic",
   "topic_summary":"summary of topic"
}"""
                )
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=transcript)
            ],
        ),
    ]

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(response_mime_type="text/plain"),
    )

    return response.text

def extract_youtube_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    elif "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtube.com/embed/" in url:
        return url.split("embed/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

def clean_json_output(raw_output: str) -> dict|None:
    """
    Takes a raw JSON string with escaped characters and formatting,
    and returns a clean Python dictionary.
    
    Args:
        raw_output (str): The raw string output from FastAPI (e.g., "```json\n{\n...}\n```\n")
    
    Returns:
        dict: The parsed and cleaned JSON as a Python dictionary
    """
    # Remove the ```json and ``` markers, if present
    cleaned = raw_output.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    
    # Parse the JSON string into a Python dictionary
    try:
        parsed_json = json.loads(cleaned)
        return parsed_json
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

@app.get("/summarize")
def get_summary(url:str):
    video_id = extract_youtube_id(url)
    transcript = get_youtube_transcript(video_id)
    if transcript.startswith("Error"):
        print(transcript)
        return (f"Invalid URL or Transcript not available")

    summary = get_summary_from_transcript(transcript)
    formatted_summary=clean_json_output(summary)
    print(formatted_summary)
    return formatted_summary