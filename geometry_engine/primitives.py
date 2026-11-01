from core_schema.style_spec import ShapeStyle
from geometry_engine.sticker_engine import SkiaStickerEngine
import numpy as np
import skia
from typography.text_shaper import TextShaper


class VectorPrimitives:

    @staticmethod
    def draw_grid_background(
        canvas: skia.Canvas,
        w: int,
        h: int,
        step: int = 50,
        bg_color=(246, 247, 245, 255),
        grid_color=(224, 228, 225, 255),
    ):
        canvas.clear(skia.Color(*bg_color))
        paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=2.0,
            Color=skia.Color(*grid_color),
        )
        for x in range(0, w, step):
            canvas.drawLine(float(x), 0.0, float(x), float(h), paint)
        for y in range(0, h, step):
            canvas.drawLine(0.0, float(y), float(w), float(y), paint)

    @staticmethod
    def draw_right_triangle(
        canvas: skia.Canvas, a: float, b: float, style: ShapeStyle
    ):
        path = skia.Path()
        path.moveTo(0.0, a)
        path.lineTo(b, a)
        path.lineTo(0.0, 0.0)
        path.close()

        fill_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kFill_Style,
            Color=skia.Color(*style.fill_color),
        )
        SkiaStickerEngine.draw_path_with_sticker(
            canvas, path, fill_paint, style.sticker
        )

        # Right-angle indicator square
        sq = min(28.0, min(a, b) / 4.0)
        marker_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=3.0,
            Color=skia.Color(255, 255, 255, 220),
        )
        marker_path = skia.Path()
        marker_path.moveTo(0.0, a - sq)
        marker_path.lineTo(sq, a - sq)
        marker_path.lineTo(sq, a)
        canvas.drawPath(marker_path, marker_paint)

    @staticmethod
    def draw_attached_square(
        canvas: skia.Canvas,
        side: float,
        subdivisions: int,
        style: ShapeStyle,
    ):
        path = skia.Path()
        path.addRoundRect(
            skia.Rect(0.0, 0.0, side, side), 12.0, 12.0
        )

        fill_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kFill_Style,
            Color=skia.Color(*style.fill_color),
        )
        SkiaStickerEngine.draw_path_with_sticker(
            canvas, path, fill_paint, style.sticker
        )

        # Inner grid unit dividers
        div_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=2.0,
            Color=skia.Color(255, 255, 255, 75),
        )
        step = side / max(1, subdivisions)
        for i in range(1, subdivisions):
            p = float(i * step)
            canvas.drawLine(p, 0.0, p, side, div_paint)
            canvas.drawLine(0.0, p, side, p, div_paint)

    @staticmethod
    def draw_text_badge(
        canvas: skia.Canvas,
        text: str,
        bg_color=(255, 255, 255, 255),
        fg_color=(18, 18, 18, 255),
    ):
        metrics = TextShaper.shape_and_measure(text, size=36.0, bold=True)
        tw, th = metrics["width"], metrics["height"]
        pw, ph = 32.0, 18.0
        bw, bh = tw + pw * 2, th + ph * 2

        rect = skia.Rect(-bw / 2, -bh / 2, bw / 2, bh / 2)
        # Background rect
        bg_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kFill_Style,
            Color=skia.Color(*bg_color),
        )
        stroke_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=3.0,
            Color=skia.Color(*fg_color),
        )
        canvas.drawRect(rect, bg_paint)
        canvas.drawRect(rect, stroke_paint)

        # Text
        text_paint = skia.Paint(
            AntiAlias=True,
            Color=skia.Color(*fg_color),
        )
        canvas.drawString(
            text,
            -tw / 2,
            th / 2 - 4.0,
            metrics["font"],
            text_paint,
        )

    @staticmethod
    def draw_distressed_stamp(
        canvas: skia.Canvas, text: str, color=(205, 68, 52, 255)
    ):
        metrics = TextShaper.shape_and_measure(text, size=72.0, bold=True)
        tw, th = metrics["width"], metrics["height"]
        sw, sh = tw + 70.0, th + 50.0

        outer_rect = skia.Rect(-sw / 2, -sh / 2, sw / 2, sh / 2)
        inner_rect = skia.Rect(
            -sw / 2 + 10, -sh / 2 + 10, sw / 2 - 10, sh / 2 - 10
        )

        p1 = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=8.0,
            Color=skia.Color(*color),
        )
        p2 = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=4.0,
            Color=skia.Color(*color),
        )
        canvas.drawRoundRect(outer_rect, 14.0, 14.0, p1)
        canvas.drawRoundRect(inner_rect, 8.0, 8.0, p2)

        text_paint = skia.Paint(
            AntiAlias=True,
            Color=skia.Color(*color),
        )
        canvas.drawString(
            text,
            -tw / 2,
            th / 2 - 6.0,
            metrics["font"],
            text_paint,
        )
