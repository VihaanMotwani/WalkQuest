from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class ColorBoxLayout(BoxLayout):
    """Base class for colored placeholder boxes"""
    def __init__(self, bg_color=(0.2, 0.2, 0.2, 1), **kwargs):
        super().__init__(**kwargs)
        with self.canvas:  # Changed from canvas.before to just canvas
            self.bg_color = Color(*bg_color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
    
    def _update_rect(self, *args):
        if hasattr(self, 'rect'):  # Check if rect exists
            self.rect.pos = self.pos
            self.rect.size = self.size 