from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage, Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from plyer import gps
import json
import re
import html

# Dictionary mapping attraction names to specific image filenames
ATTRACTION_IMAGE_FILES = {
    "National Gallery Singapore": "national_gallery_singapore.jpg",
    "Sultan Mosque (Masjid Sultan) Singapore": "sultan_mosque.jpg",
    "Sri Mariamman Temple: Hindu Temple in Singapore": "sri_mariamman_temple.jpg",
    "Armenian Church in Singapore": "armenian_church.jpg",
    "CHIJMES Singapore": "chijmes_singapore.jpg",
    "St Andrews Cathedral- Singapore Architecture Landmark": "st_andrews_cathedral.jpg",
    "Kreta Ayer Square": "kreta_ayer_square.jpg",
    "Albert Mall Trishaw Park ": "albert_hall_trishaw_park.jpg",
    "Chinatown Food Street ": "chinatown_food_street.jpg",
    "Chinatown Heritage Centre, Singapore": "chinatown_heritage_centre_singapore.jpg"
}

# Marina Bay Sands coordinates
STARTING_LOCATION = (1.2847, 103.8610)  # Marina Bay Sands coordinates

class AttractionTile(BoxLayout):
    def __init__(self, attraction_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 400
        self.padding = [10, 10]
        self.spacing = 5

        # Card background
        with self.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Extract the name from the Description field
        properties = attraction_data['properties']
        raw_description = properties.get('Description', '')
        name = self.extract_pagtitle(raw_description)

        # Clean the name
        name = self.clean_text(name)

        # Name label
        self.name_label = Label(
            text=name,
            size_hint_y=0.15,
            font_size='18sp',
            bold=True,
            halign='left',
            valign='middle',
            text_size=(self.width, None)  # Allow text to wrap
        )
        self.name_label.bind(size=self.name_label.setter('text_size'))
        self.add_widget(self.name_label)

        # Extract and clean description from HTML
        description = self.extract_description(raw_description)

        # Clean the description
        description = self.clean_text(description)

        self.desc_label = Label(
            text=description,
            size_hint_y=0.25,
            font_size='14sp',
            halign='left',
            valign='top'
        )
        self.desc_label.bind(size=self.desc_label.setter('text_size'))
        self.add_widget(self.desc_label)

        # Load image from local directory using the mapping
        image_filename = ATTRACTION_IMAGE_FILES.get(name, None)
        if image_filename:
            image_path = f'backend/src/screens/images/{image_filename}'
            print(f"Loading image for {name}: {image_path}")  # Debugging output
            self.image = Image(
                source=image_path,
                size_hint_y=0.6,
                allow_stretch=True,
                keep_ratio=True
            )
            self.add_widget(self.image)
        else:
            print(f"No image found for {name}")

        # Navigation button
        self.nav_button = Button(
            text='Go to this place',
            size_hint_y=0.1,
            background_color=(0.95, 0.75, 0.3, 1)
        )
        self.nav_button.bind(on_press=lambda x: self.show_route(attraction_data))
        self.add_widget(self.nav_button)

    def extract_pagtitle(self, raw_html):
        # Use regex to extract the PAGETITLE text from HTML
        match = re.search(r'<th>PAGETITLE<\/th> <td>([^<]+)<\/td>', raw_html)
        if match:
            return match.group(1)
        return "Unnamed Location"

    def extract_description(self, raw_html):
        # Use regex to extract the description text from HTML
        match = re.search(r'<th>OVERVIEW<\/th> <td>([^<]+)<\/td>', raw_html)
        if match:
            return match.group(1)
        return "No description available"

    def clean_text(self, text):
        # Remove unwanted characters and apostrophes
        return text.replace("'", "").replace("â", "").replace("€", "").replace("™", "")

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def show_route(self, attraction_data):
        coords = attraction_data['geometry']['coordinates']
        dest_lat, dest_lon = coords[1], coords[0]
        
        # Use Marina Bay Sands as starting point
        current_lat, current_lon = STARTING_LOCATION
        
        maps_url = f"https://www.google.com/maps/dir/?api=1&origin={current_lat},{current_lon}&destination={dest_lat},{dest_lon}&travelmode=walking"
        import webbrowser
        webbrowser.open(maps_url)

    def on_location(self, **kwargs):
        # Called when GPS location is received
        self.current_lat = kwargs['lat']
        self.current_lon = kwargs['lon']
        gps.stop()

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_attractions()

    def load_attractions(self):
        try:
            # Main container
            main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

            # Header
            header = Label(
                text='Discover Singapore',
                size_hint_y=0.1,
                font_size='24sp',
                bold=True
            )
            main_layout.add_widget(header)

            # Scrollable grid for attractions
            scroll = ScrollView(size_hint=(1, 0.9))
            grid = GridLayout(
                cols=1,
                spacing=15,
                size_hint_y=None,
                padding=[10, 10]
            )
            # Important: This makes the grid scrollable
            grid.bind(minimum_height=grid.setter('height'))

            # Load and display attractions
            with open('backend/src/data/TouristAttractions.geojson', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Create a card for each attraction
                for feature in data['features'][:10]:  # Limit to first 10 for now
                    tile = AttractionTile(feature)
                    grid.add_widget(tile)

            scroll.add_widget(grid)
            main_layout.add_widget(scroll)
            self.add_widget(main_layout)

        except Exception as e:
            # Add error display
            error_layout = BoxLayout(orientation='vertical', padding=20)
            error_label = Label(
                text=f"Error loading attractions: {str(e)}",
                color=(1, 0, 0, 1)  # Red text
            )
            error_layout.add_widget(error_label)
            self.add_widget(error_layout)
            print(f"Error: {str(e)}")  # Print to console for debugging 