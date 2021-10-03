from typing import Callable, Tuple

FirstOrderDiffEqn = Callable[[float], float]
StepFunction = Callable[[FirstOrderDiffEqn, float, float], float]
SolverFunction = Callable[[FirstOrderDiffEqn, float, float, float], Tuple[float, float]]