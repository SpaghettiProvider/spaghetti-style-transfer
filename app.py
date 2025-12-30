import os, subprocess, glob
import gradio as gr
from PIL import Image
import sys

BASE = os.path.abspath("NeuralNeighborStyleTransfer")
CONTENT_DIR = os.path.join(BASE, "inputs", "content")
STYLE_DIR = os.path.join(BASE, "inputs", "style")
OUTPUT_DIR = os.path.join(BASE, "outputs")
SCRIPT_PATH = os.path.join(BASE, "styleTransfer.py")

os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(STYLE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

STYLE_PATH = os.path.join(STYLE_DIR, "spag.jpeg")

# Download spaghetti style once
if not os.path.exists(STYLE_PATH):
    subprocess.run([
        "curl", "-L",
        "https://i.imgur.com/9VbJoDy.jpeg",
        "-o", STYLE_PATH
    ], check=True)

def run_nn(
    image, alpha, dont_colorize, content_loss, high_res, no_flip
):
    if image is None:
        return None, None, "No image provided"

    # Save content
    name = os.path.basename(image)
    content_path = os.path.join(CONTENT_DIR, name)
    Image.open(image).save(content_path)

    base, ext = os.path.splitext(name)
    raw_out = os.path.join(OUTPUT_DIR, f"spaghetti_{base}_raw.png")
    final_out = os.path.join(OUTPUT_DIR, f"spaghetti_{base}.png")

    cmd = [
        sys.executable,
        SCRIPT_PATH,
        "--content_path", content_path,
        "--style_path", STYLE_PATH,
        "--output_path", raw_out,
        "--alpha", str(alpha),
    ]

    if dont_colorize: cmd.append("--dont_colorize")
    if content_loss: cmd.append("--content_loss")
    if high_res: cmd.append("--high_res")
    if no_flip: cmd.append("--no_flip")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        return None, None, e.stderr

    # Resize to original
    orig = Image.open(content_path)
    out = Image.open(raw_out)
    out.resize(orig.size, Image.LANCZOS).save(final_out)

    return raw_out, final_out, result.stdout

with gr.Blocks() as demo:
    gr.Markdown("## Spaghetti Neural Neighbor Style Transfer")

    img = gr.Image(type="filepath", label="Upload Image")

    alpha = gr.Slider(0.05, 1.0, value=0.4, label="Alpha: Lower = More spaghetti, Higher = More Original Image")
    dont_colorize = gr.Checkbox(True, label="Preserve Spaghetti colors: Turning this off will make the original image colours come though")
    content_loss = gr.Checkbox(True, label="Enable content loss: Preserves structure more, This creates a shinier look with more highlights for spaghetti")
    high_res = gr.Checkbox(False, label="High resolution (more VRAM): Not typically neccessary)")
    no_flip = gr.Checkbox(False, label="Disable Patch Flipping")

    run = gr.Button("Cook Spaghetti")

    raw = gr.Image(label="Raw Output")
    final = gr.Image(label="Final Output")
    log = gr.Textbox(lines=10, label="Console Output")

    run.click(
        run_nn,
        inputs=[img, alpha, dont_colorize, content_loss, high_res, no_flip],
        outputs=[raw, final, log]
    )

demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    inbrowser=True
)

