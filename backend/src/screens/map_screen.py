from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from widgets.placeholders import ColorBoxLayout
from .base_screen import BaseScreen

class MapScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        container = FloatLayout()
        
        # Map background
        map_box = ColorBoxLayout(
            bg_color=(0.15, 0.15, 0.15, 1),
            size_hint=(1, 1)
        )
        
        # Route info overlay
        info_overlay = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.15),
            pos_hint={'bottom': 0},
            padding=[20, 10]
        )
        
        location = Label(
            text='Pandan Reserver',
            color=(1, 0.8, 0, 1),
            font_size='20sp',
            halign='left'
        )
        
        details = Label(
            text='Distance: 2300m\nTime estimated: 32 minutes',
            color=(1, 0.8, 0, 1),
            halign='left',
            font_size='14sp'
        )
        
        info_overlay.add_widget(location)
        info_overlay.add_widget(details)
        
        container.add_widget(map_box)
        container.add_widget(info_overlay)
        self.add_widget(container) 