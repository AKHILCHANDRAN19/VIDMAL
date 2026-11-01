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
You are the Lead Visual Director of a studio-grade 2D Vector Motion Graphics Engine.
The user wants an educational motion graphics video explaining: "{prompt}".

TECHNICAL CANVAS SPECIFICATIONS:
- Resolution: {w}x{h} ({aspect_ratio})
- Center Anchor: ({cx}, {cy})
- Total Duration: 2 to 3 logical scenes, 3.0 to 4.0 seconds each.

DESIGN RULES (MANDATORY FOR STUDIO QUALITY):
1. NO OVERLAPPING: Never put two objects at the exact same coordinates. Space elements at least 160px apart.
2. BALANCE & SYMMETRY: Balance objects around the center ({cx}, {cy}). Do NOT pile objects in corners.
3. PROFESSIONAL BACKGROUND: Choose a background gradient matching the topic:
   - Science/Tech/Space/Physics: Deep dark void (#0A0F1D to #020617) with radiant accents.
   - Biology/Nature: Clean organic cream (#FDFBF7 to #F4EFE6) or forest hues.
   - Mathematics/Theory: Studio charcoal (#18181B to #09090B) with bright cyan and orange vectors.
   - Business/Finance: Rich dark slate (#0F172A) with gold and emerald accents.
4. AVAILABLE SHAPE TYPES:
   - "circle": params: {{"radius": 120, "label": "Text"}}
   - "rectangle": params: {{"width": 260, "height": 180, "label": "Text"}}
   - "triangle": params: {{"base": 240, "height": 200}}
   - "arrow": params: {{"length": 220, "label": "Energy"}} (points from one concept to another)
   - "text_badge": params: {{"text": "Key Concept"}}
   - "stamp": params: {{"text": "CORE LAW / FORMULA"}}

OUTPUT ONLY RAW VALID JSON MATCHING THIS EXACT SCHEMA (no markdown, no quotes around json, no preamble):
{{
  "title": "{prompt.replace('"', '')}",
  "aspect_ratio": "{aspect_ratio}",
  "width": {w},
  "height": {h},
  "scenes": [
    {{
      "scene_id": "scene_1",
      "duration": 3.5,
      "narration": "First introductory concept.",
      "layers": [
        {{
          "id": "bg",
          "z_index": 0,
          "shape": {{
            "type": "background",
            "params": {{"style": "gradient", "stops": ["#0A0F1D", "#020617"]}},
            "style": {{}}
          }},
          "initial_transform": {{"x": {cx}, "y": {cy}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0}},
          "animations": []
        }},
        {{
          "id": "hero_object",
          "z_index": 2,
          "shape": {{
            "type": "circle",
            "params": {{"radius": 140, "label": "Core"}},
            "style": {{"fill_color": [56, 189, 248, 255], "sticker": {{"enabled": true, "border_width": 14}}}}
          }},
          "initial_transform": {{"x": {cx}, "y": {cy}, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0}},
          "animations": [
            {{
              "start_time": 0.2,
              "duration": 0.8,
              "easing": "elastic",
              "from_transform": {{"x": {cx}, "y": {cy}, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0}},
              "to_transform": {{"x": {cx}, "y": {cy}, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0}}
            }}
          ]
        }}
      ]
    }}
  ]
}}
"""
        print(f"[*] Gemini Visual Director is planning topic: '{prompt}'...")
        raw_text = await self.client.ask(system_prompt)

        # Clean any accidental markdown wrap
        match = re.search(r"(\{.*\})", raw_text, re.DOTALL)
        if match:
            raw_text = match.group(1)

        try:
            data = json.loads(raw_text)
            return StoryboardSpec(**data)
        except Exception as e:
            print(f"[!] Warning: JSON parsing error ({e}). Generating adaptive clean scene...")
            return self._build_adaptive_fallback(prompt, aspect_ratio, w, h, cx, cy)

    def _build_adaptive_fallback(
        self, prompt: str, aspect_ratio: str, w: int, h: int, cx: int, cy: int
    ) -> StoryboardSpec:
        """Adaptive fallback if Gemini API experiences rate limits or returns broken JSON."""
        return StoryboardSpec(
            title=prompt,
            aspect_ratio=aspect_ratio,
            width=w,
            height=h,
            scenes=[
                {
                    "scene_id": "scene_1",
                    "duration": 3.5,
                    "narration": f"Understanding {prompt}",
                    "layers": [
                        {
                            "id": "bg",
                            "z_index": 0,
                            "shape": {"type": "background", "params": {"stops": ["#0A0F1D", "#020617"]}},
                            "initial_transform": {"x": cx, "y": cy, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0},
                            "animations": [],
                        },
                        {
                            "id": "main_badge",
                            "z_index": 2,
                            "shape": {
                                "type": "text_badge",
                                "params": {"text": prompt.upper()[:28]},
                                "style": {"fill_color": [30, 41, 59, 255]},
                            },
                            "initial_transform": {"x": cx, "y": cy - 120, "scale_x": 0.1, "scale_y": 0.1, "rotation": 0.0, "opacity": 0.0},
                            "animations": [
                                {
                                    "start_time": 0.2,
                                    "duration": 0.8,
                                    "easing": "elastic",
                                    "from_transform": {"x": cx, "y": cy - 120, "scale_x": 0.1, "scale_y": 0.1, "rotation": 0.0, "opacity": 0.0},
                                    "to_transform": {"x": cx, "y": cy - 120, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0},
                                }
                            ],
                        },
                        {
                            "id": "core_circle",
                            "z_index": 3,
                            "shape": {
                                "type": "circle",
                                "params": {"radius": 130, "label": "CORE"},
                                "style": {"fill_color": [56, 189, 248, 255]},
                            },
                            "initial_transform": {"x": cx, "y": cy + 80, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0},
                            "animations": [
                                {
                                    "start_time": 0.6,
                                    "duration": 0.8,
                                    "easing": "elastic",
                                    "from_transform": {"x": cx, "y": cy + 80, "scale_x": 0.01, "scale_y": 0.01, "rotation": 0.0, "opacity": 0.0},
                                    "to_transform": {"x": cx, "y": cy + 80, "scale_x": 1.0, "scale_y": 1.0, "rotation": 0.0, "opacity": 1.0},
                                }
                            ],
                        },
                    ],
                }
            ],
)
