from typing import Any, Dict, List, Optional
from core_schema.animation_spec import AnimationTween, TransformState
from core_schema.style_spec import ShapeStyle
from pydantic import BaseModel, Field


class ShapeSpec(BaseModel):
    type: str  # 'grid_bg', 'triangle', 'attached_square', 'text_badge', 'stamp'
    params: Dict[str, Any] = Field(default_factory=dict)
    style: ShapeStyle = Field(default_factory=ShapeStyle)


class LayerSpec(BaseModel):
    id: str
    z_index: int = 0
    parent_id: Optional[str] = None
    shape: ShapeSpec
    initial_transform: TransformState
    animations: List[AnimationTween] = Field(default_factory=list)


class SceneSpec(BaseModel):
    scene_id: str
    duration: float
    narration: Optional[str] = None
    layers: List[LayerSpec]


class StoryboardSpec(BaseModel):
    title: str
    aspect_ratio: str = "16:9"
    width: int = 1920
    height: int = 1080
    scenes: List[SceneSpec]
