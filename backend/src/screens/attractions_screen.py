from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.carousel import Carousel
import json
from kivy.network.urlrequest import UrlRequest
import certifi

class AttractionCard(BoxLayout):
    def __init__(self, attraction_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [20, 20]
        self.spacing = 10

        # Image
        if 'IMAGE_PATH' in attraction_data['properties']:
            image_url = attraction_data['properties']['IMAGE_PATH']
            if image_url:
                self.image = AsyncImage(
                    source=image_url,
                    size_hint_y=0.6,
                    allow_stretch=True,
                    keep_ratio=True
                )
                self.add_widget(self.image)

        # Name
        name = attraction_data['properties'].get('PAGETITLE', 'Unknown Location')
        self.name_label = Label(
            text=name,
            size_hint_y=0.1,
            font_size='20sp',
            bold=True
        )
        self.add_widget(self.name_label)

        # Description
        description = attraction_data['properties'].get('OVERVIEW', '')
        self.desc_label = Label(
            text=description,
            size_hint_y=0.2,
            text_size=(self.width, None),
            halign='left',
            valign='top'
        )
        self.add_widget(self.desc_label)

        # Navigation button
        self.nav_button = Button(
            text='Go to this place',
            size_hint_y=0.1,
            background_color=(0.95, 0.75, 0.3, 1)  # Golden color
        )
        self.nav_button.bind(on_press=lambda x: self.show_route(attraction_data))
        self.add_widget(self.nav_button)

    def show_route(self, attraction_data):
        # Get coordinates from attraction data
        coords = attraction_data['geometry']['coordinates']
        dest_lat, dest_lon = coords[1], coords[0]
        
        # TODO: Get current location
        # For now using a default Singapore location
        current_lat, current_lon = 1.3521, 103.8198
        
        # Construct Google Maps URL
        maps_url = f"https://www.google.com/maps/dir/?api=1&origin={current_lat},{current_lon}&destination={dest_lat},{dest_lon}&travelmode=walking"
        
        # Open in web browser or native maps app
        import webbrowser
        webbrowser.open(maps_url)

class AttractionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_attractions()

    def load_attractions(self):
        # Create main layout
        layout = BoxLayout(orientation='vertical')
        
        # Create carousel for swiping through attractions
        carousel = Carousel(direction='right')
        
        # Load attractions data
        with open('backend/src/data/TouristAttractions.geojson', 'r') as f:
            data = json.load(f)
            
        # Create a card for each attraction
        for feature in data['features']:
            card = AttractionCard(feature)
            carousel.add_widget(card)
            
        layout.add_widget(carousel)
        self.add_widget(layout) 