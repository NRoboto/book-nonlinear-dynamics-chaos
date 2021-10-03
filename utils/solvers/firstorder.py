import numpy as np
from typing import Tuple
from . import StepFunction, FirstOrderDiffEqn, SolverFunction

def num_sol_generator(step_fn: StepFunction, cutoff_limit: float = 1e-4, max_iterations: int = 1e6) -> SolverFunction:
  assert max_iterations > 0, "max_iterations must be positive"

  def solver(fn: FirstOrderDiffEqn, x_0: float = 0.0, t_step: float = 0.1, abs_max_limit: float = 100.0) -> Tuple[float, float]:
    assert t_step > 0, "t_step must be positive"

    t = [0]
    x = [x_0]
    x_diff = np.inf
    iteration_count = 0
    
    while((x_diff > cutoff_limit) & (iteration_count < max_iterations)):
      x_n = x[-1]
      t_next = t[-1] + t_step
      x_next = step_fn(fn, x_n, t_step)

      t.append(t_next)

      if(np.abs(x_next) > abs_max_limit):
        x.append(np.sign(x_next) * abs_max_limit)
        break

      x.append(x_next)
      x_diff = np.abs(x_next - x_n)

      iteration_count += 1

    return (t, x)
  return solver

def num_sol_euler_step(fn: FirstOrderDiffEqn, x_n: float = 0.0, t_step: float = 0.01) -> float:
  return x_n + fn(x_n) * t_step
  
num_sol_euler = num_sol_generator(num_sol_euler_step)

def num_sol_runge_kutta_step(fn: FirstOrderDiffEqn, x_n: float, t_step: float) -> float:
  k_1 = fn(x_n) * t_step
  k_2 = fn(x_n + 0.5 * k_1) * t_step
  k_3 = fn(x_n + 0.5 * k_2) * t_step
  k_4 = fn(x_n + k_3) * t_step

  return x_n + (k_1 + 2 * k_2 + 2 * k_3 + k_4) / 6

num_sol_runge_kutta = num_sol_generator(num_sol_runge_kutta_step)