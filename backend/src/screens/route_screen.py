from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from services.route_service import RouteService

class RouteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.route_service = RouteService()
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Create Your Route',
            font_size='24sp',
            size_hint_y=0.1
        )
        main_layout.add_widget(title)
        
        # Preferences section
        pref_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.6)
        
        # Route type selector
        pref_layout.add_widget(Label(text='Route Type:'))
        self.route_type = Spinner(
            text='Nature',
            values=('Nature', 'Urban', 'Quick', 'Quiet'),
            size_hint=(None, None),
            size=(150, 44)
        )
        pref_layout.add_widget(self.route_type)
        
        # Distance selector
        pref_layout.add_widget(Label(text='Distance (km):'))
        self.distance_slider = Slider(
            min=1,
            max=10,
            value=5,
            step=0.5
        )
        pref_layout.add_widget(self.distance_slider)
        
        main_layout.add_widget(pref_layout)
        
        # Generate button
        generate_btn = Button(
            text='Generate Route',
            size_hint_y=0.15,
            background_color=(0.2, 0.8, 0.2, 1),
            on_press=self.generate_route
        )
        main_layout.add_widget(generate_btn)
        
        # Results section
        self.results_layout = BoxLayout(orientation='vertical', size_hint_y=0.3)
        self.results_label = Label(text='')
        self.results_layout.add_widget(self.results_label)
        main_layout.add_widget(self.results_layout)
        
        self.add_widget(main_layout)
    
    def generate_route(self, instance):
        preferences = {
            'type': self.route_type.text.lower(),
            'distance': self.distance_slider.value
        }
        
        # Get user location (for now using default Singapore coordinates)
        start_point = (1.3521, 103.8198)
        
        try:
            route = self.route_service.generate_route(
                start_point,
                preferences,
                desired_length=self.distance_slider.value
            )
            
            # Display route summary
            summary = (
                f"Route Generated!\n"
                f"Type: {route.route_type.title()}\n"
                f"Distance: {route.distance:.1f} km\n"
                f"Duration: {route.duration} minutes\n"
                f"Difficulty: {route.difficulty.title()}\n"
                f"Points of Interest: {len(route.points)-1}"
            )
            self.results_label.text = summary
            
        except Exception as e:
            self.results_label.text = f"Error generating route: {str(e)}" 