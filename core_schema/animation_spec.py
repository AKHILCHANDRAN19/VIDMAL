from pydantic import BaseModel


class TransformState(BaseModel):
    x: float
    y: float
    scale_x: float = 1.0
    scale_y: float = 1.0
    rotation: float = 0.0  # In degrees
    opacity: float = 1.0


class AnimationTween(BaseModel):
    start_time: float
    duration: float
    easing: str = (
        "ease_out_cubic"  # 'linear', 'ease_in', 'ease_out_cubic', 'elastic', 'bounce'
    )
    from_transform: TransformState
    to_transform: TransformState
