from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

# Import screens
from screens.home_screen import HomeScreen
from screens.search_screen import SearchScreen
from screens.messages_screen import MessagesScreen
from screens.profile_screen import ProfileScreen
from screens.map_screen import MapScreen
from screens.explore_screen import ExploreScreen
from screens.route_screen import RouteScreen
from screens.health_screen import HealthScreen
from screens.attractions_screen import AttractionsScreen

class NavigationBar(BoxLayout):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = 0.1
        self.screen_manager = screen_manager
        
        # Dark theme background
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Navigation buttons matching mockup
        buttons = [
            ('Home', 'Home'),      # Start walk screen
            ('Search', 'Search'),    # Explore screen
            ('Chat', 'Messages'),  # Messages screen
            ('Account', 'Profile')    # Account screen
        ]
        
        for text, screen in buttons:
            btn = Button(
                text=text,
                background_color=(0, 0, 0, 0),  # Transparent background
                color=(1, 1, 1, 1),  # White text
                on_press=self._make_callback(screen)
            )
            self.add_widget(btn)
    
    def _make_callback(self, screen_name):
        return lambda instance: setattr(self.screen_manager, 'current', screen_name)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class WalkQuestApp(App):
    def build(self):
        # Set dark theme
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background
        
        sm = ScreenManager()
        
        # Add screens matching mockup flow
        sm.add_widget(HomeScreen(name='Home'))       # Start walk screen
        sm.add_widget(SearchScreen(name='Search'))   # Explore screen
        sm.add_widget(MessagesScreen(name='Messages'))
        sm.add_widget(ProfileScreen(name='Profile')) # Account screen
        sm.add_widget(HealthScreen(name='Health'))  # Add HealthScreen
        sm.add_widget(AttractionsScreen(name='attractions'))
        
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(sm)
        layout.add_widget(NavigationBar(sm))
        
        return layout

if __name__ == "__main__":
    WalkQuestApp().run()

    