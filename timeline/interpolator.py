from core_schema.animation_spec import AnimationTween, TransformState
from timeline.easings import evaluate_easing


def interpolate_state(
    a: TransformState, b: TransformState, progress: float
) -> TransformState:
    return TransformState(
        x=a.x + (b.x - a.x) * progress,
        y=a.y + (b.y - a.y) * progress,
        scale_x=a.scale_x + (b.scale_x - a.scale_x) * progress,
        scale_y=a.scale_y + (b.scale_y - a.scale_y) * progress,
        rotation=a.rotation + (b.rotation - a.rotation) * progress,
        opacity=a.opacity + (b.opacity - a.opacity) * progress,
    )


def compute_layer_transform(
    initial: TransformState,
    animations: list[AnimationTween],
    current_time: float,
) -> TransformState:
    current = initial
    for anim in animations:
        if current_time < anim.start_time:
            continue
        p = (current_time - anim.start_time) / max(0.001, anim.duration)
        eased_p = evaluate_easing(p, anim.easing)
        current = interpolate_state(
            anim.from_transform, anim.to_transform, eased_p
        )
    return current
