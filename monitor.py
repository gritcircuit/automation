"""
Real-Time Monitoring Dashboard
Monitor your automation system status and activity
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
import subprocess


class DashboardMonitor:
    """Monitor system activity in real-time"""
    
    def __init__(self):
        self.log_file = "logs/automation.log"
        self.content_dir = "generated_content"
        
    def get_scheduler_status(self) -> dict:
        """Check if scheduler is running"""
        try:
            result = subprocess.run(
                ['tasklist', '/FI', 'IMAGENAME eq python.exe'],
                capture_output=True,
                text=True
            )
            is_running = 'python.exe' in result.stdout
            return {
                'running': is_running,
                'status': '✅ RUNNING' if is_running else '❌ STOPPED'
            }
        except:
            return {'running': False, 'status': '⚠️  UNABLE TO DETECT'}
    
    def get_latest_posts(self, limit: int = 5) -> list:
        """Get the last N generated posts"""
        if not os.path.exists(self.content_dir):
            return []
        
        posts = []
        dirs = sorted(os.listdir(self.content_dir), reverse=True)[:limit]
        
        for dir_name in dirs:
            metadata_path = os.path.join(self.content_dir, dir_name, 'metadata.json')
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        data = json.load(f)
                        data['timestamp'] = dir_name
                        posts.append(data)
                except:
                    pass
        
        return posts
    
    def get_recent_logs(self, lines: int = 20) -> str:
        """Get recent log entries"""
        if not os.path.exists(self.log_file):
            return "No logs yet..."
        
        try:
            with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                all_lines = f.readlines()
                return ''.join(all_lines[-lines:])
        except:
            return "Unable to read logs..."
    
    def get_system_stats(self) -> dict:
        """Get system statistics"""
        total_posts = 0
        total_videos = 0
        
        if os.path.exists(self.content_dir):
            for item in os.listdir(self.content_dir):
                if os.path.isdir(os.path.join(self.content_dir, item)):
                    total_posts += 1
                    video_path = os.path.join(self.content_dir, item, 'video.mp4')
                    if os.path.exists(video_path):
                        total_videos += 1
        
        return {
            'total_posts': total_posts,
            'total_videos': total_videos,
            'last_post': self.get_latest_posts(1)[0]['timestamp'] if self.get_latest_posts(1) else 'None'
        }
    
    def display_dashboard(self):
        """Display the monitoring dashboard"""
        while True:
            # Clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print("\n" + "="*70)
            print("    🚀 YOUTUBE & TIKTOK AUTO-POSTING SYSTEM - MONITORING DASHBOARD")
            print("="*70)
            
            # Scheduler Status
            print("\n" + "─"*70)
            print("📊 SCHEDULER STATUS")
            print("─"*70)
            status = self.get_scheduler_status()
            print(f"{status['status']}")
            print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # System Stats
            print("\n" + "─"*70)
            print("📈 SYSTEM STATISTICS")
            print("─"*70)
            stats = self.get_system_stats()
            print(f"✓ Total Posts Generated: {stats['total_posts']}")
            print(f"✓ Total Videos Created: {stats['total_videos']}")
            print(f"✓ Last Post: {stats['last_post']}")
            
            # Recent Posts
            print("\n" + "─"*70)
            print("📝 RECENT POSTS (Last 3)")
            print("─"*70)
            posts = self.get_latest_posts(3)
            if posts:
                for i, post in enumerate(posts, 1):
                    print(f"\n  {i}. {post.get('title', 'Untitled')}")
                    print(f"     Time: {post['timestamp']}")
                    print(f"     Hashtags: {', '.join(post.get('hashtags', [])[:3])}...")
            else:
                print("  No posts yet...")
            
            # Recent Activity Log
            print("\n" + "─"*70)
            print("📋 RECENT ACTIVITY (Last 10 lines)")
            print("─"*70)
            logs = self.get_recent_logs(10)
            for line in logs.split('\n'):
                if line.strip():
                    # Clean up the line for display
                    line = line.replace('✓', '√').replace('❌', 'X').replace('✅', '√')
                    print(f"  {line[:68]}")
            
            # Instructions
            print("\n" + "─"*70)
            print("⌨️  CONTROLS")
            print("─"*70)
            print("  [Enter] - Refresh (auto-refreshes in 30 seconds)")
            print("  [Q]     - Quit dashboard")
            print("  [C]     - Check logs in editor")
            print("  [S]     - Show full stats")
            
            print("\n" + "="*70 + "\n")
            
            try:
                user_input = input("Enter command (or press Enter to refresh): ").lower().strip()
                
                if user_input == 'q':
                    print("Exiting dashboard...")
                    break
                elif user_input == 'c':
                    os.system(f'notepad {self.log_file}')
                elif user_input == 's':
                    self.show_full_stats()
                else:
                    time.sleep(30)
                    
            except KeyboardInterrupt:
                print("\n\nExiting dashboard...")
                break
    
    def show_full_stats(self):
        """Show detailed statistics"""
        print("\n" + "="*70)
        print("📊 DETAILED STATISTICS")
        print("="*70)
        
        posts = self.get_latest_posts(100)
        
        print(f"\nTotal Posts: {len(posts)}")
        
        if posts:
            print("\nRecent Posts:")
            for post in posts[:10]:
                print(f"\n  • {post.get('title', 'Untitled')}")
                print(f"    Generated: {post['timestamp']}")
                print(f"    Script: {post.get('script', '')[:100]}...")
        
        input("\nPress Enter to return to dashboard...")


def main():
    """Main monitoring dashboard"""
    print("\n🚀 Starting Monitoring Dashboard...\n")
    time.sleep(2)
    
    monitor = DashboardMonitor()
    monitor.display_dashboard()


if __name__ == "__main__":
    main()
