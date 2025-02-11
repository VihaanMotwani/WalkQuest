from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from widgets.placeholders import ColorBoxLayout
from .base_screen import BaseScreen

class ProfileScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main container
        container = FloatLayout()
        
        # Profile section at top left
        profile_section = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.15,
            pos_hint={'top': 1},  # Position at top
            padding=[20, 10],
            spacing=15
        )
        
        # Profile image and info
        profile_info = BoxLayout(
            orientation='horizontal',
            size_hint_x=0.6,
            spacing=10
        )
        
        # Profile image
        image_container = ColorBoxLayout(
            bg_color=(0.5, 0.5, 0.5, 1),
            size_hint=(None, None),
            size=('60dp', '60dp')
        )
        
        # Name and title container
        text_container = BoxLayout(
            orientation='vertical',
            spacing=2,
            size_hint_x=0.7
        )
        
        name = Label(
            text='Kelly Wong',
            font_size='18sp',
            color=(1, 1, 1, 1),
            halign='left',
            valign='bottom',
            text_size=(None, None)
        )
        
        title = Label(
            text='Product manager, bank\nJurong East, Cityhall',
            color=(0.8, 0.8, 0.8, 1),
            font_size='14sp',
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        
        text_container.add_widget(name)
        text_container.add_widget(title)
        
        profile_info.add_widget(image_container)
        profile_info.add_widget(text_container)
        
        profile_section.add_widget(profile_info)
        profile_section.add_widget(BoxLayout())  # Spacer
        
        # Menu options
        menu = BoxLayout(
            orientation='vertical',
            size_hint_y=0.75,
            pos_hint={'top': 0.8},  # Position below profile
            padding=[20, 10],
            spacing=10
        )
        
        options = [
            'Personal',
            'History',
            'Friends',
            'Groups',
            'Health'
        ]
        
        for option in options:
            btn = Button(
                text=option,
                background_color=(0.2, 0.2, 0.2, 1),
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height='50dp',
                halign='left'
            )
            menu.add_widget(btn)
        
        # Add everything to the container
        container.add_widget(menu)
        container.add_widget(profile_section)  # Add profile section last to be on top
        
        self.add_widget(container) 