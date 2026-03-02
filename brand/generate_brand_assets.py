"""Generate Synthgubbar brand assets using DALL-E."""
import os
import requests
from openai import OpenAI
from PIL import Image
from io import BytesIO

API_KEY = os.environ.get("OPENAI_API_KEY", "SET_YOUR_KEY_HERE")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

client = OpenAI(api_key=API_KEY)

PROMPTS = {
    "retro-sun-icon": (
        "A minimal synthwave retro sun icon on a pure black background. "
        "The sun is a perfect circle with a warm gradient from golden amber center "
        "to deep purple edges. Horizontal stripe cutouts slice through the lower half, "
        "classic 80s retrowave style. Muted, desaturated colors — not neon bright. "
        "Colors: warm amber (#d4a574), dusty rose (#b45098), deep purple (#3a1050). "
        "Clean, geometric, suitable as a favicon or app icon. No text. Centered."
    ),
    "social-profile": (
        "A square synthwave profile image for a band called Synthgubbar. "
        "A retro sun setting behind a perspective grid that stretches to the horizon. "
        "Muted synthwave palette: deep purples, warm amber, dusty rose on near-black background. "
        "Twinkling stars in the sky above. Moody, mysterious, cinematic. "
        "No text, no people. Clean composition suitable for a social media avatar."
    ),
    "banner-wide": (
        "A wide cinematic synthwave landscape banner. Retro sun on the horizon with "
        "horizontal stripe cutouts. Perspective grid stretching into the distance below. "
        "Starry sky above. Muted color palette: deep purples (#1a0828), warm amber glow (#d4a574), "
        "dusty rose horizon (#b45098), near-black sky (#06050a). "
        "Atmospheric, moody, mysterious. No text, no people. "
        "Suitable as a website header or social media banner."
    ),
    "og-share-image": (
        "A synthwave scene optimized for social media sharing. "
        "Centered retro sun with horizontal stripe cutouts, sitting on a glowing horizon line. "
        "Purple perspective grid below, starfield above. "
        "Muted synthwave colors: amber, dusty rose, deep purple on near-black. "
        "Clean, iconic, moody. No text, no people. Perfectly centered composition."
    ),
}

RESIZE_SPECS = {
    "retro-sun-icon": [
        ("favicon-16x16.png", 16, 16),
        ("favicon-32x32.png", 32, 32),
        ("favicon-48x48.png", 48, 48),
        ("favicon-64x64.png", 64, 64),
        ("favicon-128x128.png", 128, 128),
        ("apple-touch-icon-180x180.png", 180, 180),
        ("android-chrome-192x192.png", 192, 192),
        ("android-chrome-512x512.png", 512, 512),
        ("icon-1024x1024.png", 1024, 1024),
    ],
    "social-profile": [
        ("profile-400x400.png", 400, 400),
        ("profile-800x800.png", 800, 800),
    ],
    "og-share-image": [
        ("og-image-1200x1200.png", 1200, 1200),
    ],
}


def generate_image(name, prompt, size="1024x1024"):
    print(f"\nGenerating: {name} ...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="hd",
        n=1,
    )
    url = response.data[0].url
    revised = response.data[0].revised_prompt
    print(f"  Revised prompt: {revised[:100]}...")

    img_data = requests.get(url).content
    img = Image.open(BytesIO(img_data))

    master_path = os.path.join(OUT_DIR, f"{name}-master.png")
    img.save(master_path, "PNG")
    print(f"  Saved: {master_path}")

    return img


def resize_and_save(img, specs):
    for filename, w, h in specs:
        resized = img.resize((w, h), Image.LANCZOS)
        path = os.path.join(OUT_DIR, filename)
        resized.save(path, "PNG")
        print(f"  Saved: {filename} ({w}x{h})")


def create_ico(img):
    sizes = [16, 32, 48]
    images = [img.resize((s, s), Image.LANCZOS) for s in sizes]

    # Save to brand folder
    ico_path = os.path.join(OUT_DIR, "favicon.ico")
    images[0].save(ico_path, format="ICO", sizes=[(s, s) for s in sizes],
                   append_images=images[1:])
    print(f"  Saved: favicon.ico (multi: {sizes})")

    # Copy to repo root
    root_ico = os.path.join(OUT_DIR, "..", "favicon.ico")
    images[0].save(root_ico, format="ICO", sizes=[(s, s) for s in sizes],
                   append_images=images[1:])
    print(f"  Saved: ../favicon.ico")


def main():
    print("=== Synthgubbar Brand Asset Generation ===\n")

    masters = {}

    # Generate square images (1024x1024)
    for name in ["retro-sun-icon", "social-profile", "og-share-image"]:
        masters[name] = generate_image(name, PROMPTS[name], "1024x1024")

    # Generate wide banner (1792x1024)
    masters["banner-wide"] = generate_image("banner-wide", PROMPTS["banner-wide"], "1792x1024")

    # Create resized versions
    print("\n--- Resizing ---")
    for name, specs in RESIZE_SPECS.items():
        print(f"\n{name}:")
        resize_and_save(masters[name], specs)

    # Create favicon.ico
    print("\n--- Favicon ICO ---")
    create_ico(masters["retro-sun-icon"])

    # Create banner resizes
    print("\n--- Banner resizes ---")
    banner = masters["banner-wide"]
    for suffix, w, h in [("1500x500", 1500, 500), ("1200x630", 1200, 630)]:
        resized = banner.resize((w, h), Image.LANCZOS)
        path = os.path.join(OUT_DIR, f"banner-{suffix}.png")
        resized.save(path, "PNG")
        print(f"  Saved: banner-{suffix}.png")

    print("\n=== Done! ===")
    print(f"All assets saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()
