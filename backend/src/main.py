from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window

# Import screens
from screens.home_screen import HomeScreen
from screens.search_screen import SearchScreen
from screens.messages_screen import MessagesScreen
from screens.profile_screen import ProfileScreen
from screens.map_screen import MapScreen
from screens.explore_screen import ExploreScreen

class NavigationBar(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.1
        self.screen_manager = screen_manager
        
        # Create navigation buttons
        buttons = [
            ('🏠', 'Home'),
            ('🔍', 'Search'),
            ('💬', 'Messages'),
            ('👤', 'Profile')
        ]
        
        for icon, screen in buttons:
            # Create a separate function for each button to avoid closure issues
            def make_callback(screen_name):
                return lambda instance: setattr(self.screen_manager, 'current', screen_name)
            
            btn = Button(
                text=f"{icon}\n{screen}",
                on_press=make_callback(screen)
            )
            self.add_widget(btn)

class WalkQuestApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        
        sm = ScreenManager()
        
        # Add all screens
        sm.add_widget(HomeScreen(name='Home'))
        sm.add_widget(SearchScreen(name='Search'))
        sm.add_widget(MessagesScreen(name='Messages'))
        sm.add_widget(ProfileScreen(name='Profile'))
        sm.add_widget(MapScreen(name='Map'))
        sm.add_widget(ExploreScreen(name='Explore'))
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(sm)
        layout.add_widget(NavigationBar(sm))
        
        return layout

if __name__ == "__main__":
    WalkQuestApp().run()

    