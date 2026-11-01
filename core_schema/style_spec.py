from typing import Optional, Tuple
from pydantic import BaseModel, Field


class ShadowStyle(BaseModel):
    enabled: bool = True
    color: Tuple[int, int, int, int] = (0, 0, 0, 60)
    sigma_x: float = 14.0
    sigma_y: float = 14.0
    dx: float = 0.0
    dy: float = 8.0


class StickerStyle(BaseModel):
    enabled: bool = True
    border_width: float = 18.0
    border_color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    shadow: ShadowStyle = Field(default_factory=ShadowStyle)


class ShapeStyle(BaseModel):
    fill_color: Tuple[int, int, int, int] = (45, 110, 85, 255)
    stroke_color: Optional[Tuple[int, int, int, int]] = (15, 15, 15, 255)
    stroke_width: float = 0.0
    sticker: StickerStyle = Field(default_factory=StickerStyle)
