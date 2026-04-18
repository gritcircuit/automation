"""
Testing & Debugging Script
Helps verify all components are working correctly
"""

import os
import sys
from dotenv import load_dotenv
import json


class SystemTester:
    """Test all system components"""
    
    def __init__(self):
        load_dotenv()
        self.results = {}
    
    def test_environment(self):
        """Test environment variables"""
        print("\n" + "="*60)
        print("🔐 ENVIRONMENT VARIABLES TEST")
        print("="*60)
        
        required_vars = [
            'OPENAI_API_KEY',
            'YOUTUBE_CLIENT_ID',
            'YOUTUBE_CLIENT_SECRET',
            'YOUTUBE_REFRESH_TOKEN',
            'TIKTOK_ACCESS_TOKEN',
            'TIKTOK_REFRESH_TOKEN'
        ]
        
        results = {}
        for var in required_vars:
            value = os.getenv(var)
            if value:
                masked = value[:10] + "..." if len(value) > 10 else value
                print(f"✓ {var}: {masked}")
                results[var] = "FOUND"
            else:
                print(f"❌ {var}: NOT FOUND")
                results[var] = "MISSING"
        
        self.results['environment'] = results
    
    def test_packages(self):
        """Test Python package imports"""
        print("\n" + "="*60)
        print("📦 PYTHON PACKAGES TEST")
        print("="*60)
        
        packages = {
            'openai': 'OpenAI API',
            'google.auth': 'Google Auth',
            'google.oauth2': 'Google OAuth2',
            'google_auth_oauthlib': 'Google Auth OAuthLib',
            'google_auth_httplib2': 'Google Auth HTTPLib2',
            'googleapiclient': 'Google API Client',
            'requests': 'HTTP Library',
            'PIL': 'Pillow (Image Processing)',
            'moviepy': 'MoviePy (Video Processing)',
            'apscheduler': 'APScheduler',
            'pydantic': 'Pydantic',
            'dotenv': 'Python-dotenv'
        }
        
        results = {}
        for package, name in packages.items():
            try:
                __import__(package)
                print(f"✓ {name} ({package})")
                results[package] = "OK"
            except ImportError:
                print(f"❌ {name} ({package}) - MISSING")
                results[package] = "MISSING"
        
        self.results['packages'] = results
    
    def test_file_structure(self):
        """Test project file structure"""
        print("\n" + "="*60)
        print("📁 FILE STRUCTURE TEST")
        print("="*60)
        
        required_files = [
            'main.py',
            'content_generator.py',
            'thumbnail_generator.py',
            'video_creator.py',
            'youtube_uploader.py',
            'tiktok_uploader.py',
            'requirements.txt',
            '.env',
            'README.md'
        ]
        
        results = {}
        for file in required_files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"✓ {file} ({size} bytes)")
                results[file] = "EXISTS"
            else:
                print(f"❌ {file} - MISSING")
                results[file] = "MISSING"
        
        self.results['files'] = results
    
    def test_openai_connection(self):
        """Test OpenAI API connection"""
        print("\n" + "="*60)
        print("🤖 OPENAI API TEST")
        print("="*60)
        
        try:
            import openai
            api_key = os.getenv('OPENAI_API_KEY')
            
            if not api_key:
                print("❌ OpenAI API key not found")
                self.results['openai'] = "API_KEY_MISSING"
                return
            
            client = openai.OpenAI(api_key=api_key)
            
            print("⏳ Testing connection...")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            
            if response:
                print(f"✓ Connection successful!")
                print(f"  Model: {response.model}")
                print(f"  Tokens used: {response.usage.total_tokens}")
                self.results['openai'] = "OK"
        
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            self.results['openai'] = f"ERROR: {str(e)}"
    
    def test_youtube_credentials(self):
        """Test YouTube credentials"""
        print("\n" + "="*60)
        print("🎥 YOUTUBE API TEST")
        print("="*60)
        
        try:
            from youtube_uploader import YouTubeUploader
            
            if not os.path.exists('credentials.json'):
                print("⚠️  credentials.json not found")
                print("   Would be created on first YouTube API call")
                self.results['youtube'] = "CREDENTIALS_MISSING"
                return
            
            print("⏳ Testing YouTube authentication...")
            uploader = YouTubeUploader()
            
            if uploader.youtube:
                stats = uploader.get_channel_stats()
                if stats:
                    print(f"✓ YouTube authentication successful!")
                    for key, value in stats.items():
                        print(f"  {key}: {value}")
                    self.results['youtube'] = "OK"
                else:
                    print("⚠️  Authenticated but couldn't fetch channel stats")
                    self.results['youtube'] = "PARTIAL"
        
        except Exception as e:
            print(f"⚠️  YouTube test: {e}")
            self.results['youtube'] = f"ERROR: {str(e)}"
    
    def test_tiktok_credentials(self):
        """Test TikTok credentials"""
        print("\n" + "="*60)
        print("🎵 TIKTOK API TEST")
        print("="*60)
        
        try:
            from tiktok_uploader import TikTokUploader
            
            access_token = os.getenv('TIKTOK_ACCESS_TOKEN')
            refresh_token = os.getenv('TIKTOK_REFRESH_TOKEN')
            
            if not access_token or not refresh_token:
                print("❌ TikTok tokens not found in .env")
                self.results['tiktok'] = "MISSING_TOKENS"
                return
            
            print("⏳ Testing TikTok authentication...")
            uploader = TikTokUploader(access_token, refresh_token)
            
            user_info = uploader.get_user_info()
            
            if user_info:
                print(f"✓ TikTok authentication successful!")
                for key, value in user_info.items():
                    print(f"  {key}: {value}")
                self.results['tiktok'] = "OK"
            else:
                print("⚠️  Authenticated but couldn't fetch user info")
                self.results['tiktok'] = "PARTIAL"
        
        except Exception as e:
            print(f"⚠️  TikTok test: {e}")
            self.results['tiktok'] = f"ERROR: {str(e)}"
    
    def test_content_generator(self):
        """Test content generation"""
        print("\n" + "="*60)
        print("📝 CONTENT GENERATION TEST")
        print("="*60)
        
        try:
            from content_generator import ContentGenerator
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                print("❌ OpenAI API key required")
                self.results['content_generation'] = "API_KEY_MISSING"
                return
            
            print("⏳ Generating sample content...")
            generator = ContentGenerator(api_key)
            content = generator.generate_motivation_post()
            
            print(f"✓ Content generated successfully!")
            print(f"  Title: {content.title}")
            print(f"  Duration: {content.duration}s")
            print(f"  Hashtags: {len(content.hashtags)}")
            
            self.results['content_generation'] = "OK"
        
        except Exception as e:
            print(f"❌ Content generation failed: {e}")
            self.results['content_generation'] = f"ERROR: {str(e)}"
    
    def test_thumbnail_generator(self):
        """Test thumbnail generation"""
        print("\n" + "="*60)
        print("🎨 THUMBNAIL GENERATOR TEST")
        print("="*60)
        
        try:
            from thumbnail_generator import ThumbnailGenerator
            import os
            
            print("⏳ Generating test thumbnail...")
            generator = ThumbnailGenerator()
            
            output_path = "test_thumbnail.jpg"
            generator.create_thumbnail(
                title="Test Motivation",
                thumbnail_text="START NOW",
                output_path=output_path
            )
            
            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"✓ Thumbnail generated successfully!")
                print(f"  File: {output_path}")
                print(f"  Size: {size} bytes")
                self.results['thumbnail_generation'] = "OK"
            else:
                print(f"❌ Thumbnail file not created")
                self.results['thumbnail_generation'] = "FILE_NOT_CREATED"
        
        except Exception as e:
            print(f"❌ Thumbnail generation failed: {e}")
            self.results['thumbnail_generation'] = f"ERROR: {str(e)}"
    
    def test_video_creator(self):
        """Test video creation"""
        print("\n" + "="*60)
        print("🎬 VIDEO CREATOR TEST")
        print("="*60)
        
        try:
            from video_creator import VideoCreator
            import os
            
            print("⏳ Creating test video (30 seconds)...")
            creator = VideoCreator()
            
            output_path = "test_video.mp4"
            video_path = creator.create_simple_video(
                script_text="Test video creation.\nThis is a test.\nSuccess!",
                title="test",
                duration=10,
                output_path=output_path
            )
            
            if video_path and os.path.exists(video_path):
                size = os.path.getsize(video_path)
                print(f"✓ Video created successfully!")
                print(f"  File: {video_path}")
                print(f"  Size: {size / (1024*1024):.2f} MB")
                self.results['video_creation'] = "OK"
            else:
                print(f"❌ Video file not created")
                self.results['video_creation'] = "FILE_NOT_CREATED"
        
        except Exception as e:
            print(f"❌ Video creation failed: {e}")
            self.results['video_creation'] = f"ERROR: {str(e)}"
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        total = 0
        passed = 0
        failed = 0
        
        for category, results in self.results.items():
            print(f"\n{category.upper()}:")
            
            if isinstance(results, dict):
                for key, value in results.items():
                    total += 1
                    if value == "OK" or value == "FOUND" or value == "EXISTS":
                        print(f"  ✓ {key}")
                        passed += 1
                    else:
                        print(f"  ❌ {key}: {value}")
                        failed += 1
            else:
                total += 1
                if results == "OK":
                    print(f"  ✓ Passed")
                    passed += 1
                else:
                    print(f"  ❌ {results}")
                    failed += 1
        
        print(f"\n" + "="*60)
        print(f"Results: {passed}/{total} passed, {failed}/{total} failed")
        print("="*60)
        
        if failed == 0:
            print("\n✅ All tests passed! System is ready to use.")
            print("\nRun: python main.py once")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Check errors above.")
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n🔧 RUNNING SYSTEM TESTS\n")
        
        self.test_environment()
        self.test_packages()
        self.test_file_structure()
        self.test_openai_connection()
        self.test_youtube_credentials()
        self.test_tiktok_credentials()
        self.test_content_generator()
        self.test_thumbnail_generator()
        self.test_video_creator()
        
        self.print_summary()


def main():
    """Main entry point"""
    try:
        tester = SystemTester()
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n❌ Testing interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
