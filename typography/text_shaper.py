from typography.font_manager import FontManager
import skia
import uharfbuzz as hb


class TextShaper:

    @staticmethod
    def shape_and_measure(text: str, size: float = 36.0, bold: bool = True):
        font_path = FontManager.get_font_path(bold)
        typeface = FontManager.get_typeface(bold)
        sk_font = skia.Font(typeface, size)

        # HarfBuzz Text Shaping
        if font_path:
            with open(font_path, "rb") as font_file:
                font_data = font_file.read()
            hb_face = hb.Face(font_data)
            hb_font = hb.Font(hb_face)
            hb_font.scale = (int(size * 64), int(size * 64))

            buf = hb.Buffer()
            buf.add_str(text)
            buf.guess_segment_properties()
            hb.shape(hb_font, buf)

            total_advance_x = (
                sum(pos.x_advance for pos in buf.glyph_positions) / 64.0
            )
        else:
            total_advance_x = sk_font.measureText(text)

        bounds = skia.Rect()
        sk_font.measureText(text, bounds=bounds)

        return {
            "width": total_advance_x,
            "height": bounds.height(),
            "font": sk_font,
            "bounds": bounds,
        }
