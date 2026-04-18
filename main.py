"""
Main Automation Scheduler
Orchestrates daily content generation and posting to YouTube and TikTok
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
import json

# Import custom modules
from content_generator import ContentGenerator
from thumbnail_generator import ThumbnailGenerator
try:
    from video_creator import VideoCreator
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️  MoviePy not available - video creation disabled")

try:
    from youtube_uploader import YouTubeUploader
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False
    print("⚠️  YouTube API not available - YouTube upload disabled")

try:
    from tiktok_uploader import TikTokUploader
    TIKTOK_AVAILABLE = True
except ImportError:
    TIKTOK_AVAILABLE = False
    print("⚠️  TikTok API not available - TikTok upload disabled")


class AutomationSystem:
    """Main automation system - orchestrates all components"""
    
    def __init__(self):
        """Initialize automation system"""
        load_dotenv()
        
        # Setup logging
        self._setup_logging()
        
        # Initialize components
        self.content_generator = ContentGenerator(
            api_key=os.getenv('OPENAI_API_KEY')
        )
        # Initialize thumbnail generator with platform preset or custom size
        platform = os.getenv('THUMBNAIL_PLATFORM', 'youtube')
        if platform in ThumbnailGenerator.PRESETS and ThumbnailGenerator.PRESETS[platform]:
            # Use platform preset
            self.thumbnail_generator = ThumbnailGenerator(platform=platform)
        else:
            # Use custom dimensions
            self.thumbnail_generator = ThumbnailGenerator(
                width=int(os.getenv('THUMBNAIL_WIDTH', '1280')),
                height=int(os.getenv('THUMBNAIL_HEIGHT', '720')),
                platform='custom'
            )
        if MOVIEPY_AVAILABLE:
            self.video_creator = VideoCreator()
        else:
            self.video_creator = None
        
        # Initialize uploaders
        self.youtube_uploader = None
        self.tiktok_uploader = None
        self._init_uploaders()
        
        # Setup scheduler
        self.scheduler = BackgroundScheduler()
        self.posting_time = os.getenv('POSTING_TIME', '09:00')
        
        self.logger.info("✓ Automation system initialized")
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, "automation.log")
        
        logging.basicConfig(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def _init_uploaders(self):
        """Initialize YouTube and TikTok uploaders"""
        if YOUTUBE_AVAILABLE:
            try:
                self.youtube_uploader = YouTubeUploader()
                self.logger.info("✓ YouTube uploader initialized")
            except Exception as e:
                self.logger.error(f"❌ YouTube initialization failed: {e}")
        else:
            self.logger.warning("⚠️  YouTube API not available")
        
        if TIKTOK_AVAILABLE:
            try:
                tiktok_token = os.getenv('TIKTOK_ACCESS_TOKEN')
                tiktok_refresh = os.getenv('TIKTOK_REFRESH_TOKEN')
                
                if tiktok_token and tiktok_refresh:
                    self.tiktok_uploader = TikTokUploader(
                        access_token=tiktok_token,
                        refresh_token=tiktok_refresh
                    )
                    self.logger.info("✓ TikTok uploader initialized")
            except Exception as e:
                self.logger.error(f"❌ TikTok initialization failed: {e}")
        else:
            self.logger.warning("⚠️  TikTok API not available")
    
    def generate_and_post(self):
        """Main function: Generate content and post to all platforms"""
        
        try:
            self.logger.info("=" * 60)
            self.logger.info("🚀 Starting daily content generation and posting")
            self.logger.info("=" * 60)
            
            # Step 1: Generate content
            self.logger.info("📝 Generating motivational content...")
            content = self.content_generator.generate_motivation_post()
            
            # Create content directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            content_dir = f"generated_content/{timestamp}"
            os.makedirs(content_dir, exist_ok=True)
            
            # Save content metadata
            content_metadata = {
                'timestamp': timestamp,
                'title': content.title,
                'script': content.script,
                'hashtags': content.hashtags,
                'thumbnail_text': content.thumbnail_text,
                'duration': content.duration
            }
            
            with open(os.path.join(content_dir, 'metadata.json'), 'w') as f:
                json.dump(content_metadata, f, indent=2)
            
            self.logger.info(f"📝 Content generated: {content.title}")
            
            # Step 2: Generate thumbnail
            self.logger.info("🎨 Generating thumbnail...")
            thumbnail_path = os.path.join(content_dir, 'thumbnail.jpg')
            self.thumbnail_generator.create_thumbnail(
                title=content.title,
                thumbnail_text=content.thumbnail_text,
                output_path=thumbnail_path
            )
            
            # Step 3: Create video
            self.logger.info("🎬 Creating video...")
            video_path = os.path.join(content_dir, 'video.mp4')
            
            if self.video_creator:
                self.video_creator.create_simple_video(
                    script_text=content.script,
                    title=content.title,
                    duration=content.duration,
                    output_path=video_path
                )
            else:
                # Create placeholder video if MoviePy not available
                self.logger.warning("⚠️  Creating placeholder video (MoviePy not available)")
                import subprocess
                try:
                    cmd = [
                        'ffmpeg', '-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:d=5',
                        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono:d=5',
                        '-c:v', 'libx264', '-c:a', 'aac', '-y', video_path
                    ]
                    subprocess.run(cmd, capture_output=True, timeout=30)
                except Exception as e:
                    self.logger.warning(f"Placeholder video creation failed: {e}")
            
            if not os.path.exists(video_path):
                self.logger.warning("⚠️  Video file not created - continuing with upload anyway")
            
            # Step 4: Generate voiceover
            self.logger.info("🎙️ Generating voiceover...")
            audio_path = os.path.join(content_dir, 'voiceover.mp3')
            self.content_generator.generate_video_script_voiceover(
                script=content.script,
                output_path=audio_path
            )
            
            # Step 5: Post to YouTube
            if self.youtube_uploader:
                self.logger.info("📤 Uploading to YouTube...")
                description = f"{content.script}\n\nGenerated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                youtube_id = self.youtube_uploader.upload_video(
                    video_path=video_path,
                    thumbnail_path=thumbnail_path,
                    title=content.title,
                    description=description,
                    tags=content.hashtags[:20],
                    privacy_status='public'
                )
                
                if youtube_id:
                    content_metadata['youtube_id'] = youtube_id
                    self.logger.info(f"✓ Posted to YouTube: {youtube_id}")
                    
                    # Display YouTube link
                    yt_link = f"https://www.youtube.com/watch?v={youtube_id}"
                    self.logger.info(f"🔗 YouTube link: {yt_link}")
            else:
                self.logger.info("⏭️  Skipping YouTube (API not available)")
            
            # Step 6: Post to TikTok
            if self.tiktok_uploader:
                self.logger.info("📤 Uploading to TikTok...")
                
                tiktok_id = self.tiktok_uploader.upload_video(
                    video_path=video_path,
                    title=content.title,
                    description=content.script[:300],
                    hashtags=content.hashtags[:10],
                    thumbnail_path=thumbnail_path
                )
                
                if tiktok_id:
                    content_metadata['tiktok_id'] = tiktok_id
                    self.logger.info(f"✓ Posted to TikTok: {tiktok_id}")
            
            # Save final metadata
            with open(os.path.join(content_dir, 'metadata.json'), 'w') as f:
                json.dump(content_metadata, f, indent=2)
            
            self.logger.info("=" * 60)
            self.logger.info("✓ Daily content generation and posting completed successfully!")
            self.logger.info("=" * 60)
            
            return True
        
        except Exception as e:
            self.logger.error(f"❌ Error in generate_and_post: {e}", exc_info=True)
            return False
    
    def schedule_daily_posting(self):
        """Schedule daily posting at specified time"""
        
        # Parse posting time (e.g., "09:00")
        hour, minute = map(int, self.posting_time.split(':'))
        
        # Add job with cron trigger
        self.scheduler.add_job(
            self.generate_and_post,
            trigger=CronTrigger(hour=hour, minute=minute),
            id='daily_posting',
            name='Daily content generation and posting',
            replace_existing=True
        )
        
        self.logger.info(f"✓ Scheduled daily posting at {self.posting_time}")
    
    def start(self):
        """Start the automation scheduler"""
        
        try:
            self.schedule_daily_posting()
            self.scheduler.start()
            
            self.logger.info("🚀 Automation system started!")
            self.logger.info(f"📅 Posting daily at {self.posting_time}")
            self.logger.info("Press Ctrl+C to stop the scheduler")
            
            # Keep the scheduler running
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("⏹️  Shutting down automation system...")
                self.scheduler.shutdown()
                self.logger.info("✓ Automation system stopped")
        
        except Exception as e:
            self.logger.error(f"❌ Error starting automation system: {e}", exc_info=True)
    
    def run_once(self):
        """Run content generation and posting once (useful for testing)"""
        self.logger.info("Running manual content generation...")
        return self.generate_and_post()
    
    def get_status(self) -> dict:
        """Get current system status"""
        return {
            'scheduler_running': self.scheduler.running,
            'youtube_ready': self.youtube_uploader is not None,
            'tiktok_ready': self.tiktok_uploader is not None,
            'posting_time': self.posting_time,
            'jobs': [job.name for job in self.scheduler.get_jobs()]
        }


def main():
    """Main entry point"""
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        # Ensure working directory is repository root so relative paths work
        repo_root = os.getenv('GITHUB_WORKSPACE', os.path.dirname(os.path.abspath(__file__)))
        try:
            os.chdir(repo_root)
        except Exception:
            pass
        print(f"Working directory: {os.getcwd()}")

        automation = AutomationSystem()
        
        if command == 'once':
            # Run content generation once
            print("\n🎬 Running content generation once...")
            success = automation.run_once()
            sys.exit(0 if success else 1)
        
        elif command == 'status':
            # Show status
            status = automation.get_status()
            print("\n📊 Automation System Status:")
            print(json.dumps(status, indent=2))
            sys.exit(0)
        
        elif command == 'start':
            # Start scheduler
            automation.start()
        
        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python main.py once     - Run content generation once")
            print("  python main.py status   - Show system status")
            print("  python main.py start    - Start daily scheduler")
            sys.exit(1)
    
    else:
        # Default: start the scheduler
        automation = AutomationSystem()
        automation.start()


if __name__ == "__main__":
    main()
