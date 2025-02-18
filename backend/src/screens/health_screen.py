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
from kivy.graphics import Color, RoundedRectangle

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
        self.date_label = Label(
            text=self.get_date_range(),
            size_hint_x=0.4
        )
        right_arrow = Button(
            text='>',
            size_hint_x=0.3,
            on_press=self.next_week
        )
        
        nav_box.add_widget(left_arrow)
        nav_box.add_widget(self.date_label)
        nav_box.add_widget(right_arrow)
        
        header.add_widget(title)
        header.add_widget(nav_box)
        
        # Stats container with dark background and rounded corners
        stats_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.2,
            spacing=10,
            padding=[20, 10]
        )
        
        # Create a background box
        stats_box = BoxLayout(
            orientation='vertical',
            padding=[15, 10],
            spacing=5
        )
        stats_box.canvas.before.add(Color(0.12, 0.12, 0.12, 1))  # Dark gray
        stats_box.canvas.before.add(RoundedRectangle(pos=stats_box.pos, size=stats_box.size, radius=[10,]))
        
        # Today label
        today_label = Label(
            text='TODAY',
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=0.3,
            halign='left'
        )
        today_label.bind(size=today_label.setter('text_size'))
        
        # Stats row
        stats_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.7)
        
        # Steps column
        steps_column = BoxLayout(orientation='horizontal', spacing=5)
        self.steps_value = Label(
            text='0',
            font_size='24sp',
            color=(1, 1, 1, 1)
        )
        steps_unit = Label(
            text='steps in',
            font_size='16sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        steps_column.add_widget(self.steps_value)
        steps_column.add_widget(steps_unit)
        
        # Time/calories column
        time_cal_column = BoxLayout(orientation='horizontal', spacing=5)
        self.time_value = Label(
            text='0',
            font_size='24sp',
            color=(1, 1, 1, 1)
        )
        time_unit = Label(
            text='minutes',
            font_size='16sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        time_cal_column.add_widget(self.time_value)
        time_cal_column.add_widget(time_unit)
        
        # Calories row
        calories_row = BoxLayout(orientation='horizontal', spacing=5)
        self.calories_value = Label(
            text='0',
            font_size='24sp',
            color=(1, 1, 1, 1)
        )
        calories_unit = Label(
            text='calories',
            font_size='16sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        calories_row.add_widget(self.calories_value)
        calories_row.add_widget(calories_unit)
        
        # Add everything to stats box
        stats_box.add_widget(today_label)
        stats_row.add_widget(steps_column)
        stats_row.add_widget(time_cal_column)
        stats_box.add_widget(stats_row)
        stats_box.add_widget(calories_row)
        
        # Add stats box to container
        stats_container.add_widget(stats_box)
        
        # Add all to main container
        self.container.add_widget(header)
        self.container.add_widget(stats_container)
        
        # Create and add graph
        self.update_graph()
        
        self.add_widget(self.container)
        
        # Update initial values
        self.update_display()
    
    def get_date_range(self):
        """Get the date range string for current week"""
        start = self.current_date - timedelta(days=self.current_date.weekday())
        end = start + timedelta(days=6)
        return f"{start.strftime('%d/%m')} - {end.strftime('%d/%m')}"
    
    def update_display(self):
        """Update all display elements with current data"""
        # Update date label
        self.date_label.text = self.get_date_range()
        
        # Update step count for today
        today_str = self.current_date.strftime('%Y-%m-%d')
        steps = self.step_tracker.get_steps_for_date(today_str)
        self.steps_value.text = str(steps)
        
        # Calculate and update calories (rough estimate: 0.04 calories per step)
        calories = int(steps * 0.04)
        self.calories_value.text = str(calories)
        
        # Calculate and update time (rough estimate: 1 minute per 100 steps)
        minutes = int(steps / 100)
        self.time_value.text = str(minutes)
        
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
        # Clear any existing plots
        plt.clf()
        
        # Create figure with dark background
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#1a1a1a')
        
        # Create bar chart
        bars = ax.bar(days, steps, color='#4CAF50', alpha=0.7)
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', color='white')
        
        # Customize the plot
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#333333')
        ax.spines['bottom'].set_color('#333333')
        ax.tick_params(colors='white')
        ax.grid(True, axis='y', color='#333333', linestyle='-', alpha=0.2)
        
        # Set y-axis limits based on data
        max_steps = max(steps) if steps else 1000
        ax.set_ylim(0, max_steps * 1.2)  # Add 20% padding
        
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
        plt.close('all')
        
        # Create and return the Kivy Image widget
        return Image(texture=img_buf.texture, size_hint_y=0.4) 