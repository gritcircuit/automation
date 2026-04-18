"""
ORACLE CLOUD SETUP GUIDE
Deploy your automation to Oracle Cloud's Always-Free tier

Oracle Cloud offers:
✓ Always FREE (no credit card, no expiration)
✓ 2 x Always Free Virtual Machines (1 OCPU, 1GB RAM each)
✓ 20GB Block Storage
✓ Autonomous Database
✓ Perfect for 24/7 automation
"""

ORACLE_SETUP = """
╔══════════════════════════════════════════════════════════════════╗
║           ORACLE CLOUD ALWAYS-FREE TIER SETUP                    ║
╚══════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: CREATE ORACLE CLOUD ACCOUNT (FREE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to: https://www.oracle.com/cloud/free/
2. Click "Start for free"
3. Enter your email and country
4. You'll get $300 FREE credits (separate from always-free)
5. Create account - NO credit card required for free tier!
6. Login to Oracle Cloud Console

Time: 5 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: CREATE COMPUTE INSTANCE (VM)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. In Oracle Cloud Console:
   - Click "Compute" → "Instances"
   - Click "Create Instance"

2. Configure Instance:
   - Name: youtube-automation
   - Image: Ubuntu 22.04 (always free eligible)
   - Shape: Ampere (Always Free eligible - ARM processor)
   - vCPU: 4
   - RAM: 24 GB
   
3. Networking:
   - Use default VCN (Virtual Cloud Network)
   - Auto-assign public IP: YES

4. SSH Key:
   - Save SSH key on your computer (IMPORTANT!)
   - Click "Create"

Time: 3 minutes
Result: Free Ubuntu VM running 24/7

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: CONNECT TO YOUR VM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

From PowerShell on your PC:

# Copy SSH key file
move "C:\path\to\ssh-key.key" ~/.ssh/

# Connect to VM
ssh -i ~/.ssh/ssh-key.key ubuntu@YOUR_PUBLIC_IP

(Get PUBLIC_IP from Oracle Cloud Console)

Time: 2 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4: INSTALL DEPENDENCIES ON VM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Once connected via SSH:

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y python3.11 python3-pip git ffmpeg

# Install PM2 (keeps your app running forever)
sudo npm install -g pm2

# Clone your automation code OR upload files
git clone <your-github-repo>
cd my-automation-folder

# Install Python dependencies
pip install -r requirements.txt

Time: 5-10 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5: SETUP YOUR .ENV FILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

On the VM:

# Create .env file
nano .env

# Paste your credentials:
OPENAI_API_KEY=sk-proj-...
YOUTUBE_CLIENT_ID=3914537525-...
YOUTUBE_CLIENT_SECRET=GOCSPX-...
YOUTUBE_REFRESH_TOKEN=will-auto-generate
TIKTOK_ACCESS_TOKEN=
TIKTOK_REFRESH_TOKEN=
POSTING_TIME=09:00

# Save: Ctrl+X, then Y, then Enter

Time: 2 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 6: START YOUR AUTOMATION WITH PM2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PM2 is a process manager that keeps your app running 24/7:

# Start the automation
pm2 start main.py --name youtube-automation --interpreter python3

# Make it restart on reboot
pm2 startup
pm2 save

# View logs
pm2 logs youtube-automation

Time: 1 minute
Result: System running 24/7 forever!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 7: MONITOR ON YOUR PC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

From your local PC:

# Check if running
ssh -i ~/.ssh/ssh-key.key ubuntu@YOUR_PUBLIC_IP pm2 status

# View logs
ssh -i ~/.ssh/ssh-key.key ubuntu@YOUR_PUBLIC_IP pm2 logs youtube-automation

# Stop (if needed)
ssh -i ~/.ssh/ssh-key.key ubuntu@YOUR_PUBLIC_IP pm2 stop youtube-automation

# Restart (if needed)
ssh -i ~/.ssh/ssh-key.key ubuntu@YOUR_PUBLIC_IP pm2 restart youtube-automation

Time: Anytime, from anywhere

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TL;DR - QUICK VERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Sign up: https://www.oracle.com/cloud/free/ (5 min)
2. Create Ubuntu VM (3 min)
3. SSH into VM (2 min)
4. Install: python3, pip, git, ffmpeg, pm2 (5 min)
5. Upload your code
6. Create .env file
7. Run: pm2 start main.py --interpreter python3
8. Done! Runs forever, FREE forever

TOTAL TIME: ~30 minutes
COST: $0 forever (always-free tier)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADVANTAGES OF ORACLE CLOUD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ ALWAYS FREE (no time limit, no credit card required)
✓ 4 vCPU + 24GB RAM (very generous!)
✓ Runs forever 24/7
✓ Full Linux server (not serverless)
✓ Easy to manage
✓ Can do ANYTHING (not just scheduled tasks)
✓ Total control

DISADVANTAGES:
✗ Need to manage VM yourself
✗ Need SSH knowledge
✗ Need to keep free tier eligible (easy)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VS OTHER OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Google Cloud:
- Pros: Serverless, simple
- Cons: Free tier expires, limited

Heroku:
- Pros: Very easy
- Cons: $7/month

Oracle Cloud:
- Pros: Always FREE, full server, 4 vCPU!
- Cons: Slightly more setup

>>> BEST VALUE: ORACLE CLOUD <<<

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
READY TO SET UP ORACLE CLOUD?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Say: "YES, ORACLE CLOUD" and I'll guide you step-by-step

Or ask questions before starting!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

print(ORACLE_SETUP)
