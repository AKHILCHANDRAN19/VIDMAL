from core_schema.scene_spec import LayerSpec


class LayerTrackManager:

    @staticmethod
    def get_render_order(layers: list[LayerSpec]) -> list[LayerSpec]:
        return sorted(layers, key=lambda l: l.z_index)
