"""Generate t-shirt mockup images using DALL-E."""
import os
import requests
from openai import OpenAI
from PIL import Image
from io import BytesIO

API_KEY = os.environ.get("OPENAI_API_KEY", "SET_YOUR_KEY_HERE")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

client = OpenAI(api_key=API_KEY)

TEES = {
    "tee_back_to_the_light": (
        "Product photo of a black t-shirt laid flat on a dark surface, photographed from above. "
        "The t-shirt has a large centered chest print of a synthwave retro sun setting over a horizon — "
        "warm amber and golden orange gradient sun with horizontal stripe cutouts, two small silhouette "
        "figures standing below, fiery sunset sky. The print is vibrant against the black cotton fabric. "
        "Moody studio lighting, minimal background, e-commerce product photography style. No text on the shirt."
    ),
    "tee_you_and_i": (
        "Product photo of a black t-shirt laid flat on a dark surface, photographed from above. "
        "The t-shirt has a large centered chest print of a synthwave cityscape at sunset — "
        "purple and orange gradient sky, silhouette of a city skyline, a glowing ethereal female figure, "
        "retro 80s aesthetic. The print is vibrant against the black cotton fabric. "
        "Moody studio lighting, minimal background, e-commerce product photography style. No text on the shirt."
    ),
    "tee_i_lost_you": (
        "Product photo of a black t-shirt laid flat on a dark surface, photographed from above. "
        "The t-shirt has a large centered chest print of a man standing in the rain holding a rose, "
        "pink and purple neon-lit rain, sunset in the background, melancholic synthwave atmosphere. "
        "The print is vibrant against the black cotton fabric. "
        "Moody studio lighting, minimal background, e-commerce product photography style. No text on the shirt."
    ),
}


def main():
    print("=== Generating T-shirt Mockups ===\n")

    for name, prompt in TEES.items():
        print(f"Generating: {name} ...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="hd",
            n=1,
        )
        url = response.data[0].url
        print(f"  Revised: {response.data[0].revised_prompt[:80]}...")

        img_data = requests.get(url).content
        img = Image.open(BytesIO(img_data))

        # Save master
        master_path = os.path.join(OUT_DIR, f"{name}_master.png")
        img.save(master_path, "PNG")
        print(f"  Saved: {master_path}")

        # Save web-optimized 800x800
        web = img.resize((800, 800), Image.LANCZOS)
        web_path = os.path.join(OUT_DIR, f"{name}.jpg")
        web.save(web_path, "JPEG", quality=90)
        print(f"  Saved: {web_path}")

    print("\n=== Done! ===")


if __name__ == "__main__":
    main()
