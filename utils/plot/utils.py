from typing import Literal, Text, Tuple
from matplotlib.patches import Wedge, Circle
from matplotlib.pyplot import axes
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate

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

def plot_second_order_phase_portrait(df, initial_conds, xy_range, solver_options={}, **kwargs):
  X, Y = np.meshgrid(np.linspace(xy_range[0][0], xy_range[0][1], 14), np.linspace(xy_range[1][0], xy_range[1][1], 14))

  dy_dt = np.array(df(0, [X, Y]))
  dy_dt_normalised = dy_dt / np.linalg.norm(dy_dt, axis=0)

  plt.quiver(X, Y, dy_dt_normalised[0], dy_dt_normalised[1], scale=50, width=.002)
  for y0 in initial_conds:
    sol = integrate.solve_ivp(df, [0, 100], y0, max_step=0.01, **solver_options)
    plt.plot(sol.y[0], sol.y[1], **kwargs)

  plt.xlim(xy_range[0])
  plt.ylim(xy_range[1])

def plot_second_order_phase_portrait_polar(df, initial_conds, max_radius, solver_options={}, **kwargs):
  def df_cartesian(t, y):
    r = np.sqrt(y[0] ** 2 + y[1] ** 2)
    theta = np.arctan2(y[1], y[0])
    [r_dot, theta_dot] = df(t, [r, theta])

    return [r_dot * np.cos(theta) - r * theta_dot * np.sin(theta), r_dot * np.sin(theta) + r * theta_dot * np.cos(theta)]

  initial_conds_cartesian = [[r * np.cos(theta), r * np.sin(theta)] for [r, theta] in initial_conds]
  xy_range = [[-max_radius, max_radius], [-max_radius, max_radius]]
  plot_second_order_phase_portrait(df_cartesian, initial_conds_cartesian, xy_range, solver_options=solver_options, **kwargs)
  
def get_iterative_map_results(fn, init_val, num_iterations):
  x = init_val
  acc = [x]
  for _ in range(num_iterations):
    x = fn(x)
    acc.append(x)

  return acc

def plot_cobweb(fn, initial_conds, num_iterations = 5, x_range = [-1, 1]):
  x = np.linspace(*x_range, num=500)
  y = fn(x)
  plt.plot(x, y)
  plt.xlim(*x_range)
  plt.plot([x_range[0], x_range[1]], [x_range[0], x_range[1]], color="black")

  for init in initial_conds:
    ys = np.repeat(get_iterative_map_results(fn, init, num_iterations), 2)
    xs = np.roll(ys, 1)
    xs[0] = init
    plt.plot(xs, ys)

def plot_orbit_diagram(fn, init_val = .5, r_range = [1, 4], num_rs = 1000, num_iterations = 600, transient_iteration_count=300):
  rs = np.linspace(r_range[0], r_range[1], num_rs)

  for r in rs:
    values = get_iterative_map_results(fn(r), init_val, num_iterations)[transient_iteration_count:]
    plt.scatter([r for _ in values], values, color="black", s=.1)