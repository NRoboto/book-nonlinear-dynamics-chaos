from typing import Literal, Text, Tuple
from matplotlib.patches import Wedge, Circle
from matplotlib.pyplot import axes
import matplotlib.pyplot as plt

def draw_circle(center: Tuple[float, float], radius: float, angle: float = 0.0, ax: axes = None, type: Literal['full', 'empty', 'none', 'left', 'right', 'bottom', 'top'] = 'full', colors: Tuple[Text, Text] = ['purple', 'white'], **kwargs):
  assert radius > 0, "Radius must be positive"
  
  if ax is None:
    ax = plt.gca()

  face_color = colors[0]
  alt_color = colors[1]
  edge_color = colors[0]

  if type == 'empty':
    type = 'full'
    face_color = colors[1]

  filled_marker_style = dict(marker='o',
                             markersize=radius,
                             markerfacecolor=face_color,
                             markerfacecoloralt=alt_color,
                             markeredgecolor=edge_color)

  ax.plot(center[0], center[1], fillstyle=type, **filled_marker_style, **kwargs)

def draw_arrow(xy: Tuple[float, float], direction: Literal['left', 'right'], ax: axes = None, color: Text = 'purple', head_length = 0.5, head_width = 0.1, **kwargs):
  if ax is None:
    ax = plt.gca()

  num_dir = 1 if direction == "right" else -1
  plt.arrow(xy[0] - 0.5 * head_length * num_dir, xy[1], 0.001 * num_dir, 0, head_width=head_width, head_length=head_length, edgecolor='None', facecolor=color, **kwargs)