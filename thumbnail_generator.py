"""
Thumbnail Generator Module
Creates custom thumbnail images with dynamic text overlays
Supports multiple aspect ratios: YouTube, TikTok, Instagram, custom
"""

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("WARNING: PIL not available - thumbnail generation disabled")

import os
from typing import Tuple, Optional, Dict
from datetime import datetime
import textwrap


class ThumbnailGenerator:
    """Generates custom thumbnails with flexible sizing for different platforms"""
    
    # Platform presets
    PRESETS = {
        'youtube': {'width': 1280, 'height': 720, 'name': 'YouTube'},
        'tiktok': {'width': 1080, 'height': 1920, 'name': 'TikTok/Reels'},
        'instagram': {'width': 1080, 'height': 1080, 'name': 'Instagram Square'},
        'instagram_story': {'width': 1080, 'height': 1920, 'name': 'Instagram Story'},
        'twitter': {'width': 1200, 'height': 675, 'name': 'Twitter'},
        'custom': None  # Custom size specified by user
    }
    
class ThumbnailGenerator:
    """Generates custom thumbnails with flexible sizing for different platforms"""
    
    # Platform presets
    PRESETS = {
        'youtube': {'width': 1280, 'height': 720, 'name': 'YouTube'},
        'tiktok': {'width': 1080, 'height': 1920, 'name': 'TikTok/Reels'},
        'instagram': {'width': 1080, 'height': 1080, 'name': 'Instagram Square'},
        'instagram_story': {'width': 1080, 'height': 1920, 'name': 'Instagram Story'},
        'twitter': {'width': 1200, 'height': 675, 'name': 'Twitter'},
        'custom': None  # Custom size specified by user
    }
    
    def __init__(self, width: int = 1280, height: int = 720, platform: str = 'youtube'):
        """
        Initialize thumbnail generator
        
        Args:
            width: Thumbnail width in pixels
            height: Thumbnail height in pixels
            platform: Use preset dimensions ('youtube', 'tiktok', 'instagram', etc.)
        """
        if not PIL_AVAILABLE:
            print("⚠️ PIL not available - thumbnail generation disabled")
            self.width = width
            self.height = height
            self.platform = platform
            return
            
        # Load preset if specified
        if platform in self.PRESETS and self.PRESETS[platform]:
            preset = self.PRESETS[platform]
            self.width = preset['width']
            self.height = preset['height']
            self.platform = platform
        else:
            self.width = width
            self.height = height
            self.platform = 'custom'
        
        # Calculate scale factor for dynamic sizing
        self.base_width = 1280  # Reference size for font calculations
        self.scale_factor = self.width / self.base_width
        
        # Determine if portrait (taller than wide)
        self.is_portrait = self.height > self.width
        
        self.bg_colors = [
            (255, 67, 54),    # Red
            (251, 188, 5),    # Gold
            (52, 168, 224),   # Blue
            (156, 39, 176),   # Purple
            (0, 150, 136),    # Teal
        ]
    
    def create_thumbnail(
        self,
        title: str,
        thumbnail_text: str,
        output_path: str,
        bg_color: Optional[Tuple] = None,
        quality: int = 95
    ) -> str:
        """
        Create a custom thumbnail with title and text overlay
        
        Args:
            title: Thumbnail title/heading
            thumbnail_text: Main text on thumbnail
            output_path: Where to save the thumbnail
            bg_color: RGB tuple for background (random if None)
            quality: JPEG quality (1-95)
        
        Returns:
            Path to created thumbnail
        """
        
        if not PIL_AVAILABLE:
            print(f"⚠️ PIL not available - creating placeholder thumbnail at {output_path}")
            # Create a simple placeholder file
            with open(output_path, 'w') as f:
                f.write("Placeholder thumbnail - PIL not available")
            return output_path
        
        # Select background color
        if bg_color is None:
            import random
            bg_color = random.choice(self.bg_colors)
        
        # Create base image
        img = Image.new('RGB', (self.width, self.height), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect
        self._add_gradient_overlay(img)
        
        # Calculate dynamic font sizes based on image dimensions
        title_size = self._calc_font_size(80)
        text_size = self._calc_font_size(120)
        badge_size = self._calc_font_size(30)
        
        # Try to load fonts, fallback to default
        try:
            title_font = ImageFont.truetype("arial.ttf", title_size)
            text_font = ImageFont.truetype("arial.ttf", text_size)
            badge_font = ImageFont.truetype("arial.ttf", badge_size)
        except IOError:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            badge_font = ImageFont.load_default()
        
        # White text for contrast
        text_color = (255, 255, 255)
        
        # Calculate positions based on aspect ratio
        if self.is_portrait:
            # For vertical layouts (TikTok, Instagram Story, etc.)
            title_y = int(self.height * 0.15)
            text_y = int(self.height * 0.5)
        else:
            # For horizontal layouts (YouTube, Twitter, etc.)
            title_y = int(self.height * 0.15)
            text_y = int(self.height * 0.5)
        
        # Add title at top
        self._draw_text_with_outline(
            draw,
            title,
            (self.width // 2, title_y),
            font=title_font,
            fill=text_color,
            outline_width=self._calc_font_size(4),
            anchor="mm"
        )
        
        # Add main text in center
        self._draw_text_with_outline(
            draw,
            thumbnail_text,
            (self.width // 2, text_y),
            font=text_font,
            fill=text_color,
            outline_width=self._calc_font_size(4),
            anchor="mm"
        )
        
        # Add timestamp badge
        timestamp = datetime.now().strftime("%Y-%m-%d")
        badge_text = f"NEW | {timestamp}"
        
        # Position badge appropriately based on aspect ratio
        if self.is_portrait:
            badge_x = self.width // 2
            badge_y = int(self.height * 0.9)
        else:
            badge_x = self.width - int(self.width * 0.2)
            badge_y = self.height - int(self.height * 0.1)
        
        self._draw_text_with_outline(
            draw,
            badge_text,
            (badge_x, badge_y),
            font=badge_font,
            fill=(255, 215, 0),
            outline_width=self._calc_font_size(2),
            anchor="mm"
        )
        
        # Save thumbnail
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, quality=quality)
        print(f"✓ Thumbnail created: {output_path} ({self.width}x{self.height} - {self.platform})")
        
        return output_path
    
    def _calc_font_size(self, base_size: int) -> int:
        """Calculate font size based on scale factor for responsive sizing"""
        return int(base_size * self.scale_factor)
    
    def _add_gradient_overlay(self, img: Image.Image):
        """Add subtle gradient overlay to the image"""
        gradient = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        grad_draw = ImageDraw.Draw(gradient)
        
        # Create dark overlay at bottom for text contrast
        for y in range(self.height):
            alpha = int((y / self.height) * 100)
            grad_draw.rectangle(
                [(0, y), (self.width, y + 1)],
                fill=(0, 0, 0, alpha)
            )
        
        img.paste(Image.alpha_composite(img.convert('RGBA'), gradient).convert('RGB'))
    
    def _draw_text_with_outline(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        position: Tuple,
        font: ImageFont.FreeTypeFont,
        fill: Tuple = (255, 255, 255),
        outline_color: Tuple = (0, 0, 0),
        outline_width: int = 4,
        anchor: str = "mm"
    ):
        """Draw text with outline for better readability"""
        x, y = position
        
        # Text outline
        for adj_x in range(-outline_width, outline_width + 1):
            for adj_y in range(-outline_width, outline_width + 1):
                if adj_x != 0 or adj_y != 0:
                    draw.text(
                        (x + adj_x, y + adj_y),
                        text,
                        font=font,
                        fill=outline_color,
                        anchor=anchor,
                        align="center"
                    )
        
        # Main text
        draw.text(
            position,
            text,
            font=font,
            fill=fill,
            anchor=anchor,
            align="center"
        )
    
    def create_batch_thumbnails(
        self,
        content_list: list,
        output_dir: str
    ) -> list:
        """Create multiple thumbnails at once"""
        generated_paths = []
        
        for i, content in enumerate(content_list):
            output_path = os.path.join(
                output_dir,
                f"thumbnail_{i+1}.jpg"
            )
            
            path = self.create_thumbnail(
                title=content.get('title', 'Motivation'),
                thumbnail_text=content.get('thumbnail_text', 'Inspire'),
                output_path=output_path
            )
            generated_paths.append(path)
        
        return generated_paths


if __name__ == "__main__":
    # Test creating thumbnails for different platforms
    output_dir = "thumbnails"
    os.makedirs(output_dir, exist_ok=True)
    
    test_content = {
        'title': 'Motivation',
        'thumbnail_text': 'START NOW'
    }
    
    print("🎬 Creating thumbnails for multiple platforms...\n")
    
    # Create for different platforms
    for platform in ['youtube', 'tiktok', 'instagram', 'twitter']:
        generator = ThumbnailGenerator(platform=platform)
        output_path = os.path.join(output_dir, f"test_{platform}.jpg")
        
        generator.create_thumbnail(
            title=test_content['title'],
            thumbnail_text=test_content['thumbnail_text'],
            output_path=output_path
        )
    
    # Custom size example
    generator_custom = ThumbnailGenerator(width=800, height=600, platform='custom')
    generator_custom.create_thumbnail(
        title='Custom Size',
        thumbnail_text='800x600',
        output_path=os.path.join(output_dir, 'test_custom.jpg')
    )
    
    print("\n✅ All test thumbnails created successfully!")
