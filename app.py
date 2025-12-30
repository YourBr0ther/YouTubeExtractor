"""
Transcriptor - YouTube Transcript Extractor with AI Summarization
Built by YourBr0ther
"""

import os
import re
from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
from groq import Groq
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Groq client
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_video_id(url: str) -> str | None:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/shorts\/([^&\n?#]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_video_info(video_id: str) -> dict | None:
    """Fetch video metadata using oembed API."""
    try:
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(oembed_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "title": data.get("title", "Unknown Title"),
                "channel": data.get("author_name", "Unknown Channel"),
                "thumbnail": f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
            }
    except Exception:
        pass
    return {
        "title": "Video",
        "channel": "Unknown",
        "thumbnail": f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
    }


def get_transcript(video_id: str) -> str:
    """Fetch transcript for a YouTube video."""
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    # Combine all transcript segments into a single string
    full_transcript = " ".join([entry['text'] for entry in transcript_list])
    return full_transcript


def summarize_transcript(transcript: str, title: str = "") -> str:
    """Summarize the transcript using Groq's LLM."""
    # Truncate transcript if too long (Groq has token limits)
    max_chars = 30000
    if len(transcript) > max_chars:
        transcript = transcript[:max_chars] + "..."

    prompt = f"""Please provide a comprehensive yet concise summary of the following YouTube video transcript.

Video Title: {title}

Structure your summary as follows:
📌 **Key Points** - The main takeaways (3-5 bullet points)
📝 **Summary** - A brief paragraph summarizing the content
🎯 **Main Topics** - List the key topics discussed

Transcript:
{transcript}

Provide a clear, well-organized summary that captures the essence of the video."""

    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes YouTube video transcripts. Be concise but comprehensive. Use clear formatting."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama-3.1-70b-versatile",
        temperature=0.3,
        max_tokens=1500
    )

    return chat_completion.choices[0].message.content


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/transcript', methods=['POST'])
def api_transcript():
    """API endpoint to fetch transcript."""
    data = request.get_json()
    url = data.get('url', '')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        transcript = get_transcript(video_id)
        video_info = get_video_info(video_id)

        return jsonify({
            "transcript": transcript,
            "video_id": video_id,
            "video_info": video_info
        })

    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 400
    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video. It may not have captions."}), 400
    except VideoUnavailable:
        return jsonify({"error": "Video is unavailable or does not exist"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to fetch transcript: {str(e)}"}), 500


@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    """API endpoint to summarize transcript."""
    data = request.get_json()
    transcript = data.get('transcript', '')
    title = data.get('title', '')

    if not transcript:
        return jsonify({"error": "Transcript is required"}), 400

    if not os.getenv("GROQ_API_KEY"):
        return jsonify({"error": "Groq API key not configured"}), 500

    try:
        summary = summarize_transcript(transcript, title)
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": f"Failed to generate summary: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
