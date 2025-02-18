from plyer import accelerometer
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

class StepTracker:
    def __init__(self):
        self.steps_data_file = Path('data/steps_data.json')
        self.steps_data_file.parent.mkdir(exist_ok=True)
        self.load_data()
        self.last_acceleration = None
        self.step_threshold = 10.0
        self.tracking_enabled = False
    
    def load_data(self):
        """Load stored step data"""
        if self.steps_data_file.exists():
            try:
                with open(self.steps_data_file, 'r') as f:
                    self.steps_data = json.load(f)
            except:
                self.steps_data = {}
        else:
            self.steps_data = {}
    
    def save_data(self):
        """Save step data to file"""
        try:
            with open(self.steps_data_file, 'w') as f:
                json.dump(self.steps_data, f)
        except Exception as e:
            print(f"Error saving step data: {e}")
    
    def start_tracking(self):
        """Start tracking steps"""
        try:
            accelerometer.enable()
            accelerometer.bind(on_acceleration=self._on_acceleration)
            self.tracking_enabled = True
        except:
            print("Warning: Step tracking not available on this device")
            self.tracking_enabled = False
    
    def stop_tracking(self):
        """Stop tracking steps"""
        if self.tracking_enabled:
            try:
                accelerometer.disable()
            except:
                print("Warning: Could not disable step tracking")
        self.tracking_enabled = False
    
    def _on_acceleration(self, acc, val):
        """Handle acceleration updates"""
        if not self.tracking_enabled:
            return
            
        x, y, z = val
        
        if self.last_acceleration:
            delta = abs(x - self.last_acceleration[0]) + \
                   abs(y - self.last_acceleration[1]) + \
                   abs(z - self.last_acceleration[2])
            
            if delta > self.step_threshold:
                self._count_step()
        
        self.last_acceleration = (x, y, z)
    
    def _count_step(self):
        """Count a step"""
        today = datetime.now().strftime('%Y-%m-%d')
        self.steps_data[today] = self.steps_data.get(today, 0) + 1
        self.save_data()
    
    def get_steps_for_date(self, date_str):
        """Get step count for a specific date"""
        return self.steps_data.get(date_str, 0)
    
    def get_steps_for_week(self, start_date):
        """Get step counts for a week starting from start_date"""
        week_data = []
        current_date = start_date
        for _ in range(7):
            date_str = current_date.strftime('%Y-%m-%d')
            week_data.append(self.steps_data.get(date_str, 0))
            current_date = current_date + timedelta(days=1)
        return week_data 