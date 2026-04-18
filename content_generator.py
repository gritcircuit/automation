"""
Content Generator Module
Generates motivational content using OpenAI and creates video/audio
"""

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("WARNING: OpenAI not available - using fallback content only")

import os
from typing import Dict
from datetime import datetime
from pydantic import BaseModel


class GeneratedContent(BaseModel):
    """Model for generated content"""
    title: str
    script: str
    hashtags: list[str]
    thumbnail_text: str
    duration: int


class ContentGenerator:
    """Generates AI-based motivational content"""
    
    def __init__(self, api_key: str):
        """Initialize OpenAI client"""
        if not OPENAI_AVAILABLE:
            print("⚠️ OpenAI library not available - content generation will use fallback")
            self.client = None
        elif not api_key:
            print("⚠️ OpenAI API key not provided - content generation will use fallback")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"  # Use turbo for faster/cheaper results
    
    def generate_motivation_post(self) -> GeneratedContent:
        """Generate a motivational post with title, script, and metadata"""
        
        if not self.client:
            print("Using fallback content (OpenAI not available or no API key)")
            return GeneratedContent(
                title="Your Success Awaits",
                script="Every day is a new opportunity. Don't wait for the perfect moment. Start now, make mistakes, learn, and grow. Your future self will thank you for taking action today.",
                hashtags=["#Motivation", "#Success", "#Inspire", "#GrowthMindset", "#Goals", "#Action", "#Believe", "#Hustle"],
                thumbnail_text="Start Now",
                duration=60
            )
        
        prompt = """Generate a short, inspiring motivational post for social media.
        
        Return JSON with these exact fields:
        - title: catchy title (max 60 chars)
        - script: short script for voiceover (150-200 words)
        - hashtags: list of 8-10 relevant hashtags
        - thumbnail_text: one-liner for thumbnail (max 20 chars)
        
        Make it original, engaging, and suitable for teens/young adults.
        Focus on success, perseverance, and personal growth."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a motivational content creator. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            # Parse response
            import json
            content = json.loads(response.choices[0].message.content)
            
            return GeneratedContent(
                title=content['title'],
                script=content['script'],
                hashtags=content['hashtags'],
                thumbnail_text=content['thumbnail_text'],
                duration=60
            )
        
        except Exception as e:
            print(f"Error generating content: {e}")
            # Fallback content
            return GeneratedContent(
                title="Your Success Awaits",
                script="Every day is a new opportunity. Don't wait for the perfect moment. Start now, make mistakes, learn, and grow. Your future self will thank you for taking action today.",
                hashtags=["#Motivation", "#Success", "#Inspire", "#GrowthMindset", "#Goals", "#Action", "#Believe", "#Hustle"],
                thumbnail_text="Start Now",
                duration=60
            )
    
    def generate_video_script_voiceover(self, script: str, output_path: str):
        """Convert script to audio using text-to-speech (requires pyttsx3)"""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 130)  # Words per minute
            engine.setProperty('volume', 0.9)
            engine.save_to_file(script, output_path)
            engine.runAndWait()
            print(f"✓ Voiceover generated: {output_path}")
        except ImportError:
            print("pyttsx3 not installed. Install with: pip install pyttsx3")
    
    def create_content_file(self, content: GeneratedContent, output_dir: str) -> Dict:
        """Save generated content to files"""
        os.makedirs(output_dir, exist_ok=True)
        
        content_metadata = {
            'timestamp': datetime.now().isoformat(),
            'title': content.title,
            'script': content.script,
            'hashtags': ' '.join(content.hashtags),
            'thumbnail_text': content.thumbnail_text,
            'duration': content.duration
        }
        
        # Save metadata
        import json
        metadata_path = os.path.join(output_dir, 'content_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(content_metadata, f, indent=2)
        
        # Save script
        script_path = os.path.join(output_dir, 'script.txt')
        with open(script_path, 'w') as f:
            f.write(content.script)
        
        content_metadata['metadata_path'] = metadata_path
        content_metadata['script_path'] = script_path
        
        return content_metadata


if __name__ == "__main__":
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not set in environment")
        exit(1)
    
    generator = ContentGenerator(api_key)
    content = generator.generate_motivation_post()
    print(f"Title: {content.title}")
    print(f"Script: {content.script}")
    print(f"Hashtags: {' '.join(content.hashtags)}")
