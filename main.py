from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class MyApp(App):
    def build(self):
        layout = BoxLayout()
        btn = Button(text="Hello, Android!")
        layout.add_widget(btn)
        return layout

if __name__ == "__main__":
    MyApp().run()

    