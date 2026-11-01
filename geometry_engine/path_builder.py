import numpy as np
import skia


class PathMath:

    @staticmethod
    def create_cubic_bezier(
        p0: tuple, p1: tuple, p2: tuple, p3: tuple
    ) -> skia.Path:
        path = skia.Path()
        path.moveTo(p0[0], p0[1])
        path.cubicTo(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1])
        return path

    @staticmethod
    def compute_outward_normal(p1: tuple, p2: tuple) -> np.ndarray:
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = np.hypot(dx, dy)
        if length == 0:
            return np.array([0.0, 1.0])
        return np.array([dy / length, -dx / length])

    @staticmethod
    def midpoint(p1: tuple, p2: tuple) -> tuple[float, float]:
        return ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)
