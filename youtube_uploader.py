"""
YouTube Uploader Module
Handles authentication and video uploads to YouTube
"""

import os
import pickle
from typing import Dict, Optional

try:
    import google_auth_oauthlib.flow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.api_python_client.discovery import build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    print("WARNING: Google API client not available - YouTube uploads disabled")
import time


class YouTubeUploader:
    """Handles YouTube API authentication and video uploads"""
    
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    
    def __init__(self, credentials_file: str = "credentials.json"):
        """Initialize YouTube uploader"""
        if not GOOGLE_API_AVAILABLE:
            print("⚠️ Google API not available - YouTube uploads disabled")
            self.youtube = None
            return
            
        self.credentials_file = credentials_file
        self.youtube = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with YouTube API using OAuth2"""
        if not GOOGLE_API_AVAILABLE:
            return
            
        creds = None
        
        # Load existing credentials
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        
        # Try to use environment variables for authentication
        client_id = os.getenv('YOUTUBE_CLIENT_ID')
        client_secret = os.getenv('YOUTUBE_CLIENT_SECRET')
        refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')
        
        if client_id and client_secret and refresh_token:
            # Create credentials from environment variables
            creds = Credentials(
                token=None,  # Will be obtained via refresh
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret,
                token_uri="https://oauth2.googleapis.com/token",
                scopes=self.SCOPES
            )
            # Refresh the token
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"❌ Failed to refresh YouTube credentials: {e}")
                creds = None
        elif creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif not creds or not creds.valid:
            if not os.path.exists(self.credentials_file):
                print("⚠️ No valid YouTube credentials found. YouTube uploads will be disabled.")
                print("To enable YouTube uploads, either:")
                print("1. Set YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN environment variables")
                print("2. Or provide credentials.json file")
                return  # Don't raise exception, just disable YouTube
            
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file,
                scopes=self.SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        if creds:
            # Save credentials
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
            
            # Build YouTube API client
            self.youtube = build(
                self.API_SERVICE_NAME,
                self.API_VERSION,
                credentials=creds
            )
            
            print("✓ YouTube authentication successful")
        else:
            self.youtube = None
            print("⚠️ YouTube authentication failed - uploads disabled")
    
    def upload_video(
        self,
        video_path: str,
        thumbnail_path: str,
        title: str,
        description: str,
        tags: list,
        privacy_status: str = "public",
        made_for_kids: bool = False
    ) -> Optional[str]:
        """Upload video to YouTube with thumbnail"""
        
        if not self.youtube:
            print("⚠️ YouTube API not available - skipping upload")
            return None
        
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return None
        
        try:
            request_body = {
                "snippet": {
                    "title": title[:100],  # Max 100 chars
                    "description": description[:5000],  # Max 5000 chars
                    "tags": tags[:30],  # Max 30 tags
                    "categoryId": "29"  # Category: Nonprofits & Activism
                },
                "status": {
                    "privacyStatus": privacy_status,
                    "madeForKids": made_for_kids
                },
                "processingDetails": {
                    "processingStatus": "processing"
                }
            }
            
            # Upload video
            print(f"⏳ Uploading video: {title}")
            with open(video_path, "rb") as video_file:
                request = self.youtube.videos().insert(
                    part="snippet,status",
                    body=request_body,
                    media_body=video_file,
                    notifySubscribers=False
                )
                response = request.execute()
            
            video_id = response.get("id")
            print(f"✓ Video uploaded: {video_id}")
            
            # Upload thumbnail (wait a bit for processing)
            time.sleep(2)
            if os.path.exists(thumbnail_path):
                self._upload_thumbnail(video_id, thumbnail_path)
            
            return video_id
        
        except Exception as e:
            print(f"❌ Error uploading to YouTube: {e}")
            return None
    
    def _upload_thumbnail(self, video_id: str, thumbnail_path: str):
        """Upload custom thumbnail"""
        try:
            with open(thumbnail_path, "rb") as thumbnail_file:
                request = self.youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=thumbnail_file
                )
                request.execute()
            
            print(f"✓ Thumbnail uploaded for video {video_id}")
        except Exception as e:
            print(f"⚠️ Failed to upload thumbnail: {e}")
    
    def schedule_for_later(
        self,
        video_path: str,
        thumbnail_path: str,
        title: str,
        description: str,
        tags: list,
        publish_time: str  # ISO 8601 format: 2024-01-15T10:00:00Z
    ) -> Optional[str]:
        """Upload video and schedule for later publishing"""
        
        try:
            with open(video_path, "rb") as video_file:
                request_body = {
                    "snippet": {
                        "title": title[:100],
                        "description": description[:5000],
                        "tags": tags[:30],
                        "categoryId": "29"
                    },
                    "status": {
                        "privacyStatus": "private",  # Private until scheduled time
                        "publishAt": publish_time,
                        "madeForKids": False
                    }
                }
                
                request = self.youtube.videos().insert(
                    part="snippet,status",
                    body=request_body,
                    media_body=video_file
                )
                response = request.execute()
            
            video_id = response.get("id")
            print(f"✓ Video scheduled for publishing: {video_id}")
            
            # Upload thumbnail
            time.sleep(2)
            if os.path.exists(thumbnail_path):
                self._upload_thumbnail(video_id, thumbnail_path)
            
            return video_id
        
        except Exception as e:
            print(f"❌ Error scheduling video: {e}")
            return None
    
    def get_channel_stats(self) -> Dict:
        """Get YouTube channel statistics"""
        try:
            request = self.youtube.channels().list(
                part="statistics,snippet",
                mine=True
            )
            response = request.execute()
            
            if response["items"]:
                channel = response["items"][0]
                return {
                    "channelName": channel["snippet"]["title"],
                    "subscribers": channel["statistics"].get("subscriberCount", "N/A"),
                    "videoCount": channel["statistics"].get("videoCount", "0"),
                    "views": channel["statistics"].get("viewCount", "0")
                }
        except Exception as e:
            print(f"⚠️ Error fetching channel stats: {e}")
        
        return {}


if __name__ == "__main__":
    print("YouTube API client initialized. To use:")
    print("1. Ensure credentials.json is in the working directory")
    print("2. Create YouTubeUploader instance")
    print("3. Use upload_video() method")
