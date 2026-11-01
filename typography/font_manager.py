import os
import freetype
import skia


class FontManager:
    _cached_typefaces = {}

    @staticmethod
    def get_font_path(bold: bool = True) -> str:
        candidates = [
            "/system/fonts/Roboto-Bold.ttf"
            if bold
            else "/system/fonts/Roboto-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
            if bold
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return ""

    @classmethod
    def get_typeface(cls, bold: bool = True) -> skia.Typeface:
        key = "bold" if bold else "regular"
        if key in cls._cached_typefaces:
            return cls._cached_typefaces[key]

        font_path = cls.get_font_path(bold)
        if font_path:
            # Validate through FreeType
            try:
                ft_face = freetype.Face(font_path)
            except Exception:
                pass
            tf = skia.Typeface.MakeFromFile(font_path)
        else:
            tf = skia.Typeface.MakeFromName(
                "sans-serif",
                skia.FontStyle.Bold() if bold else skia.FontStyle.Normal(),
            )

        cls._cached_typefaces[key] = tf
        return tf
