import argparse
import asyncio
import os
from ai_director.prompt_parser import PromptParser
from config.settings import DEFAULT_ASPECT, FPS, OUTPUT_DIR
from renderer.cpu_compositor import SkiaCPUCompositor


async def run():
    parser = argparse.ArgumentParser(
        description="Skia Python Vector Motion Graphics Engine"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="Explain Pythagoras Theorem with attached squares on sides a, b, and hypotenuse c",
        help="Prompt for video generation",
    )
    parser.add_argument(
        "--format",
        type=str,
        default=DEFAULT_ASPECT,
        choices=["16:9", "9:16"],
        help="Aspect ratio: 16:9 (Landscape) or 9:16 (Reels/Shorts)",
    )
    args = parser.parse_args()

    print("=" * 65)
    print("      SKIA + UHARFBUZZ + PYAV VECTOR ENGINE (PRODUCTION)     ")
    print(f" Format: {args.format} | FPS: {FPS}")
    print("=" * 65)

    # 1. Parse prompt via Gemini Web API using cookies
    director = PromptParser()
    storyboard = await director.parse_prompt_to_storyboard(
        args.prompt, aspect_ratio=args.format
    )

    # 2. Output path directly in mobile Download folder
    slug = (
        storyboard.title.lower()
        .replace(" ", "_")
        .replace("?", "")
        .replace(",", "")
    )
    output_filename = f"{slug}_{args.format.replace(':', 'x')}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # 3. Compile and render via Skia CPU + PyAV
    compositor = SkiaCPUCompositor(storyboard, fps=FPS)
    compositor.render(output_path)

    print("=" * 65)
    print(f"🎉 Complete! Pure vector MP4 saved to: {output_path}")
    print("=" * 65)


if __name__ == "__main__":
    asyncio.run(run())
