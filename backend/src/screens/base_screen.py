from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Dark theme background
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.main_layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def add_title(self, text):
        """Add a title label in the app's style"""
        title = Label(
            text=text,
            font_size='24sp',
            color=(1, 1, 1, 1),  # White text
            size_hint_y=0.1,
            halign='left'
        )
        title.bind(size=title.setter('text_size'))  # Enable text wrapping
        self.main_layout.add_widget(title) 