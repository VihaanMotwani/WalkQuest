from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.garden.graph import Graph, MeshLinePlot
from .base_screen import BaseScreen

class HealthScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.add_title('Activities')
        
        # Today's stats
        stats_grid = GridLayout(cols=2, size_hint_y=0.2)
        stats = [
            ('9200', 'steps in'),
            ('35', 'minutes'),
            ('420', 'calories')
        ]
        for value, label in stats:
            stats_grid.add_widget(Label(
                text=value,
                font_size='24sp',
                color=(1, 1, 1, 1)
            ))
            stats_grid.add_widget(Label(
                text=label,
                color=(0.8, 0.8, 0.8, 1)
            ))
        self.main_layout.add_widget(stats_grid)
        
        # Activity graph placeholder
        graph = Graph(
            xlabel='Day',
            ylabel='Steps',
            x_ticks_minor=1,
            x_ticks_major=5,
            y_ticks_major=2000,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            x_grid=True,
            y_grid=True,
            xmin=0,
            xmax=7,
            ymin=0,
            ymax=10000,
            size_hint_y=0.5
        )
        self.main_layout.add_widget(graph) 