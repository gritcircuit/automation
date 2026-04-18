"""
Video Creator Module
Creates videos from scripts with text overlays and background music
"""

import os
from moviepy.editor import (
    ColorClip, CompositeVideoClip, TextClip,
    AudioFileClip, concatenate_videoclips
)
from pathlib import Path
from typing import Optional
import subprocess


class VideoCreator:
    """Creates videos from scripts and voiceover"""
    
    def __init__(self, output_dir: str = "videos"):
        """Initialize video creator"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def create_simple_video(
        self,
        script_text: str,
        title: str,
        duration: int = 60,
        bg_color: tuple = (26, 35, 126),  # Dark blue
        output_path: str = None,
        font_size: int = 60,
        font_path: str = None
    ) -> Optional[str]:
        """
        Create a simple motivational video with text overlay
        Uses vertical text animation (good for TikTok/Shorts)
        """
        
        if output_path is None:
            output_path = os.path.join(self.output_dir, f"video_{title.replace(' ', '_')}.mp4")
        
        try:
            # Create background clip
            background = ColorClip(
                size=(1080, 1920),  # TikTok/Shorts format (vertical)
                color=bg_color,
                duration=duration
            )
            
            # Create text clips
            lines = script_text.split('\n')
            clips = [background]
            
            # Default font
            if font_path is None:
                font_path = "Arial"
            
            # Calculate timing per line
            line_duration = duration / max(len(lines), 1)
            current_time = 0
            
            for i, line in enumerate(lines):
                if not line.strip():
                    continue
                
                # Create text with white color
                txt_clip = TextClip(
                    txt=line.strip(),
                    fontsize=font_size,
                    color='white',
                    font=font_path,
                    method='caption',
                    size=(1000, None),
                    align='center'
                ).set_duration(line_duration).set_start(current_time)
                
                # Position text in center
                txt_clip = txt_clip.set_position('center')
                clips.append(txt_clip)
                
                current_time += line_duration
            
            # Composite all clips
            final_video = CompositeVideoClip(clips)
            
            # Write video file (using ffmpeg codec for better compatibility)
            print(f"⏳ Creating video: {output_path}")
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio=False,
                verbose=False,
                logger=None
            )
            
            print(f"✓ Video created: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"❌ Error creating video: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def add_voiceover(
        self,
        video_path: str,
        audio_path: str,
        output_path: Optional[str] = None
    ) -> Optional[str]:
        """Add voiceover audio to video"""
        
        if output_path is None:
            base = os.path.splitext(video_path)[0]
            output_path = f"{base}_with_audio.mp4"
        
        try:
            print(f"⏳ Adding voiceover to video...")
            
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            
            # Trim audio to match video duration
            if audio_clip.duration > video_clip.duration:
                audio_clip = audio_clip.subclipped(0, video_clip.duration)
            
            # Set audio
            final_video = video_clip.set_audio(audio_clip)
            
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            print(f"✓ Video with audio created: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"❌ Error adding voiceover: {e}")
            return None
    
    def add_background_music(
        self,
        video_path: str,
        music_path: str,
        output_path: Optional[str] = None,
        music_volume: float = 0.5
    ) -> Optional[str]:
        """Add background music to video"""
        
        if output_path is None:
            base = os.path.splitext(video_path)[0]
            output_path = f"{base}_with_music.mp4"
        
        try:
            from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
            
            print(f"⏳ Adding background music...")
            
            video_clip = VideoFileClip(video_path)
            music_clip = AudioFileClip(music_path)
            
            # Trim or loop music to match video
            if music_clip.duration < video_clip.duration:
                # Simple approach: repeat music
                repeats = int(video_clip.duration / music_clip.duration) + 1
                music_clip = concatenate_audioclips([music_clip] * repeats)
            
            music_clip = music_clip.subclipped(0, video_clip.duration)
            music_clip = music_clip.volumex(music_volume)
            
            # Combine audio tracks if video has audio
            if video_clip.audio is not None:
                final_audio = CompositeAudioClip([
                    video_clip.audio,
                    music_clip
                ])
            else:
                final_audio = music_clip
            
            final_video = video_clip.set_audio(final_audio)
            
            final_video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            print(f"✓ Video with music created: {output_path}")
            return output_path
        
        except Exception as e:
            print(f"❌ Error adding music: {e}")
            return None


if __name__ == "__main__":
    creator = VideoCreator()
    
    test_script = """Start with your dream.
    
Take small steps.

Stay consistent.

Never give up."""
    
    video_path = creator.create_simple_video(
        script_text=test_script,
        title="motivation_test",
        duration=30
    )
    
    if video_path:
        print("✓ Test video created successfully!")
