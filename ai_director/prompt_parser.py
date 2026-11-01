import json
import re
from ai_director.llm_clients.gemini_client import GeminiWebClient
from ai_director.visual_metaphor import VisualMetaphorDirector
from core_schema.scene_spec import StoryboardSpec


class PromptParser:

    def __init__(self):
        self.client = GeminiWebClient()

    async def parse_prompt_to_storyboard(
        self, prompt: str, aspect_ratio: str = "16:9"
    ) -> StoryboardSpec:
        bounds = VisualMetaphorDirector.get_layout_bounds(aspect_ratio)
        w, h, cx, cy = (
            bounds["width"],
            bounds["height"],
            bounds["center_x"],
            bounds["center_y"],
        )

        system_prompt = f"""
You are the Technical Animation Director for a Skia-powered Vector Motion Engine.
Topic: "{prompt}".

CRITICAL LAYOUT RULES (TO AVOID ANY OVERLAPPING):
- Canvas: {w}x{h} ({aspect_ratio}).
- Triangle center anchor is at ({cx}, {cy + 40}).
- Right Triangle legs: leg_a=240, leg_b=320, hypotenuse=400.
- Attached Square A sits along leg a (left side, width 240, height 240).
- Attached Square B sits along leg b (bottom side, width 320, height 320).
- Text Badges must be placed cleanly outside of the shape boundaries.
- Stamp badge sits above the triangle without colliding.

Output strictly valid JSON matching this schema (no markdown formatting, no code fences):
{{
  "title": "{prompt.replace('"', '')}",
  "aspect_ratio": "{aspect_ratio}",
  "width": {w},
  "height": {h},
  "scenes": [
    {{
      "scene_id": "scene_1",
      "duration": 3.0,
      "narration": "Let us consider a right-angled triangle with legs a and b.",
      "layers": [
        {{
          "id": "bg",
          "z_index": 0,
          "shape": {{ "type": "grid_bg", "params": {{}}, "style": {{}} }},
          "initial_transform": {{ "x": {cx}, "y": {cy}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0 }},
          "animations": []
        }},
        {{
          "id": "triangle",
          "z_index": 2,
          "shape": {{
            "type": "triangle",
            "params": {{ "a": 240, "b": 320 }},
            "style": {{ "fill_color": [45, 110, 85, 255], "sticker": {{ "enabled": true, "border_width": 18 }} }}
          }},
          "initial_transform": {{ "x": {cx}, "y": {cy + 40}, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0 }},
          "animations": [
            {{
              "start_time": 0.2,
              "duration": 0.8,
              "easing": "elastic",
              "from_transform": {{ "x": {cx}, "y": {cy + 40}, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0 }},
              "to_transform": {{ "x": {cx}, "y": {cy + 40}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0 }}
            }}
          ]
        }},
        {{
          "id": "label_c",
          "z_index": 5,
          "shape": {{ "type": "text_badge", "params": {{ "text": "Hypotenuse (c)" }}, "style": {{}} }},
          "initial_transform": {{ "x": {cx + 80}, "y": {cy - 120}, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0 }},
          "animations": [
            {{
              "start_time": 1.0,
              "duration": 0.5,
              "easing": "ease_out_cubic",
              "from_transform": {{ "x": {cx + 80}, "y": {cy - 120}, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0 }},
              "to_transform": {{ "x": {cx + 80}, "y": {cy - 120}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0 }}
            }}
          ]
        }}
      ]
    }},
    {{
      "scene_id": "scene_2",
      "duration": 3.0,
      "narration": "Squares are constructed along the legs a and b.",
      "layers": [
        {{
          "id": "bg",
          "z_index": 0,
          "shape": {{ "type": "grid_bg", "params": {{}}, "style": {{}} }},
          "initial_transform": {{ "x": {cx}, "y": {cy}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0 }},
          "animations": []
        }},
        {{
          "id": "triangle",
          "z_index": 2,
          "shape": {{
            "type": "triangle",
            "params": {{ "a": 240, "b": 320 }},
            "style": {{ "fill_color": [45, 110, 85, 255], "sticker": {{ "enabled": true, "border_width": 18 }} }}
          }},
          "initial_transform": {{ "x": {cx}, "y": {cy + 40}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0 }},
          "animations": []
        }},
        {{
          "id": "sq_a",
          "z_index": 1,
          "shape": {{ "type": "attached_square", "params": {{ "side": 240, "subdivisions": 3 }}, "style": {{ "fill_color": [52, 120, 246, 255] }} }},
          "initial_transform": {{ "x": {cx - 280}, "y": {cy + 40}, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0 }},
          "animations": [
            {{
              "start_time": 0.2,
              "duration": 0.8,
              "easing": "ease_out_cubic",
              "from_transform": {{ "x": {cx - 280}, "y": {cy + 40}, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0 }},
              "to_transform": {{ "x": {cx - 280}, "y": {cy + 40}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0 }}
            }}
          ]
        }},
        {{
          "id": "sq_b",
          "z_index": 1,
          "shape": {{ "type": "attached_square", "params": {{ "side": 320, "subdivisions": 4 }}, "style": {{ "fill_color": [245, 140, 44, 255] }} }},
          "initial_transform": {{ "x": {cx}, "y": {cy + 320}, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0 }},
          "animations": [
            {{
              "start_time": 0.6,
              "duration": 0.8,
              "easing": "ease_out_cubic",
              "from_transform": {{ "x": {cx}, "y": {cy + 320}, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0 }},
              "to_transform": {{ "x": {cx}, "y": {cy + 320}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0 }}
            }}
          ]
        }}
      ]
    }},
    {{
      "scene_id": "scene_3",
      "duration": 3.0,
      "narration": "Thus, the sum of areas a squared and b squared equals c squared.",
      "layers": [
        {{
          "id": "bg",
          "z_index": 0,
          "shape": {{ "type": "grid_bg", "params": {{}}, "style": {{}} }},
          "initial_transform": {{ "x": {cx}, "y": {cy}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0 }},
          "animations": []
        }},
        {{
          "id": "triangle",
          "z_index": 2,
          "shape": {{
            "type": "triangle",
            "params": {{ "a": 240, "b": 320 }},
            "style": {{ "fill_color": [45, 110, 85, 255], "sticker": {{ "enabled": true, "border_width": 18 }} }}
          }},
          "initial_transform": {{ "x": {cx}, "y": {cy + 40}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0 }},
          "animations": []
        }},
        {{
          "id": "stamp_theorem",
          "z_index": 10,
          "shape": {{ "type": "stamp", "params": {{ "text": "a² + b² = c²" }}, "style": {{}} }},
          "initial_transform": {{ "x": {cx}, "y": {cy - 230}, "scale_x": 2.2, "scale_y": 2.2, "rotation": -4.0, "opacity": 0.0 }},
          "animations": [
            {{
              "start_time": 0.3,
              "duration": 0.6,
              "easing": "bounce",
              "from_transform": {{ "x": {cx}, "y": {cy - 230}, "scale_x": 2.2, "scale_y": 2.2, "rotation": -4.0, "opacity": 0.0 }},
              "to_transform": {{ "x": {cx}, "y": {cy - 230}, "scale_x": 1.0, "scale_y": 1.0, "rotation": -4.0, "opacity": 1.0 }}
            }}
          ]
        }}
      ]
    }}
  ]
}}
Allowed types: 'grid_bg', 'triangle', 'attached_square', 'text_badge', 'stamp'.
Return ONLY raw JSON.
"""
        print(f"[*] Contacting Gemini Web API for {aspect_ratio} storyboard...")
        raw_text = await self.client.ask(system_prompt)

        match = re.search(r"(\{.*\})", raw_text, re.DOTALL)
        if match:
            raw_text = match.group(1)

        data = json.loads(raw_text)
        return StoryboardSpec(**data)
