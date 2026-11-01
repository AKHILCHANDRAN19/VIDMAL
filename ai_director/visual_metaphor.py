class VisualMetaphorDirector:

    @staticmethod
    def get_layout_bounds(aspect_ratio: str = "16:9"):
        if aspect_ratio == "16:9":
            return {
                "width": 1920,
                "height": 1080,
                "center_x": 960,
                "center_y": 540,
                "scale": 1.25,
            }
        else:  # 9:16
            return {
                "width": 1080,
                "height": 1920,
                "center_x": 540,
                "center_y": 960,
                "scale": 1.0,
            }
