import av
import numpy as np


class PyAVVideoEncoder:

    def __init__(
        self, output_path: str, width: int, height: int, fps: int = 30
    ):
        self.output_path = output_path
        self.width = width
        self.height = height
        self.fps = fps

        self.container = av.open(output_path, mode="w")
        self.stream = self.container.add_stream("libx264", rate=fps)
        self.stream.width = width
        self.stream.height = height
        self.stream.pix_fmt = "yuv420p"
        self.stream.options = {"crf": "18", "preset": "fast"}

    def write_skia_surface(self, surface_buffer: np.ndarray):
        # Skia surface is RGBA, convert to RGB for FFmpeg
        rgb_data = surface_buffer[:, :, :3]
        frame = av.VideoFrame.from_ndarray(rgb_data, format="rgb24")
        for packet in self.stream.encode(frame):
            self.container.mux(packet)

    def close(self):
        for packet in self.stream.encode():
            self.container.mux(packet)
        self.container.close()
