from core_schema.style_spec import StickerStyle
import skia


class SkiaStickerEngine:

    @staticmethod
    def draw_path_with_sticker(
        canvas: skia.Canvas,
        path: skia.Path,
        fill_paint: skia.Paint,
        sticker_style: StickerStyle,
    ):
        if not sticker_style.enabled:
            canvas.drawPath(path, fill_paint)
            return

        sh = sticker_style.shadow
        # 1. Skia Native Gaussian Drop Shadow Filter
        if sh.enabled:
            shadow_paint = skia.Paint(
                AntiAlias=True,
                ImageFilter=skia.ImageFilters.DropShadowOnly(
                    sh.dx,
                    sh.dy,
                    sh.sigma_x,
                    sh.sigma_y,
                    skia.Color(*sh.color),
                ),
            )
            # Expand shadow contour
            border_stroke_shadow = skia.Paint(
                AntiAlias=True,
                Style=skia.Paint.kStroke_Style,
                StrokeWidth=sticker_style.border_width * 2,
                StrokeJoin=skia.Paint.kRound_Join,
                StrokeCap=skia.Paint.kRound_Cap,
                Color=skia.Color(*sh.color),
                ImageFilter=skia.ImageFilters.DropShadowOnly(
                    sh.dx,
                    sh.dy,
                    sh.sigma_x,
                    sh.sigma_y,
                    skia.Color(*sh.color),
                ),
            )
            canvas.drawPath(path, border_stroke_shadow)
            canvas.drawPath(path, shadow_paint)

        # 2. Die-cut Crisp White Sticker Outline
        border_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=sticker_style.border_width * 2,
            StrokeJoin=skia.Paint.kRound_Join,
            StrokeCap=skia.Paint.kRound_Cap,
            Color=skia.Color(*sticker_style.border_color),
        )
        canvas.drawPath(path, border_paint)

        # 3. Inner Fill
        canvas.drawPath(path, fill_paint)
