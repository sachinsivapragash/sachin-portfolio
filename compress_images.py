"""Shrink big photos so the pages load fast.
Usage (in PowerShell, from your Portfolio folder):
    pip install pillow
    python compress_images.py assets
A backup copy of the folder is made first (assets_backup)."""
import sys, os, shutil
from PIL import Image, ImageOps
root = sys.argv[1] if len(sys.argv) > 1 else "assets"
bak = root.rstrip("/\\") + "_backup"
if not os.path.exists(bak):
    shutil.copytree(root, bak)
MAX = 1800
saved = 0
for d, _, files in os.walk(root):
    for n in files:
        if not n.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        p = os.path.join(d, n)
        before = os.path.getsize(p)
        try:
            im = ImageOps.exif_transpose(Image.open(p))
            if max(im.size) > MAX:
                im.thumbnail((MAX, MAX), Image.LANCZOS)
            if n.lower().endswith(".png"):
                if before < 400_000 and max(im.size) <= MAX:
                    continue
                im.save(p, optimize=True)
            else:
                im.convert("RGB").save(p, "JPEG", quality=80, optimize=True, progressive=True)
        except Exception as e:
            print("skip", p, e); continue
        after = os.path.getsize(p)
        if after >= before:
            shutil.copy2(os.path.join(bak, os.path.relpath(p, root)), p)
        else:
            saved += before - after
            print(f"{p}: {before//1024} KB -> {after//1024} KB")
print(f"Saved {saved/1048576:.1f} MB")
