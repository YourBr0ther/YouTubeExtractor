# Transcriptor

A sleek YouTube transcript extractor with AI-powered summarization.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

- **Extract Transcripts** - Fetch transcripts from any YouTube video with captions
- **AI Summarization** - Get intelligent summaries powered by Groq's LLaMA 3.3 70B
- **Download & Copy** - One-click download or copy for transcripts and summaries
- **Modern UI** - Clean, responsive dark theme interface
- **No YouTube API Key Required** - Uses `youtube-transcript-api` module

## Quick Start

### Prerequisites

- Python 3.9+
- A Groq API key ([Get one free](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YourBr0ther/YouTubeExtractor.git
   cd YouTubeExtractor
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

1. Paste a YouTube URL into the input field
2. Click "Extract" to fetch the transcript
3. View the full transcript and AI-generated summary side by side
4. Download or copy the content using the buttons provided

## Tech Stack

- **Backend**: Flask (Python)
- **Transcript Fetching**: youtube-transcript-api
- **AI Summarization**: Groq (LLaMA 3.3 70B)
- **Frontend**: HTML, Tailwind CSS, Vanilla JS
- **Fonts**: Instrument Serif, Sora

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key for AI summarization |

## Limitations

- Only works with videos that have captions/subtitles enabled
- Auto-generated captions may contain errors
- Very long videos may have truncated summaries due to token limits

## License

MIT License - feel free to use and modify as needed.

## Author

Built with love by **YourBr0ther**

---

*Powered by youtube-transcript-api and Groq*
