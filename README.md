# YouTube & TikTok Auto-Posting System - Setup Guide

## 📋 System Overview

This is a complete Python-based automation system that:
- ✅ Generates motivational content daily using AI (OpenAI)
- ✅ Creates custom thumbnails with dynamic templates
- ✅ Generates voiceover from scripts
- ✅ Creates videos with text overlays
- ✅ Posts automatically to YouTube and TikTok
- ✅ Schedules daily posts at specified time
- ✅ Runs on cloud servers (AWS, GCP, Azure)

## 🔧 Prerequisites

- Python 3.9+
- FFmpeg (for video processing)
- Valid API keys for: OpenAI, YouTube, TikTok

## 📦 Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg

**Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

### 3. Setup Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your actual keys:
```
OPENAI_API_KEY=sk-...
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...
TIKTOK_ACCESS_TOKEN=...
TIKTOK_REFRESH_TOKEN=...
```

## 🔐 API Setup Instructions

### YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file
6. Rename to `credentials.json` and place in project root
7. First run will prompt you to authorize

### TikTok API Setup

1. Go to [TikTok Developer Portal](https://developer.tiktok.com/)
2. Create a new application
3. Request access to Video Upload API
4. Get your:
   - Client ID
   - Client Secret
   - Access Token
   - Refresh Token

### OpenAI API Setup

1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add to `.env` file as `OPENAI_API_KEY`

## 🚀 Usage

### Run Once (Testing)

Generate and post content immediately:

```bash
python main.py once
```

### Start Daily Scheduler

Run the automation 24/7 with daily posts:

```bash
python main.py start
```

### Check System Status

```bash
python main.py status
```

## 📁 Project Structure

```
my automation folder/
├── main.py                    # Main orchestrator
├── content_generator.py       # AI content generation
├── thumbnail_generator.py     # Thumbnail creation
├── video_creator.py          # Video creation
├── youtube_uploader.py       # YouTube API integration
├── tiktok_uploader.py        # TikTok API integration
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .env                      # Your actual credentials (DO NOT COMMIT)
├── logs/                     # Automation logs
├── generated_content/        # Created content (organized by timestamp)
└── README.md                 # This file
```

## ☁️ Deploying to Cloud Server

### AWS EC2

1. **Launch EC2 Instance:**
   - OS: Ubuntu 22.04 LTS
   - Type: t3.medium+ (for video processing)
   - Storage: 50GB+ (videos take space)

2. **Connect and Setup:**
   ```bash
   # Update system
   sudo apt-get update && sudo apt-get upgrade -y
   
   # Install dependencies
   sudo apt-get install python3.9 python3-pip ffmpeg git -y
   
   # Clone/transfer your project
   git clone <your-repo-url>
   cd my\ automation\ folder
   
   # Install Python packages
   pip3 install -r requirements.txt
   
   # Setup environment
   cp .env.example .env
   nano .env  # Add your API keys
   ```

3. **Run in Background:**
   ```bash
   # Using screen (simple)
   screen -S automation
   python3 main.py start
   # Press Ctrl+A then D to detach
   
   # Or using nohup
   nohup python3 main.py start > automation.log 2>&1 &
   ```

4. **Keep Running with PM2 (Recommended):**
   ```bash
   npm install -g pm2
   pm2 start main.py --name automation --interpreter python3
   pm2 save
   pm2 startup
   ```

### Google Cloud Run (Serverless)

1. **Create `app.yaml`:**
   ```yaml
   runtime: python39
   env: standard
   entrypoint: python main.py start
   ```

2. **Deploy:**
   ```bash
   gcloud app deploy
   ```

### Docker (Cloud-agnostic)

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV OPENAI_API_KEY=your_key
ENV YOUTUBE_CLIENT_ID=your_id
# ... other env vars

CMD ["python", "main.py", "start"]
```

**Build & Run:**
```bash
docker build -t youtube-tiktok-automation .
docker run -d --name automation youtube-tiktok-automation
```

## 📊 Monitoring & Logs

Logs are saved in `logs/automation.log`:

```bash
# View real-time logs
tail -f logs/automation.log

# View last 50 lines
tail -50 logs/automation.log

# Search for errors
grep "ERROR" logs/automation.log
```

## 🎯 Customization Guide

### Change Posting Time

Edit `.env`:
```
POSTING_TIME=14:30  # Posts at 2:30 PM daily
```

### Modify Content Topics

Edit `content_generator.py` - modify the prompt in `generate_motivation_post()`:

```python
prompt = """Generate a [YOUR_TOPIC] post..."""
```

### Customize Thumbnail Design

Edit `thumbnail_generator.py` - modify colors and text positioning

### Change Video Duration

Edit `.env`:
```
VIDEO_DURATION=120  # 2 minutes instead of 60 seconds
```

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Ensure `.env` file exists with valid API key
- Verify key is active on OpenAI dashboard

### "FFmpeg not found"
- Install FFmpeg (see Prerequisites)
- Add to system PATH

### YouTube authentication fails
- Delete `token.pickle`
- Ensure `credentials.json` is in project root
- Run `python main.py once` to re-authenticate

### TikTok token expired
- Refresh token manually from TikTok Developer Portal
- Update `.env` with new token
- Uploader will auto-refresh on next run

### Video creation slow on cloud server
- Use higher tier server (more CPU cores)
- Reduce video duration
- Lower FPS (edit video_creator.py, change fps=24 to fps=15)

## 📈 Content Statistics

Check generated content in `generated_content/`:

```bash
# List all generated content
ls -la generated_content/

# View metadata of latest post
cat generated_content/LATEST_TIMESTAMP/metadata.json
```

## ✅ Checklist Before Going Live

- [ ] YouTube API credentials set up
- [ ] TikTok API credentials set up
- [ ] OpenAI API key added
- [ ] `.env` file configured
- [ ] FFmpeg installed
- [ ] Test run successful: `python main.py once`
- [ ] Verify posts appear on both platforms
- [ ] Set desired posting time in `.env`
- [ ] Deploy to cloud or local server
- [ ] Monitor logs for errors

## 🚨 Important Notes

1. **API Costs:**
   - OpenAI: ~$0.01-0.05 per content generation
   - YouTube: Free (within quota)
   - TikTok: Free (within rate limits)

2. **Rate Limits:**
   - OpenAI: 3,500 RPM (Pro), adjust if needed
   - TikTok: ~10 videos per day recommended
   - YouTube: 1 video per day recommended

3. **Content Quality:**
   - OpenAI generates unique content daily
   - Customize prompts for your niche
   - Monitor engagement to optimize

4. **Legal Compliance:**
   - Ensure content follows platform guidelines
   - Disclose if AI-generated (check platform requirements)
   - Respect copyright for any background music

## 📞 Support

For issues:
1. Check logs: `tail -f logs/automation.log`
2. Verify API keys and permissions
3. Test components individually
4. Check platform API documentation

## 📜 License

This project is provided as-is for personal use.

---

**Happy automating! 🚀**
