# Quick Reference Guide

## 🚀 Quick Start Commands

### Setup (First Time Only)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run setup wizard (interactive configuration)
python setup.py

# 3. Test the system
python test_system.py
```

### Running the System

```bash
# Generate and post once (for testing)
python main.py once

# Start daily scheduler (runs 24/7)
python main.py start

# Check system status
python main.py status
```

### Monitoring & Debugging

```bash
# View live logs
tail -f logs/automation.log

# View last 50 lines of logs
tail -50 logs/automation.log

# Search logs for errors
grep "ERROR" logs/automation.log

# Run system diagnostics
python test_system.py

# List generated content
ls -la generated_content/

# Check specific post metadata
cat generated_content/TIMESTAMP/metadata.json
```

## 📁 Project Files Overview

| File | Purpose |
|------|---------|
| `main.py` | Main orchestrator - runs everything |
| `content_generator.py` | AI content generation using OpenAI |
| `thumbnail_generator.py` | Creates custom PNG thumbnails |
| `video_creator.py` | Generates videos from scripts |
| `youtube_uploader.py` | YouTube API integration |
| `tiktok_uploader.py` | TikTok API integration |
| `setup.py` | Interactive setup wizard |
| `test_system.py` | System diagnostics and testing |
| `.env` | Configuration file (API keys, settings) |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |

## ⚙️ Configuration (.env)

Edit `.env` to customize:

```
# API Keys
OPENAI_API_KEY=sk-...
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...
YOUTUBE_REFRESH_TOKEN=...
TIKTOK_ACCESS_TOKEN=...
TIKTOK_REFRESH_TOKEN=...

# Settings
POSTING_TIME=09:00           # Daily posting time
VIDEO_DURATION=60            # Video duration (seconds)
CONTENT_TYPE=motivation      # Content type
THUMBNAIL_WIDTH=1280         # Thumbnail width
THUMBNAIL_HEIGHT=720         # Thumbnail height

# Logging
LOG_LEVEL=INFO               # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/automation.log # Log file location
```

## 🔑 Getting API Keys

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. Copy to `.env`

### YouTube
1. Go to https://console.cloud.google.com/
2. Create new project
3. Enable "YouTube Data API v3"
4. Create OAuth 2.0 credentials
5. Download JSON → rename to `credentials.json`
6. Add Client ID and Secret to `.env`
7. First run generates refresh token automatically

### TikTok
1. Go to https://developer.tiktok.com/
2. Create app
3. Request "Video Upload" access
4. Get Access Token and Refresh Token
5. Add to `.env`

## 🐛 Troubleshooting

### Problem: "OPENAI_API_KEY not found"
```bash
# Solution: Check .env file
cat .env | grep OPENAI_API_KEY

# If empty, add it:
echo "OPENAI_API_KEY=sk-YOUR_KEY_HERE" >> .env
```

### Problem: "FFmpeg not found"
```bash
# Windows
choco install ffmpeg

# Mac
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### Problem: "Can't import moviepy"
```bash
pip install --upgrade moviepy
```

### Problem: YouTube upload fails
```bash
# Delete token cache and re-authenticate
rm token.pickle

# Ensure credentials.json exists
ls credentials.json

# Run again
python main.py once
```

### Problem: TikTok token expired
```bash
# Get new tokens from https://developer.tiktok.com/
# Update .env with new tokens
nano .env

# Restart
python main.py start
```

### Problem: Video creation is slow
```bash
# Option 1: Use smaller video
# Edit .env: VIDEO_DURATION=30

# Option 2: Lower quality (faster rendering)
# Edit video_creator.py line 45: fps=15 (instead of 24)

# Option 3: Use faster cloud instance
```

### Problem: Posts aren't appearing
```bash
# 1. Check logs
tail -f logs/automation.log

# 2. Check metadata
cat generated_content/*/metadata.json

# 3. Verify API permissions on platforms
# YouTube: https://myaccount.google.com/permissions
# TikTok: https://www.tiktok.com/creator/studio

# 3. Run test
python test_system.py
```

## 📊 Monitoring Commands

```bash
# Check if system is running
ps aux | grep main.py

# Kill running process
pkill -f "python main.py"

# View disk usage (videos take space)
du -sh generated_content/

# Count generated videos
ls -1 generated_content/*/video.mp4 | wc -l

# Check API usage (OpenAI dashboard)
# https://platform.openai.com/account/usage

# Check TikTok analytics
# https://www.tiktok.com/creator/studio/analytics
```

## 🚀 Cloud Deployment Quick Commands

### AWS EC2
```bash
# Connect to instance
ssh -i key.pem ubuntu@YOUR_IP

# Install dependencies
sudo apt-get update
sudo apt-get install python3.9 python3-pip ffmpeg -y
git clone <your-repo>
cd my\ automation\ folder
pip3 install -r requirements.txt

# Setup
python3 setup.py

# Run in background
nohup python3 main.py start > automation.log 2>&1 &

# Check status
ps aux | grep main.py
tail -f automation.log
```

### Docker
```bash
# Build
docker build -t youtube-automation .

# Run
docker run -d --name automation youtube-automation

# Check logs
docker logs -f automation

# Stop
docker stop automation
```

### Screen Session (Simple)
```bash
# Start new session
screen -S automation

# Run system
python main.py start

# Detach (keep running)
# Press Ctrl+A, then D

# Reattach later
screen -r automation

# Kill session
screen -X -S automation quit
```

## 📈 Performance Tips

- Use smaller videos (30-60 seconds) for faster processing
- Lower FPS (15-20) instead of 24 for faster rendering
- Post during peak hours for better engagement
- Vary content to maintain audience interest
- Monitor analytics and adjust posting time based on views

## 🔒 Security Checklist

- [ ] Never commit `.env` file to git
- [ ] Use unique, strong API keys
- [ ] Rotate API keys regularly
- [ ] Don't share credentials publicly
- [ ] Use environment variables on cloud servers
- [ ] Monitor API access logs
- [ ] Set up IP whitelisting if available

## 📞 Getting Help

1. Check logs: `tail -f logs/automation.log`
2. Run diagnostics: `python test_system.py`
3. Review README.md for detailed documentation
4. Check platform API documentation:
   - YouTube: https://developers.google.com/youtube/docs
   - TikTok: https://developers.tiktok.com/doc/
   - OpenAI: https://platform.openai.com/docs

## 🎯 Common Customizations

### Change posting time
```bash
# Edit .env
POSTING_TIME=14:30  # 2:30 PM
```

### Change content topic
```bash
# Edit content_generator.py
# Find: prompt = """Generate a short, inspiring motivational post...
# Change to your topic
```

### Different thumbnail style
```bash
# Edit thumbnail_generator.py
# Modify colors: self.bg_colors = [(255, 67, 54), ...]
# Adjust fonts and positioning in create_thumbnail()
```

### Change video format
```bash
# Edit video_creator.py
# Change size from (1080, 1920) for different aspect ratio
# 1280x720 for YouTube
# 1080x1920 for shorts/TikTok
# 1200x675 for social media
```

---

**Last Updated:** 2024
**Version:** 1.0
