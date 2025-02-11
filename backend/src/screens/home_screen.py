from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10)
        label = Label(
            text='This is the Home page',
            font_size='24sp',  # Make text bigger
            color=(0, 0, 0, 1)  # Black color
        )
        layout.add_widget(label)
        self.add_widget(layout) 