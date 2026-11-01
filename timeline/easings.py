import math


def evaluate_easing(t: float, method: str = "ease_out_cubic") -> float:
    t = max(0.0, min(1.0, t))
    if method == "linear":
        return t
    elif method == "ease_in":
        return t * t * t
    elif method == "ease_out_cubic":
        return 1.0 - (1.0 - t) ** 3
    elif method == "elastic":
        c4 = (2 * math.pi) / 3
        return (
            0.0
            if t == 0
            else (
                1.0
                if t == 1
                else 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * c4) + 1.0
            )
        )
    elif method == "bounce":
        n1, d1 = 7.5625, 2.75
        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            t -= 1.5 / d1
            return n1 * t * t + 0.75
        elif t < 2.5 / d1:
            t -= 2.25 / d1
            return n1 * t * t + 0.9375
        else:
            t -= 2.625 / d1
            return n1 * t * t + 0.984375
    return t
