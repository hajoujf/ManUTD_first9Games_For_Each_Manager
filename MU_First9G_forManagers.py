import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import pandas as pd

# Custom Radar Chart Function
def radar_factory(num_vars, frame='polygon'):
    """Create a radar chart with `num_vars` axes."""
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):
        name = 'radar'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')

        def plot(self, *args, **kwargs):
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels, fontsize=12, color='black')

        def _gen_axes_patch(self):
            if frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars, radius=.5, edgecolor="black")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def draw(self, renderer):
            super().draw(renderer)

        def _gen_axes_spines(self):
            if frame == 'polygon':
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5) + self.transAxes)
                spine.set_edgecolor('black')  # Set edge color of the frame to black

                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

# Categories for the radar chart
categories = ['On Target (%)', 'Off Target (%)', 'Conversion Rate (%)']

# Data1 Table
data1 = {
    'Moyes': [53.98, 46.02, 12.39],
    'Ten Hag': [38.02, 61.98, 13.22],
    'OGS': [31.21, 68.79, 7.80],
    'Jose': [34.13, 65.87, 13.49],
    'LVG': [45.10, 54.90, 15.69],
    'Ruben Amorim': [34.56, 65.44, 12.50]
}

# Create a pandas DataFrame for tabular format
data_table = pd.DataFrame.from_dict(data1, orient='index', columns=categories)
print("Manager Performance Data (in %):")
print(data_table)

# Create the radar chart
num_vars = len(categories)
theta = radar_factory(num_vars, frame='polygon')

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='radar'))
fig.subplots_adjust(top=0.85, bottom=0.05)

# Light background color for the figure and axes
fig.patch.set_facecolor('#F0F0F0')
ax.set_facecolor('#F0F0F0')

# Line colors (dark for light mode)
colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A1', '#F4D03F', '#8E44AD']

for idx, (manager, values) in enumerate(data1.items()):
    ax.plot(theta, values, linewidth=2, linestyle='-', label=manager, color=colors[idx % len(colors)])

# Labels and grid settings
ax.set_varlabels(categories)
ax.set_rgrids([0, 20, 40, 60, 80], 
             labels=['0%', '20%', '40%', '60%', '80%'], 
             angle=0, fontsize=9, color='black', alpha=0.7)
ax.set_ylim(0, 80)

# Title and legend
fig.suptitle('Manager Performance Comparison', fontsize=16, fontweight='bold', color='black')
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), facecolor='#F0F0F0', edgecolor='black', labelcolor='black',  labels=[f"{manager}" for manager in data1.keys()])

# Add performance data in a box centered below the plot
performance_lines = [
    (colors[0], "Moyes - On Target: 53.98, Off Target: 46.02, Conversion Rate: 12.39"),
    (colors[1], "Ten Hag - On Target: 38.02, Off Target: 61.98, Conversion Rate: 13.22"),
    (colors[2], "OGS - On Target: 31.21, Off Target: 68.79, Conversion Rate: 7.80"),
    (colors[3], "Jose - On Target: 34.13, Off Target: 65.87, Conversion Rate: 13.49"),
    (colors[4], "LVG - On Target: 45.10, Off Target: 54.90, Conversion Rate: 15.69"),
    (colors[5], "Ruben Amorim - On Target: 34.56, Off Target: 65.44, Conversion Rate: 12.50")
]

# Starting position for the text box
text_y_position = 0.05  # Y-coordinate for the first line
line_spacing = 0.03  # Spacing between lines

# Add a bounding box with a lighter background color
box_height = len(performance_lines) * line_spacing + 0.02  # Calculate box height
plt.figtext(0.5, text_y_position + box_height / 2 - 0.02, "",
            fontsize=10, ha='center', va='bottom',
            bbox=dict(facecolor='#FFFFFF', alpha=0.8, edgecolor='black'))

# Render each line of text with the appropriate colors (no longer white for all)
for color, text in performance_lines:
    plt.figtext(0.5, text_y_position, text, fontsize=10, ha='center', va='bottom', color=color)  # Use the line color here
    text_y_position += line_spacing

plt.show()
