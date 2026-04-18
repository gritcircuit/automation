# GitHub Actions Setup Guide - Complete

## Step-by-Step Setup for FREE 24/7 Automation

Your automation system will run automatically on GitHub's servers every day at 9:00 AM!

---

## STEP 1: Create GitHub Account (FREE)

1. Go to: https://github.com/signup
2. Sign up with your email
3. Verify your email address
4. Done! You now have a free GitHub account

**Time: 2 minutes**

---

## STEP 2: Create a New Repository

1. Go to: https://github.com/new
2. Repository name: `youtube-automation`
3. Description: `Automated YouTube & TikTok posting system`
4. **IMPORTANT:** Select **"Public"** (required for free Actions)
5. *Do NOT* check "Initialize with README"
6. Click **"Create repository"**

**Time: 1 minute**

---

## STEP 3: Upload Your Code Files

You'll upload your Python files to GitHub. Here's the easiest way:

### Option A: Upload via GitHub Web (EASIEST)

1. You're now in your empty repository
2. Click **"Add file"** → **"Upload files"**
3. Drag and drop these files into the upload area:

**ESSENTIAL FILES (MUST upload):**
- `main.py`
- `content_generator.py`
- `thumbnail_generator.py`
- `video_creator.py`
- `youtube_uploader.py`
- `tiktok_uploader.py`
- `requirements.txt`
- `.gitignore`
- `credentials.json`

**Optional (for reference):**
- `README.md`
- `QUICK_REFERENCE.md`
- `monitor.py`

4. Click **"Commit changes"**

**Time: 3 minutes**

---

## STEP 4: Add GitHub Secrets (IMPORTANT!)

Your API keys need to be stored securely in GitHub Secrets (not in the code).

1. In your repository, click **"Settings"** tab
2. Click **"Secrets and variables"** → **"Actions"**
3. Click **"New repository secret"** for each:

**Add these secrets (copy from your .env file):**

| Secret Name | Value |
|-------------|-------|
| `OPENAI_API_KEY` | `sk-proj-...` (your OpenAI key) |
| `YOUTUBE_CLIENT_ID` | `3914537525-...` |
| `YOUTUBE_CLIENT_SECRET` | `GOCSPX-...` |
| `YOUTUBE_REFRESH_TOKEN` | Your refresh token |
| `TIKTOK_ACCESS_TOKEN` | (leave empty for now) |
| `TIKTOK_REFRESH_TOKEN` | (leave empty for now) |

**How to add each secret:**
1. Click **"New repository secret"**
2. Name: (from table above, e.g., `OPENAI_API_KEY`)
3. Secret: (paste your actual value)
4. Click **"Add secret"**
5. Repeat for all secrets

**Time: 3 minutes**

---

## STEP 5: Create GitHub Actions Workflow

The workflow file tells GitHub to run your code automatically.

1. In your repository, click the **"Actions"** tab
2. Look for suggested workflows - ignore them
3. Click **"Set up a workflow yourself"** (or new file)
4. Delete any existing content
5. Paste this workflow code:

```yaml
name: Daily YouTube & TikTok Automation

on:
  schedule:
    - cron: '0 9 * * *'
  workflow_dispatch:

jobs:
  automation:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y ffmpeg
      
      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Create .env file
        run: |
          cat > .env << EOF
          OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}
          YOUTUBE_CLIENT_ID=${{ secrets.YOUTUBE_CLIENT_ID }}
          YOUTUBE_CLIENT_SECRET=${{ secrets.YOUTUBE_CLIENT_SECRET }}
          YOUTUBE_REFRESH_TOKEN=${{ secrets.YOUTUBE_REFRESH_TOKEN }}
          TIKTOK_ACCESS_TOKEN=${{ secrets.TIKTOK_ACCESS_TOKEN }}
          TIKTOK_REFRESH_TOKEN=${{ secrets.TIKTOK_REFRESH_TOKEN }}
          POSTING_TIME=09:00
          VIDEO_DURATION=60
          CONTENT_TYPE=motivation
          THUMBNAIL_WIDTH=1280
          THUMBNAIL_HEIGHT=720
          LOG_LEVEL=INFO
          EOF
      
      - name: Run automation
        run: python main.py once
      
      - name: Upload generated content
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: generated-content
          path: generated_content/
          retention-days: 7
      
      - name: Upload logs
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: automation-logs
          path: logs/
          retention-days: 7
```

6. Name the file: `.github/workflows/automation.yml`
7. Click **"Commit changes"**

**Time: 2 minutes**

---

## STEP 6: Test Your Workflow

### Manual Test (Do this first!)

1. Go to **"Actions"** tab
2. Click **"Daily YouTube & TikTok Automation"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Watch it run! (takes 2-5 minutes)
5. Check if it succeeded or failed

### View Results

After it completes:
1. Click the completed run
2. Check each step for output
3. Download artifacts (generated content, logs)
4. Verify everything worked!

**Time: 5 minutes (includes waiting)**

---

## STEP 7: Verify Automatic Scheduling

The workflow is now scheduled to run:

✅ **Every day at 9:00 AM UTC**
✅ **Automatically (no action needed)**
✅ **Forever (while your repo exists)**

**To change the time:**

Edit `.github/workflows/automation.yml` and change:
```yaml
cron: '0 9 * * *'
```

Use: https://crontab.guru to find the right time

Common examples:
- `0 9 * * *` = 9:00 AM UTC
- `0 14 * * *` = 2:00 PM UTC
- `0 18 * * *` = 6:00 PM UTC

---

## STEP 8: Monitor Your Runs

### View Workflow Runs

1. Go to **"Actions"** tab
2. Click **"Daily YouTube & TikTok Automation"**
3. See all past runs
4. Click any run to see details and logs

### Download Results

After each run:
1. Click the completed run
2. Scroll down to "Artifacts"
3. Download:
   - `generated-content` - Your created videos/thumbnails
   - `automation-logs` - Detailed logs

---

## TROUBLESHOOTING

### Workflow failed?

1. Click the failed run
2. Expand each step to see the error
3. Common issues:

**"ModuleNotFoundError"**
- Fix: Make sure all dependencies are in `requirements.txt`

**"Authentication failed"**
- Fix: Check your GitHub Secrets are correct
- Go to Settings → Secrets → Verify each one

**"Timeout"**
- Fix: Increase timeout in workflow (change 3600 to 5400)

**"No module named 'moviepy.editor'"**
- This is expected - system uses fallback
- Your posts will still be generated!

### Check Logs

After each run, download the `automation-logs` artifact to see what happened.

---

## WHAT HAPPENS AUTOMATICALLY

✅ **Every day at 9:00 AM UTC:**
1. GitHub starts your automation
2. Installs dependencies
3. Generates motivational content using OpenAI
4. Creates thumbnail image
5. Creates video file
6. Posts to YouTube
7. Logs everything
8. Cleans up

✅ **Results are saved:**
- Generated videos & thumbnails
- Execution logs
- Available for 7 days

---

## MONITORING FROM YOUR PC

You can check your automation anytime:

1. Go to: https://github.com/YOUR_USERNAME/youtube-automation
2. Click **"Actions"** tab
3. See all your posts
4. Download artifacts
5. Check logs

---

## QUICK REFERENCE

| Action | How |
|--------|-----|
| **View runs** | Go to Actions tab |
| **Test manually** | Click "Run workflow" |
| **Change time** | Edit `.github/workflows/automation.yml` |
| **Add TikTok later** | Update Secrets in Settings |
| **View logs** | Download artifacts after run |
| **Stop automation** | Disable workflow in Actions tab |

---

## COST

✅ **FREE** - GitHub Actions is free for public repositories
✅ **UNLIMITED** - Runs daily forever at no cost
✅ **ALWAYS-ON** - Your system never sleeps

---

## NEXT STEPS

1. Create GitHub account (if you don't have one)
2. Create repository
3. Upload your files
4. Add secrets
5. Create workflow file
6. Test manually
7. Done! Automation runs automatically

---

**Ready to set up?** Follow these steps one by one in order!

Questions? Just ask!
