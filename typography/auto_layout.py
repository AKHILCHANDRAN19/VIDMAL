import numpy as np
from shapely.geometry import box


class LayoutSupervisor:
    """Supervises scene layout: prevents overlaps, enforces safe margins, and centers visual mass."""

    @staticmethod
    def sanitize_and_balance_scene(layers: list, canvas_w: float, canvas_h: float, margin: float = 90.0):
        active_boxes = []

        # 1. Collision Repulsion Pass
        for i, layer in enumerate(layers):
            if layer.shape.type == "background":
                continue

            tf = layer.initial_transform
            # Estimate element width & height
            p = layer.shape.params
            ew = p.get("width", p.get("radius", 100) * 2)
            eh = p.get("height", p.get("radius", 100) * 2)
            half_w, half_h = (ew / 2.0) * tf.scale_x, (eh / 2.0) * tf.scale_y

            current_box = box(tf.x - half_w, tf.y - half_h, tf.x + half_w, tf.y + half_h)

            # Check overlap with previously placed elements
            for other_box in active_boxes:
                if current_box.intersects(other_box):
                    # Repel along the shortest displacement axis
                    dx = tf.x - other_box.centroid.x
                    dy = tf.y - other_box.centroid.y
                    dist = np.hypot(dx, dy)
                    if dist == 0:
                        dx, dy, dist = 0.0, 1.0, 1.0

                    push_dist = 60.0
                    tf.x += (dx / dist) * push_dist
                    tf.y += (dy / dist) * push_dist
                    current_box = box(tf.x - half_w, tf.y - half_h, tf.x + half_w, tf.y + half_h)

            # 2. Viewport Clamping (Safe Margins)
            tf.x = max(margin + half_w, min(canvas_w - margin - half_w, tf.x))
            tf.y = max(margin + half_h, min(canvas_h - margin - half_h, tf.y))

            active_boxes.append(current_box)

        # 3. Center of Mass Symmetry Balancing
        non_bg_layers = [l for l in layers if l.shape.type != "background"]
        if non_bg_layers:
            mean_x = sum(l.initial_transform.x for l in non_bg_layers) / len(non_bg_layers)
            mean_y = sum(l.initial_transform.y for l in non_bg_layers) / len(non_bg_layers)

            offset_x = (canvas_w / 2.0) - mean_x
            offset_y = (canvas_h / 2.0) - mean_y

            # Gently shift the scene toward perfect mathematical center
            for l in non_bg_layers:
                l.initial_transform.x += offset_x * 0.75
                l.initial_transform.y += offset_y * 0.75
                for anim in l.animations:
                    anim.from_transform.x += offset_x * 0.75
                    anim.from_transform.y += offset_y * 0.75
                    anim.to_transform.x += offset_x * 0.75
                    anim.to_transform.y += offset_y * 0.75
