from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from widgets.placeholders import ColorBoxLayout
from .base_screen import BaseScreenWithEmergency
from screens.health_screen import HealthScreen
from kivy.uix.textinput import TextInput
from kivy.storage.jsonstore import JsonStore

class ProfileScreen(BaseScreenWithEmergency):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore('emergency_contacts.json')
        
        # Main container
        container = FloatLayout()
        
        # Profile section at top left
        profile_section = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.15,
            pos_hint={'top': 1},  # Position at top
            padding=[20, 10],
            spacing=15
        )
        
        # Profile image and info
        profile_info = BoxLayout(
            orientation='horizontal',
            size_hint_x=0.6,
            spacing=10
        )
        
        # Profile image
        image_container = ColorBoxLayout(
            bg_color=(0.5, 0.5, 0.5, 1),
            size_hint=(None, None),
            size=('60dp', '60dp')
        )
        
        # Name and title container
        text_container = BoxLayout(
            orientation='vertical',
            spacing=2,
            size_hint_x=0.7
        )
        
        name = Label(
            text='Kelly Wong',
            font_size='18sp',
            color=(1, 1, 1, 1),
            halign='left',
            valign='bottom',
            text_size=(None, None)
        )
        
        title = Label(
            text='Product manager, bank\nJurong East, Cityhall',
            color=(0.8, 0.8, 0.8, 1),
            font_size='14sp',
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        
        text_container.add_widget(name)
        text_container.add_widget(title)
        
        profile_info.add_widget(image_container)
        profile_info.add_widget(text_container)
        
        profile_section.add_widget(profile_info)
        profile_section.add_widget(BoxLayout())  # Spacer
        
        # Emergency Contacts Section
        emergency_section = BoxLayout(
            orientation='vertical',
            size_hint_y=0.3,
            padding=[20, 10],
            spacing=10
        )
        
        emergency_title = Label(
            text='Emergency Contacts',
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height='40dp'
        )
        
        # Contact input
        contact_input = BoxLayout(orientation='horizontal', spacing=10)
        self.contact_number = TextInput(
            multiline=False,
            hint_text='Enter emergency contact number',
            text=self.load_emergency_contact(),
            size_hint_x=0.7
        )
        save_button = Button(
            text='Save',
            size_hint_x=0.3,
            on_press=self.save_emergency_contact
        )
        
        contact_input.add_widget(self.contact_number)
        contact_input.add_widget(save_button)
        
        emergency_section.add_widget(emergency_title)
        emergency_section.add_widget(contact_input)
        
        # Add to content layout
        self.content_layout.add_widget(profile_section)
        self.content_layout.add_widget(emergency_section)
        
        # Menu options
        menu = BoxLayout(
            orientation='vertical',
            size_hint_y=0.55,
            padding=[20, 10],
            spacing=10
        )
        
        options = [
            'Personal',
            'History',
            'Friends',
            'Groups',
            'Health'
        ]
        
        for option in options:
            btn = Button(
                text=option,
                background_color=(0.2, 0.2, 0.2, 1),
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height='50dp',
                halign='left',
                on_press=self.handle_menu_option
            )
            menu.add_widget(btn)
        
        self.content_layout.add_widget(menu)

    def load_emergency_contact(self):
        try:
            return self.store.get('emergency')['number']
        except:
            return ''

    def save_emergency_contact(self, instance):
        self.store.put('emergency', number=self.contact_number.text)

    def handle_menu_option(self, instance):
        if instance.text == 'Health':
            self.manager.add_widget(HealthScreen(name='Health'))
            self.manager.current = 'Health' 