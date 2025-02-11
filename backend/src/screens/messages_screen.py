from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from .base_screen import BaseScreen
from widgets.placeholders import ColorBoxLayout

class MessageBubble(ColorBoxLayout):
    def __init__(self, text, is_sent=False, **kwargs):
        # Gold for sent messages, white for received
        bg_color = (1, 0.8, 0, 1) if is_sent else (1, 1, 1, 1)
        super().__init__(bg_color=bg_color, **kwargs)
        
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 40
        self.padding = [10, 5]
        
        # Add spacing for alignment
        if is_sent:
            self.add_widget(BoxLayout(size_hint_x=0.2))
        
        # Message content
        msg = Label(
            text=text,
            color=(0, 0, 0, 1),  # Black text
            size_hint_x=0.8,
            halign='left' if not is_sent else 'right'
        )
        self.add_widget(msg)
        
        # Add spacing for alignment
        if not is_sent:
            self.add_widget(BoxLayout(size_hint_x=0.2))

class MessagesScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Chat messages area
        self.scroll = ScrollView(size_hint_y=0.8)
        self.messages_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=5,
            padding=[10, 10]
        )
        self.messages_box.bind(minimum_height=self.messages_box.setter('height'))
        
        # Sample messages
        initial_messages = [
            (False, 'Hey are you free to meet up?'),
        ]
        
        for is_sent, text in initial_messages:
            self.add_message(text, is_sent)
        
        self.scroll.add_widget(self.messages_box)
        self.main_layout.add_widget(self.scroll)
        
        # Message input area
        input_area = BoxLayout(size_hint_y=0.1, spacing=5, padding=[5, 5])
        self.text_input = TextInput(
            hint_text='Type here...',
            multiline=False,
            size_hint_x=0.8,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            on_text_validate=self.send_message  # Allow Enter key to send
        )
        send_button = Button(
            text='Send',
            size_hint_x=0.2,
            background_color=(1, 0.8, 0, 1),
            on_press=self.send_message
        )
        input_area.add_widget(self.text_input)
        input_area.add_widget(send_button)
        self.main_layout.add_widget(input_area)
    
    def add_message(self, text, is_sent=True):
        """Add a new message bubble to the chat"""
        if text.strip():  # Only add non-empty messages
            msg_bubble = MessageBubble(text=text, is_sent=is_sent)
            self.messages_box.add_widget(msg_bubble)
            # Scroll to the bottom to show new message
            self.scroll.scroll_y = 0
    
    def send_message(self, *args):
        """Handle sending a new message"""
        text = self.text_input.text.strip()
        if text:
            self.add_message(text, is_sent=True)
            self.text_input.text = ''  # Clear input after sending 