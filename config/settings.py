import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ASPECT_RATIOS = {
    "16:9": (1920, 1080),  # Landscape (Desktop / YouTube)
    "9:16": (1080, 1920),  # Portrait (Reels / Shorts)
}

DEFAULT_ASPECT = os.getenv("ASPECT_RATIO", "16:9")
CANVAS_WIDTH, CANVAS_HEIGHT = ASPECT_RATIOS.get(DEFAULT_ASPECT, (1920, 1080))
FPS = int(os.getenv("FPS", 30))

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIRECTORY", "/storage/emulated/0/Download"))
if not OUTPUT_DIR.exists():
    OUTPUT_DIR = Path("./output")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_gemini_credentials() -> tuple[str, str]:
    cookies_data = None
    env_json = os.getenv("GEMINI_COOKIES_JSON")
    if env_json:
        try:
            cookies_data = json.loads(env_json)
        except Exception:
            pass

    if not cookies_data:
        search_paths = [
            os.getenv("GEMINI_COOKIES_PATH"),
            "/storage/emulated/0/Download/cookies.json",
            "./cookies.json",
        ]
        for p in search_paths:
            if p and Path(p).exists():
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        cookies_data = json.load(f)
                    break
                except Exception:
                    continue

    if not cookies_data:
        raise FileNotFoundError(
            "cookies.json missing! Place it in /storage/emulated/0/Download/cookies.json "
            "or set GEMINI_COOKIES_PATH in .env"
        )

    psid, psidts = "", ""
    if isinstance(cookies_data, list):
        for item in cookies_data:
            name = item.get("name")
            val = item.get("value", "")
            if name == "__Secure-1PSID":
                psid = val
            elif name == "__Secure-1PSIDTS":
                psidts = val
    elif isinstance(cookies_data, dict):
        psid = cookies_data.get("__Secure-1PSID", "")
        psidts = cookies_data.get("__Secure-1PSIDTS", "")

    if not psid:
        raise ValueError("Could not find '__Secure-1PSID' inside cookies.")
    return psid, psidts
