from core_schema.scene_spec import LayerSpec, StoryboardSpec
from geometry_engine.primitives import VectorPrimitives
import numpy as np
from renderer.cache_manager import RenderCacheManager
from renderer.video_encoder import PyAVVideoEncoder
import skia
from timeline.interpolator import compute_layer_transform
from timeline.track import LayerTrackManager


class SkiaCPUCompositor:

    def __init__(self, storyboard: StoryboardSpec, fps: int = 30):
        self.sb = storyboard
        self.fps = fps
        self.w = storyboard.width
        self.h = storyboard.height
        self.cache = RenderCacheManager()

        # Allocate native Skia CPU Raster Surface
        self.surface = skia.Surface.MakeRasterN32Premul(self.w, self.h)
        self.canvas = self.surface.getCanvas()

    def render_layer(self, layer: LayerSpec, current_time: float):
        tf = compute_layer_transform(
            layer.initial_transform, layer.animations, current_time
        )
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

        if t == "triangle":
            VectorPrimitives.draw_right_triangle(
                self.canvas, p.get("a", 240.0), p.get("b", 320.0), st
            )
        elif t == "attached_square":
            VectorPrimitives.draw_attached_square(
                self.canvas,
                p.get("side", 240.0),
                p.get("subdivisions", 3),
                st,
            )
        elif t == "text_badge":
            VectorPrimitives.draw_text_badge(
                self.canvas, p.get("text", "Label")
            )
        elif t == "stamp":
            VectorPrimitives.draw_distressed_stamp(
                self.canvas, p.get("text", "a² + b² = c²")
            )

        self.canvas.restore()

    def render(self, output_path: str):
        print(
            f"[*] Skia Compositing: {self.w}x{self.h} ({self.sb.aspect_ratio}) at {self.fps} FPS"
        )
        encoder = PyAVVideoEncoder(
            output_path, self.w, self.h, fps=self.fps
        )

        for s_idx, scene in enumerate(self.sb.scenes):
            total_frames = int(scene.duration * self.fps)
            sorted_layers = LayerTrackManager.get_render_order(scene.layers)

            for frame_i in range(total_frames):
                current_time = frame_i / self.fps

                # Background Grid
                VectorPrimitives.draw_grid_background(
                    self.canvas, self.w, self.h
                )

                # Render sorted layers
                for layer in sorted_layers:
                    if layer.shape.type == "grid_bg":
                        continue
                    self.render_layer(layer, current_time)

                # Read pixels directly from Skia surface buffer to PyAV
                img = self.surface.makeImageSnapshot()
                pixel_bytes = img.tobytes()
                frame_arr = np.ndarray(
                    shape=(self.h, self.w, 4),
                    dtype=np.uint8,
                    buffer=pixel_bytes,
                )

                encoder.write_skia_surface(frame_arr)

        encoder.close()
        print(f"[✅] Pure Skia + PyAV render complete: {output_path}")
