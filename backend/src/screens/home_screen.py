from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from .base_screen import BaseScreen
from widgets.placeholders import ColorBoxLayout

class HomeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Main container
        container = FloatLayout()
        
        # Location image (green placeholder for now)
        image_box = ColorBoxLayout(
            bg_color=(0.2, 0.5, 0.3, 1),
            size_hint=(1, 0.7),
            pos_hint={'top': 1}
        )
        
        # Location info overlay
        info_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.3),
            pos_hint={'bottom': 0},
            padding=[20, 20],
            spacing=10
        )
        
        location_name = Label(
            text='Ubin Island',
            font_size='24sp',
            color=(1, 1, 1, 1),
            halign='left',
            size_hint_y=None,
            height='30dp'
        )
        
        description = Label(
            text='A granite nature supported a few thousand settlers. Much of the original vegetation was cleared for the cultivation of rubber and crops like pineapple...',
            color=(0.8, 0.8, 0.8, 1),
            text_size=(None, None),
            halign='left',
            valign='top',
            size_hint_y=None,
            height='60dp'
        )
        
        go_button = Button(
            text='Go to this place',
            size_hint_y=None,
            height='50dp',
            background_color=(1, 0.8, 0, 1),
            color=(0, 0, 0, 1)
        )
        
        info_box.add_widget(location_name)
        info_box.add_widget(description)
        info_box.add_widget(go_button)
        
        container.add_widget(image_box)
        container.add_widget(info_box)
        self.add_widget(container) 