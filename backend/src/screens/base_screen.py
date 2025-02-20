from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore
import webbrowser

class BaseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Dark theme background
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.main_layout)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def add_title(self, text):
        """Add a title label in the app's style"""
        title = Label(
            text=text,
            font_size='24sp',
            color=(1, 1, 1, 1),  # White text
            size_hint_y=0.1,
            halign='left'
        )
        title.bind(size=title.setter('text_size'))  # Enable text wrapping
        self.main_layout.add_widget(title)

class BaseScreenWithEmergency(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('emergency_contacts.json')
        
        # Main container
        self.main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Emergency button at the top
        emergency_button = Button(
            text='EMERGENCY',
            size_hint_y=0.1,
            background_color=(1, 0, 0, 1),  # Red color
            color=(1, 1, 1, 1),  # White text
            bold=True,
            font_size='20sp',
            on_press=self.trigger_emergency
        )
        self.main_layout.add_widget(emergency_button)
        
        # Content area for child screens
        self.content_layout = BoxLayout(orientation='vertical', spacing=10)
        self.main_layout.add_widget(self.content_layout)
        
        self.add_widget(self.main_layout)

    def get_emergency_contact(self):
        try:
            return self.store.get('emergency')['number']
        except:
            return '999'  # Default fallback number

    def trigger_emergency(self, instance):
        """Handle emergency button press based on platform"""
        emergency_number = self.get_emergency_contact()
        
        if platform == 'android':
            self.trigger_emergency_android(emergency_number)
        else:
            webbrowser.open(f'tel:{emergency_number}')
            print("Emergency feature is limited on desktop. Please use a phone to call emergency services.")

    def trigger_emergency_android(self, emergency_number):
        try:
            from jnius import autoclass, cast
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            
            Intent = autoclass('android.content.Intent')
            intent = Intent(Intent.ACTION_DIAL)
            intent.setData(autoclass('android.net.Uri').parse(f'tel:{emergency_number}'))
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            
            activity.startActivity(intent)

        except Exception as e:
            print(f"Error triggering emergency: {str(e)}")
            webbrowser.open(f'tel:{emergency_number}') 