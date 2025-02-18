from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from datetime import datetime, timedelta
from .base_screen import BaseScreen
import matplotlib.pyplot as plt
import numpy as np
import io
from kivy.core.image import Image as CoreImage
from services.step_tracker import StepTracker

class HealthScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.step_tracker = StepTracker()
        self.current_date = datetime.now()
        
        try:
            self.step_tracker.start_tracking()
        except:
            print("Warning: Step tracking not available on this device")
        
        # Main container with padding
        self.container = BoxLayout(orientation='vertical', padding=[20, 20], spacing=15)
        
        # Header with title and date
        header = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        title = Label(
            text='Activities',
            font_size='24sp',
            size_hint_x=0.7,
            halign='left'
        )
        
        # Navigation arrows and date
        nav_box = BoxLayout(orientation='horizontal', size_hint_x=0.3)
        left_arrow = Button(
            text='<',
            size_hint_x=0.3,
            on_press=self.previous_week
        )
        right_arrow = Button(
            text='>',
            size_hint_x=0.3,
            on_press=self.next_week
        )
        
        nav_box.add_widget(left_arrow)
        nav_box.add_widget(right_arrow)
        
        header.add_widget(title)
        header.add_widget(nav_box)
        
        # Stats container
        stats_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.15,
            spacing=10,
            padding=[0, 10]
        )
        
        # Steps
        steps_box = BoxLayout(orientation='vertical')
        self.steps_value = Label(
            text='0',
            font_size='24sp',
            color=(0, 0.7, 1, 1)
        )
        steps_label = Label(
            text='Steps',
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        steps_box.add_widget(self.steps_value)
        steps_box.add_widget(steps_label)
        
        stats_container.add_widget(steps_box)
        
        # Add all to main container
        self.container.add_widget(header)
        self.container.add_widget(stats_container)
        
        # Create and add graph
        self.update_graph()
        
        self.add_widget(self.container)
        
        # Update initial values
        self.update_display()
    
    def update_display(self):
        """Update all display elements with current data"""
        # Update step count
        today_str = self.current_date.strftime('%Y-%m-%d')
        steps = self.step_tracker.get_steps_for_date(today_str)
        self.steps_value.text = str(steps)
        
        # Update graph
        self.update_graph()
    
    def previous_week(self, instance):
        """Handle previous week button press"""
        self.current_date -= timedelta(days=7)
        self.update_display()
    
    def next_week(self, instance):
        """Handle next week button press"""
        self.current_date += timedelta(days=7)
        self.update_display()
    
    def update_graph(self):
        """Update the activity graph with current week's data"""
        # Get start of week (Monday)
        start_of_week = self.current_date - timedelta(days=self.current_date.weekday())
        
        # Get step data for the week
        week_data = self.step_tracker.get_steps_for_week(start_of_week)
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        # Create and update graph
        graph_image = self.create_activity_graph(days, week_data)
        # Add graph to the layout if it exists
        if hasattr(self, 'graph_image'):
            self.container.remove_widget(self.graph_image)
        self.graph_image = graph_image
        self.container.add_widget(self.graph_image)
    
    def create_activity_graph(self, days, steps):
        # Create figure with dark background
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#1a1a1a')
        
        # Create bar chart
        bars = ax.bar(days, steps, color='#4CAF50', alpha=0.7)
        
        # Customize the plot
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#333333')
        ax.spines['bottom'].set_color('#333333')
        ax.tick_params(colors='white')
        ax.grid(True, axis='y', color='#333333', linestyle='-', alpha=0.2)
        
        # Set y-axis limits
        ax.set_ylim(0, 10000)
        
        # Remove axis labels
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        # Tight layout
        plt.tight_layout()
        
        # Convert plot to Kivy Image
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', 
                   facecolor='#1a1a1a', edgecolor='none')
        buf.seek(0)
        img_buf = CoreImage(buf, ext='png')
        
        # Clear the current figure
        plt.close()
        
        # Create and return the Kivy Image widget
        return Image(texture=img_buf.texture, size_hint_y=0.4) 