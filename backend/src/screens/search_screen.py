from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        label = Label(
            text='This is the Search page',
            font_size='24sp',
            color=(0, 0, 0, 1)
        )
        layout.add_widget(label)
        self.add_widget(layout) 