from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

class MyApp(App):
    def build(self):
        # Set background color to white
        Window.clearcolor = (1, 1, 1, 1)
        
        layout = BoxLayout(padding=10)
        btn = Button(
            text="Heo, Android!",
            size_hint=(1, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_color=(0.2, 0.6, 1, 1)  # Light blue color
        )
        layout.add_widget(btn)
        return layout

if __name__ == "__main__":
    MyApp().run()

    