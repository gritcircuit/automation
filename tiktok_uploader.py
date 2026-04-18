"""
TikTok Uploader Module
Handles TikTok API integration for posting videos
"""

import requests
import os
from typing import Optional, Dict
from datetime import datetime


class TikTokUploader:
    """Handles TikTok API uploads and scheduling"""
    
    # TikTok API Endpoints
    UPLOAD_URL = "https://open.tiktok.com/api/v1/ov/user/video/publish"
    SEARCH_SOUND_URL = "https://open.tiktok.com/api/v1/ov/search/sounds"
    
    def __init__(self, access_token: str, refresh_token: str):
        """Initialize TikTok uploader"""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.headers = self._get_headers()
    
    def _get_headers(self) -> Dict:
        """Get authorization headers"""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def refresh_access_token(self) -> bool:
        """Refresh access token if expired"""
        try:
            refresh_url = "https://open.tiktok.com/api/v1/oauth/token"
            
            payload = {
                "client_key": os.getenv('TIKTOK_CLIENT_KEY'),
                "client_secret": os.getenv('TIKTOK_CLIENT_SECRET'),
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token
            }
            
            response = requests.post(refresh_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access_token')
                self.headers = self._get_headers()
                print("✓ TikTok access token refreshed")
                return True
            else:
                print(f"❌ Failed to refresh token: {response.text}")
                return False
        
        except Exception as e:
            print(f"❌ Error refreshing TikTok token: {e}")
            return False
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        hashtags: list,
        thumbnail_path: Optional[str] = None,
        disable_comments: bool = False,
        disable_duet: bool = False,
        disable_stitch: bool = False
    ) -> Optional[str]:
        """Upload video to TikTok"""
        
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return None
        
        # Combine title, description, and hashtags
        caption = f"{title}\n\n{description}\n\n{' '.join(hashtags)}"
        caption = caption[:2200]  # TikTok caption limit
        
        try:
            # Prepare video file
            with open(video_path, "rb") as video_file:
                video_data = video_file.read()
            
            # Upload video with metadata
            files = {
                'video': (os.path.basename(video_path), video_data, 'video/mp4')
            }
            
            data = {
                'description': caption,
                'privacy_level': 'PUBLIC_TO_ANYONE',
                'video_cover_timestamp_ms': 0,
                'disable_comment': disable_comments,
                'disable_duet': disable_duet,
                'disable_stitch': disable_stitch
            }
            
            print(f"⏳ Uploading to TikTok: {title}")
            
            response = requests.post(
                self.UPLOAD_URL,
                headers=self.headers,
                files=files,
                data=data,
                timeout=300  # 5 minutes timeout
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                video_id = result.get('data', {}).get('video_id', result.get('id'))
                print(f"✓ Video uploaded to TikTok: {video_id}")
                return video_id
            else:
                print(f"❌ TikTok upload failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        
        except Exception as e:
            print(f"❌ Error uploading to TikTok: {e}")
            return None
    
    def schedule_video(
        self,
        video_path: str,
        title: str,
        description: str,
        hashtags: list,
        publish_time: datetime
    ) -> Optional[str]:
        """Schedule video for later publishing"""
        
        caption = f"{title}\n\n{description}\n\n{' '.join(hashtags)}"
        caption = caption[:2200]
        
        try:
            with open(video_path, "rb") as video_file:
                video_data = video_file.read()
            
            files = {
                'video': (os.path.basename(video_path), video_data, 'video/mp4')
            }
            
            data = {
                'description': caption,
                'privacy_level': 'PUBLIC_TO_ANYONE',
                'publish_type': 'SCHEDULED',
                'publish_time': int(publish_time.timestamp()),
                'video_cover_timestamp_ms': 0
            }
            
            print(f"⏳ Scheduling TikTok video: {title}")
            
            response = requests.post(
                self.UPLOAD_URL,
                headers=self.headers,
                files=files,
                data=data,
                timeout=300
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                video_id = result.get('data', {}).get('video_id', result.get('id'))
                print(f"✓ Video scheduled for TikTok: {video_id}")
                return video_id
            else:
                print(f"❌ TikTok scheduling failed: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"❌ Error scheduling TikTok video: {e}")
            return None
    
    def get_user_info(self) -> Optional[Dict]:
        """Get authenticated user information"""
        try:
            url = "https://open.tiktok.com/api/v1/user/info"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    user = data['data']['user']
                    return {
                        'username': user.get('display_name'),
                        'user_id': user.get('open_id'),
                        'avatar': user.get('avatar_url'),
                        'bio': user.get('bio_description')
                    }
        except Exception as e:
            print(f"⚠️ Error fetching user info: {e}")
        
        return None
    
    def search_sounds(self, keyword: str, limit: int = 10) -> list:
        """Search for sounds/music on TikTok"""
        try:
            params = {
                'search_term': keyword,
                'count': limit
            }
            
            response = requests.get(
                self.SEARCH_SOUND_URL,
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                sounds = data.get('data', {}).get('sounds', [])
                return sounds
        
        except Exception as e:
            print(f"⚠️ Error searching sounds: {e}")
        
        return []


if __name__ == "__main__":
    print("TikTok API client initialized. To use:")
    print("1. Set TIKTOK_ACCESS_TOKEN environment variable")
    print("2. Set TIKTOK_REFRESH_TOKEN environment variable")
    print("3. Create TikTokUploader instance")
    print("4. Use upload_video() method")
