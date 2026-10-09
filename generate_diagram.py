from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("assets", exist_ok=True)

img = Image.new("RGB", (1200, 700), "#101827")
d = ImageDraw.Draw(img)
font = ImageFont.load_default()

d.text((450, 30), "NOVA AI ASSISTANT", fill="white", font=font)

boxes = [
    (400, 100, 800, 170, "USER INTERFACE"),
    (400, 220, 800, 290, "MAIN APPLICATION"),
    (400, 340, 800, 410, "RAG PIPELINE"),
    (40, 510, 340, 590, "DOCUMENT LOADER"),
    (450, 510, 750, 590, "EMBEDDINGS + FAISS"),
    (860, 510, 1160, 590, "LOCAL LLM"),
]

for x1, y1, x2, y2, label in boxes:
    d.rectangle((x1, y1, x2, y2), fill="#174A60", outline="#61C5FA", width=3)
    d.text((x1 + 20, y1 + 25), label, fill="white", font=font)

d.line((600, 170, 600, 220), fill="white", width=3)
d.line((600, 290, 600, 340), fill="white", width=3)
d.line((600, 410, 190, 510), fill="white", width=3)
d.line((600, 410, 600, 510), fill="white", width=3)
d.line((600, 410, 1010, 510), fill="white", width=3)

path = os.path.abspath("assets/nova-architecture.png")
img.save(path, format="PNG")
print("Saved:", path)
print("Bytes:", os.path.getsize(path))
