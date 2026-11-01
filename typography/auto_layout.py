import kiwisolver as kiwi


class LayoutConstraintSolver:

    @staticmethod
    def resolve_bounds(
        target_x: float,
        target_y: float,
        width: float,
        height: float,
        canvas_w: float,
        canvas_h: float,
        padding: float = 24.0,
    ) -> tuple[float, float]:
        solver = kiwi.Solver()
        x = kiwi.Variable("x")
        y = kiwi.Variable("y")

        solver.addConstraint(x >= padding)
        solver.addConstraint(y >= padding)
        solver.addConstraint(x + width <= canvas_w - padding)
        solver.addConstraint(y + height <= canvas_h - padding)

        solver.addEditVariable(x, "strong")
        solver.addEditVariable(y, "strong")
        solver.suggestValue(x, target_x)
        solver.suggestValue(y, target_y)
        solver.updateVariables()

        return float(x.value()), float(y.value())
