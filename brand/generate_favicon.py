"""Generate retro synthwave sun favicon at various resolutions."""
from PIL import Image, ImageDraw
import math
import os

def draw_retro_sun(size):
    """Draw a retro synthwave sun with horizontal stripe cutouts."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = size / 2, size / 2
    r = size * 0.44  # sun radius, slight margin for glow

    # Draw the sun as concentric circles for gradient effect
    steps = max(int(r), 50)
    for i in range(steps, 0, -1):
        t = i / steps  # 1.0 at edge, 0.0 at center
        # Gradient: center warm amber → mid orange-pink → edge deep purple
        if t < 0.4:
            # Inner: warm amber to orange
            f = t / 0.4
            red = int(235 + (220 - 235) * f)
            green = int(180 + (130 - 180) * f)
            blue = int(80 + (60 - 80) * f)
        elif t < 0.7:
            # Mid: orange to pink
            f = (t - 0.4) / 0.3
            red = int(220 + (200 - 220) * f)
            green = int(130 + (80 - 130) * f)
            blue = int(60 + (120 - 60) * f)
        else:
            # Outer: pink to deep purple
            f = (t - 0.7) / 0.3
            red = int(200 + (120 - 200) * f)
            green = int(80 + (40 - 80) * f)
            blue = int(120 + (140 - 120) * f)

        cr = r * t
        draw.ellipse(
            [cx - cr, cy - cr, cx + cr, cy + cr],
            fill=(red, green, blue, 255)
        )

    # Horizontal stripe cutouts (transparent gaps)
    stripe_count = 6
    for i in range(stripe_count):
        # Stripes in the lower portion of the sun (classic retro sun look)
        frac = 0.35 + (i / stripe_count) * 0.55
        y = cy - r + frac * r * 2
        # Gap height increases toward bottom
        gap = size * 0.012 * (1 + i * 0.7)

        # Clear the stripe area
        for py in range(max(0, int(y)), min(size, int(y + gap))):
            for px in range(size):
                dx = px - cx
                dy = py - cy
                if dx * dx + dy * dy < r * r:
                    img.putpixel((px, py), (0, 0, 0, 0))

    # Add subtle outer glow
    glow_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_r = r * 1.15
    glow_steps = 20
    for i in range(glow_steps, 0, -1):
        t = i / glow_steps
        gr = r + (glow_r - r) * t
        alpha = int(30 * (1 - t))
        glow_draw.ellipse(
            [cx - gr, cy - gr, cx + gr, cy + gr],
            fill=(180, 80, 160, alpha)
        )

    # Composite glow behind sun
    result = Image.alpha_composite(glow_img, img)
    return result


def main():
    sizes = {
        'favicon-16x16.png': 16,
        'favicon-32x32.png': 32,
        'favicon-48x48.png': 48,
        'favicon-64x64.png': 64,
        'favicon-128x128.png': 128,
        'apple-touch-icon.png': 180,
        'android-chrome-192x192.png': 192,
        'android-chrome-512x512.png': 512,
        'retro-sun-1024.png': 1024,
    }

    out_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate high-res master and downscale for quality
    master = draw_retro_sun(1024)

    for name, size in sizes.items():
        path = os.path.join(out_dir, name)
        if size == 1024:
            master.save(path, 'PNG')
        else:
            resized = master.resize((size, size), Image.LANCZOS)
            resized.save(path, 'PNG')
        print(f'  {name} ({size}x{size})')

    # Generate favicon.ico (multi-resolution)
    ico_sizes = [16, 32, 48]
    ico_images = [master.resize((s, s), Image.LANCZOS) for s in ico_sizes]
    ico_path = os.path.join(out_dir, 'favicon.ico')
    ico_images[0].save(ico_path, format='ICO', sizes=[(s, s) for s in ico_sizes],
                       append_images=ico_images[1:])
    print(f'  favicon.ico (multi: {ico_sizes})')

    # Also copy favicon.ico to repo root for browsers
    root_ico = os.path.join(out_dir, '..', 'favicon.ico')
    ico_images[0].save(root_ico, format='ICO', sizes=[(s, s) for s in ico_sizes],
                       append_images=ico_images[1:])
    print(f'  ../favicon.ico (copy)')

    print('\nDone!')


if __name__ == '__main__':
    main()
