from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from .base_screen import BaseScreen

class SearchScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.add_title('Explore')
        
        # Search bar
        search_box = BoxLayout(size_hint_y=0.1, spacing=5)
        search_input = TextInput(
            hint_text='Search for a destination',
            multiline=False,
            size_hint_x=0.8,
            background_color=(0.2, 0.2, 0.2, 1)
        )
        search_button = Button(
            text='🔍',
            size_hint_x=0.2,
            background_color=(1, 0.8, 0, 1)
        )
        search_box.add_widget(search_input)
        search_box.add_widget(search_button)
        self.main_layout.add_widget(search_box)
        
        # Filter buttons
        filters = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=5)
        filter_options = [
            'By distance from current location',
            'By popularity',
            'By exotic'
        ]
        for option in filter_options:
            btn = Button(
                text=option,
                background_color=(0.2, 0.2, 0.2, 1),
                color=(1, 1, 1, 1)
            )
            filters.add_widget(btn)
        self.main_layout.add_widget(filters) 