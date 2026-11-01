from core_schema.scene_spec import LayerSpec, StoryboardSpec
from geometry_engine.primitives import VectorPrimitives
import numpy as np
from renderer.cache_manager import RenderCacheManager
from renderer.video_encoder import PyAVVideoEncoder
import skia
from timeline.interpolator import compute_layer_transform
from timeline.track import LayerTrackManager
from typography.auto_layout import LayoutSupervisor


class SkiaCPUCompositor:

    def __init__(self, storyboard: StoryboardSpec, fps: int = 30):
        self.sb = storyboard
        self.fps = fps
        self.w = storyboard.width
        self.h = storyboard.height
        self.cache = RenderCacheManager()

        self.surface = skia.Surface.MakeRasterN32Premul(self.w, self.h)
        self.canvas = self.surface.getCanvas()

    def render_layer(self, layer: LayerSpec, current_time: float):
        tf = compute_layer_transform(layer.initial_transform, layer.animations, current_time)
        if tf.opacity <= 0.01 or tf.scale_x <= 0.01:
            return

        self.canvas.save()
        self.canvas.translate(tf.x, tf.y)
        if abs(tf.rotation) > 0.01:
            self.canvas.rotate(tf.rotation)
        if abs(tf.scale_x - 1.0) > 0.001 or abs(tf.scale_y - 1.0) > 0.001:
            self.canvas.scale(tf.scale_x, tf.scale_y)

        shape = layer.shape
        t = shape.type
        p = shape.params
        st = shape.style

        if t == "circle":
            VectorPrimitives.draw_circle(self.canvas, p.get("radius", 120.0), p.get("label", ""), st)
        elif t == "rectangle":
            VectorPrimitives.draw_rectangle(self.canvas, p.get("width", 240.0), p.get("height", 160.0), p.get("label", ""), st)
        elif t == "triangle":
            VectorPrimitives.draw_triangle(self.canvas, p.get("base", 220.0), p.get("height", 200.0), st)
        elif t == "arrow":
            VectorPrimitives.draw_arrow(self.canvas, p.get("length", 200.0), p.get("label", ""), st)
        elif t == "text_badge":
            VectorPrimitives.draw_text_badge(self.canvas, p.get("text", "Concept"), st)
        elif t == "stamp":
            VectorPrimitives.draw_distressed_stamp(self.canvas, p.get("text", "LAW"))

        self.canvas.restore()

    def render(self, output_path: str):
        print(f"[*] Skia Compositing: {self.w}x{self.h} ({self.sb.aspect_ratio}) at {self.fps} FPS")
        encoder = PyAVVideoEncoder(output_path, self.w, self.h, fps=self.fps)

        for s_idx, scene in enumerate(self.sb.scenes):
            total_frames = int(scene.duration * self.fps)
            sorted_layers = LayerTrackManager.get_render_order(scene.layers)

            # Pass through the Layout Supervisor to balance symmetry and avoid overlaps
            LayoutSupervisor.sanitize_and_balance_scene(sorted_layers, self.w, self.h)

            # Discover scene background
            bg_layer = next((l for l in sorted_layers if l.shape.type == "background"), None)
            bg_params = bg_layer.shape.params if bg_layer else {"stops": ["#0A0F1D", "#020617"]}

            for frame_i in range(total_frames):
                current_time = frame_i / self.fps

                # 1. Studio Gradient Background
                VectorPrimitives.draw_studio_background(self.canvas, self.w, self.h, bg_params)

                # 2. Render Layers
                for layer in sorted_layers:
                    if layer.shape.type == "background":
                        continue
                    self.render_layer(layer, current_time)

                # 3. Direct memory copy to PyAV H.264 stream
                img = self.surface.makeImageSnapshot()
                pixel_bytes = img.tobytes()
                frame_arr = np.ndarray(
                    shape=(self.h, self.w, 4),
                    dtype=np.uint8,
                    buffer=pixel_bytes,
                )
                encoder.write_skia_surface(frame_arr)

        encoder.close()
        print(f"[✅] Render completed: {output_path}")
