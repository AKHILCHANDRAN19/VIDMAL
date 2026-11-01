import math
from core_schema.style_spec import ShapeStyle
from geometry_engine.sticker_engine import SkiaStickerEngine
import numpy as np
import skia
from typography.text_shaper import TextShaper


class VectorPrimitives:

    @staticmethod
    def hex_to_skia_color(hex_str: str, alpha: int = 255) -> int:
        hex_str = hex_str.lstrip("#")
        if len(hex_str) == 6:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            return skia.Color(r, g, b, alpha)
        return skia.Color(20, 24, 33, alpha)

    @staticmethod
    def draw_studio_background(canvas: skia.Canvas, w: int, h: int, params: dict):
        """Draws a modern studio gradient background with a subtle ambient radial glow."""
        stops = params.get("stops", ["#0A0F1D", "#020617"])
        c1 = VectorPrimitives.hex_to_skia_color(stops[0])
        c2 = VectorPrimitives.hex_to_skia_color(stops[1] if len(stops) > 1 else stops[0])

        # 1. Base Linear Gradient (Top to Bottom)
        paint = skia.Paint(
            Shader=skia.GradientShader.MakeLinear(
                points=[(0.0, 0.0), (0.0, float(h))],
                colors=[c1, c2],
            )
        )
        canvas.drawRect(skia.Rect(0, 0, w, h), paint)

        # 2. Ambient Focal Spotlight (Center Glow)
        glow_paint = skia.Paint(
            Shader=skia.GradientShader.MakeRadial(
                center=(w / 2.0, h / 2.0),
                radius=max(w, h) * 0.65,
                colors=[skia.Color(255, 255, 255, 18), skia.Color(0, 0, 0, 0)],
            )
        )
        canvas.drawRect(skia.Rect(0, 0, w, h), glow_paint)

        # 3. Micro Grid Pattern for Depth
        grid_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=1.0,
            Color=skia.Color(255, 255, 255, 8),
        )
        step = 60
        for x in range(0, w, step):
            canvas.drawLine(float(x), 0.0, float(x), float(h), grid_paint)
        for y in range(0, h, step):
            canvas.drawLine(0.0, float(y), float(w), float(y), grid_paint)

    @staticmethod
    def draw_circle(canvas: skia.Canvas, radius: float, label: str, style: ShapeStyle):
        """Draws a vector circle strictly centered at (0, 0)."""
        path = skia.Path()
        path.addCircle(0.0, 0.0, radius)

        fill_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kFill_Style,
            Color=skia.Color(*style.fill_color),
        )
        SkiaStickerEngine.draw_path_with_sticker(canvas, path, fill_paint, style.sticker)

        if label:
            metrics = TextShaper.shape_and_measure(label, size=min(38.0, radius / 2.5), bold=True)
            tp = skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, 255))
            canvas.drawString(label, -metrics["width"] / 2.0, metrics["height"] / 3.0, metrics["font"], tp)

    @staticmethod
    def draw_rectangle(canvas: skia.Canvas, w: float, h: float, label: str, style: ShapeStyle):
        """Draws a rounded rectangle centered at (0, 0)."""
        half_w, half_h = w / 2.0, h / 2.0
        path = skia.Path()
        path.addRoundRect(skia.Rect(-half_w, -half_h, half_w, half_h), 14.0, 14.0)

        fill_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kFill_Style,
            Color=skia.Color(*style.fill_color),
        )
        SkiaStickerEngine.draw_path_with_sticker(canvas, path, fill_paint, style.sticker)

        if label:
            metrics = TextShaper.shape_and_measure(label, size=min(36.0, h / 3.0), bold=True)
            tp = skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, 255))
            canvas.drawString(label, -metrics["width"] / 2.0, metrics["height"] / 3.0, metrics["font"], tp)

    @staticmethod
    def draw_triangle(canvas: skia.Canvas, base: float, height: float, style: ShapeStyle):
        """Draws a triangle strictly centered at its visual centroid (0, 0)."""
        half_b = base / 2.0
        oy = height / 3.0  # Centroid offset

        path = skia.Path()
        path.moveTo(0.0, -height + oy)
        path.lineTo(half_b, oy)
        path.lineTo(-half_b, oy)
        path.close()

        fill_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kFill_Style,
            Color=skia.Color(*style.fill_color),
        )
        SkiaStickerEngine.draw_path_with_sticker(canvas, path, fill_paint, style.sticker)

    @staticmethod
    def draw_arrow(canvas: skia.Canvas, length: float, label: str, style: ShapeStyle):
        """Draws an explanatory vector arrow pointing rightwards, centered at (0, 0)."""
        half_l = length / 2.0
        head_size = 28.0

        line_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=8.0,
            StrokeCap=skia.Paint.kRound_Cap,
            Color=skia.Color(*style.fill_color),
        )
        canvas.drawLine(-half_l, 0.0, half_l, 0.0, line_paint)

        # Arrowhead
        head = skia.Path()
        head.moveTo(half_l, 0.0)
        head.lineTo(half_l - head_size, -head_size * 0.7)
        head.lineTo(half_l - head_size, head_size * 0.7)
        head.close()

        head_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kFill_Style,
            Color=skia.Color(*style.fill_color),
        )
        canvas.drawPath(head, head_paint)

        if label:
            metrics = TextShaper.shape_and_measure(label, size=28.0, bold=True)
            tp = skia.Paint(AntiAlias=True, Color=skia.Color(240, 244, 248, 255))
            canvas.drawString(label, -metrics["width"] / 2.0, -16.0, metrics["font"], tp)

    @staticmethod
    def draw_text_badge(canvas: skia.Canvas, text: str, style: ShapeStyle):
        """Draws a badge centered at (0, 0)."""
        metrics = TextShaper.shape_and_measure(text, size=34.0, bold=True)
        tw, th = metrics["width"], metrics["height"]
        pw, ph = 30.0, 16.0
        bw, bh = tw + pw * 2, th + ph * 2

        rect = skia.Rect(-bw / 2, -bh / 2, bw / 2, bh / 2)
        bg_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kFill_Style,
            Color=skia.Color(255, 255, 255, 245),
        )
        border_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=2.5,
            Color=skia.Color(15, 23, 42, 255),
        )
        canvas.drawRoundRect(rect, 10.0, 10.0, bg_paint)
        canvas.drawRoundRect(rect, 10.0, 10.0, border_paint)

        text_paint = skia.Paint(AntiAlias=True, Color=skia.Color(15, 23, 42, 255))
        canvas.drawString(text, -tw / 2.0, th / 2.0 - 4.0, metrics["font"], text_paint)

    @staticmethod
    def draw_distressed_stamp(canvas: skia.Canvas, text: str, color=(225, 29, 72, 255)):
        """Draws an impact/equation stamp centered at (0, 0)."""
        metrics = TextShaper.shape_and_measure(text, size=64.0, bold=True)
        tw, th = metrics["width"], metrics["height"]
        sw, sh = tw + 64.0, th + 44.0

        outer = skia.Rect(-sw / 2, -sh / 2, sw / 2, sh / 2)
        inner = skia.Rect(-sw / 2 + 8, -sh / 2 + 8, sw / 2 - 8, sh / 2 - 8)

        p1 = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=6.0,
            Color=skia.Color(*color),
        )
        p2 = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=3.0,
            Color=skia.Color(*color),
        )
        canvas.drawRoundRect(outer, 12.0, 12.0, p1)
        canvas.drawRoundRect(inner, 8.0, 8.0, p2)

        tp = skia.Paint(AntiAlias=True, Color=skia.Color(*color))
        canvas.drawString(text, -tw / 2.0, th / 2.0 - 4.0, metrics["font"], tp)
