#!/usr/bin/env python3
"""
One-shot PPTX generator with AI-generated images.

Takes a single plan JSON file and produces a complete editable PPTX presentation
with Gemini-generated background images and real editable text.

Usage:
    python generate_deck.py --plan-file <plan.json> --output-file <output.pptx>

Plan JSON format:
{
    "title": "Presentation Title",
    "author": "Author Name",
    "color_scheme": {
        "primary": "1E2761",
        "secondary": "CADCFC",
        "accent": "FFFFFF",
        "text_dark": "363636",
        "text_light": "FFFFFF"
    },
    "slides": [
        {
            "type": "title",
            "title": "Main Title",
            "subtitle": "Tagline",
            "image_prompt": "Description for AI image generation, no text"
        },
        {
            "type": "content",
            "title": "Slide Title",
            "bullets": ["Point 1", "Point 2", "Point 3"],
            "image_prompt": "Description for inline image, no text",
            "image_position": "right"
        },
        {
            "type": "stats",
            "title": "By The Numbers",
            "stats": [
                {"value": "$150B", "label": "Market Size"},
                {"value": "85%", "label": "Accuracy"},
                {"value": "3.6M", "label": "Lives Saved"}
            ]
        },
        {
            "type": "cards",
            "title": "Key Areas",
            "cards": [
                {"title": "Card 1", "description": "Description 1"},
                {"title": "Card 2", "description": "Description 2"},
                {"title": "Card 3", "description": "Description 3"}
            ]
        },
        {
            "type": "closing",
            "title": "Closing Title",
            "subtitle": "Closing quote or call to action",
            "image_prompt": "Description for background image, no text"
        }
    ]
}
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile

# ── Image generation via Gemini API ──────────────────────────────────────────


def generate_image(prompt: str, output_path: str, aspect_ratio: str = "16:9") -> bool:
    """Generate an image using the Gemini API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(f"[WARN] GEMINI_API_KEY not set, skipping image: {output_path}")
        return False

    try:
        import requests
        from PIL import Image
        from io import BytesIO
    except ImportError:
        print("[WARN] Pillow/requests not installed, skipping image generation")
        return False

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }

    try:
        print(f"[INFO] Generating image: {os.path.basename(output_path)}...")
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        for candidate in data.get("candidates", []):
            for part in candidate.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img_data = base64.b64decode(part["inlineData"]["data"])
                    img = Image.open(BytesIO(img_data))
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
                    img.save(output_path, "JPEG", quality=92)
                    print(f"[OK] Generated: {output_path}")
                    return True

        print(f"[WARN] No image in API response for: {output_path}")
        return False

    except Exception as e:
        print(f"[ERROR] Image generation failed: {e}")
        return False


# ── Node.js PPTX generation ─────────────────────────────────────────────────


def build_nodejs_script(plan: dict, image_map: dict, output_path: str) -> str:
    """Generate the Node.js script that creates the PPTX."""
    colors = plan.get("color_scheme", {
        "primary": "1E2761",
        "secondary": "CADCFC",
        "accent": "FFFFFF",
        "text_dark": "363636",
        "text_light": "FFFFFF",
    })
    p = colors["primary"]
    s = colors["secondary"]
    a = colors["accent"]
    td = colors.get("text_dark", "363636")
    tl = colors.get("text_light", "FFFFFF")

    def js_str(text: str) -> str:
        """Escape text for safe embedding in JS string literals."""
        return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '')

    slides_js = []
    for i, slide in enumerate(plan.get("slides", [])):
        slide_type = slide.get("type", "content")
        img_path = image_map.get(i)
        img_js = f'"{img_path}"' if img_path else "null"

        if slide_type == "title":
            title = js_str(slide.get("title", ""))
            subtitle = js_str(slide.get("subtitle", ""))
            slides_js.append(f"""
  // ── Slide {i+1}: Title ──
  (function() {{
    let sl = pres.addSlide();
    let img = {img_js};
    if (img && fs.existsSync(img)) {{
      sl.background = {{ path: img }};
      sl.addShape(pres.shapes.RECTANGLE, {{
        x: 0, y: 0, w: 10, h: 5.625,
        fill: {{ color: "000000", transparency: 40 }}
      }});
    }} else {{
      sl.background = {{ color: "{p}" }};
    }}
    sl.addText("{title}", {{
      x: 0.5, y: 1.2, w: 9, h: 2.5,
      fontSize: 44, fontFace: "Arial", color: "{tl}",
      bold: true, align: "center", valign: "middle",
      shadow: {{ type: "outer", color: "000000", blur: 8, offset: 3, opacity: 0.6 }}
    }});
    sl.addText("{subtitle}", {{
      x: 0.5, y: 3.8, w: 9, h: 0.8,
      fontSize: 20, fontFace: "Arial", color: "{s}",
      align: "center"
    }});
  }})();
""")
        elif slide_type == "content":
            title = js_str(slide.get("title", ""))
            bullets = slide.get("bullets", [])
            pos = slide.get("image_position", "right")
            bullet_items = []
            for bi, b in enumerate(bullets):
                b_escaped = js_str(b)
                bl = "true" if bi < len(bullets) - 1 else "false"
                bullet_items.append(
                    f'{{ text: "{b_escaped}", options: {{ bullet: true, breakLine: {bl} }} }}'
                )
            bullets_arr = ",\n        ".join(bullet_items)
            text_x = "0.5" if pos == "right" else "5.0"
            text_w = "4.8" if img_path else "9"
            img_x = "5.5" if pos == "right" else "0.3"

            slides_js.append(f"""
  // ── Slide {i+1}: Content ──
  (function() {{
    let sl = pres.addSlide();
    sl.background = {{ color: "{a}" }};
    sl.addShape(pres.shapes.RECTANGLE, {{
      x: 0, y: 0, w: 0.08, h: 5.625,
      fill: {{ color: "{p}" }}
    }});
    sl.addText("{title}", {{
      x: {text_x}, y: 0.3, w: {text_w}, h: 0.8,
      fontSize: 36, fontFace: "Arial", color: "{p}", bold: true
    }});
    sl.addText([
        {bullets_arr}
    ], {{
      x: {text_x}, y: 1.3, w: {text_w}, h: 3.5,
      fontSize: 18, fontFace: "Arial", color: "{td}", paraSpaceAfter: 8
    }});
    let img = {img_js};
    if (img && fs.existsSync(img)) {{
      sl.addImage({{ path: img, x: {img_x}, y: 0.3, w: 4.2, h: 5.0 }});
    }}
  }})();
""")
        elif slide_type == "stats":
            title = js_str(slide.get("title", ""))
            stat_items = slide.get("stats", [])
            stat_blocks = []
            for si, st in enumerate(stat_items):
                val = js_str(st.get("value", ""))
                lab = js_str(st.get("label", ""))
                sx = 0.5 + si * 3.0
                stat_blocks.append(f"""
    sl.addShape(pres.shapes.RECTANGLE, {{
      x: {sx}, y: 1.5, w: 2.8, h: 3.2,
      fill: {{ color: "{a}", transparency: 10 }},
      shadow: {{ type: "outer", color: "000000", blur: 6, offset: 2, opacity: 0.15 }}
    }});
    sl.addText("{val}", {{
      x: {sx}, y: 1.8, w: 2.8, h: 1.2,
      fontSize: 48, fontFace: "Arial", color: "{s}",
      bold: true, align: "center", valign: "middle"
    }});
    sl.addText("{lab}", {{
      x: {sx}, y: 3.2, w: 2.8, h: 1.2,
      fontSize: 14, fontFace: "Arial", color: "{tl}",
      align: "center", valign: "top"
    }});""")

            slides_js.append(f"""
  // ── Slide {i+1}: Stats ──
  (function() {{
    let sl = pres.addSlide();
    let img = {img_js};
    if (img && fs.existsSync(img)) {{
      sl.background = {{ path: img }};
      sl.addShape(pres.shapes.RECTANGLE, {{
        x: 0, y: 0, w: 10, h: 5.625,
        fill: {{ color: "000000", transparency: 50 }}
      }});
    }} else {{
      sl.background = {{ color: "{p}" }};
    }}
    sl.addText("{title}", {{
      x: 0.5, y: 0.3, w: 9, h: 0.8,
      fontSize: 36, fontFace: "Arial", color: "{tl}", bold: true
    }});
    {"".join(stat_blocks)}
  }})();
""")
        elif slide_type == "cards":
            title = js_str(slide.get("title", ""))
            card_items = slide.get("cards", [])
            card_blocks = []
            for ci, c in enumerate(card_items):
                ct = js_str(c.get("title", ""))
                cd = js_str(c.get("description", ""))
                cx = 0.5 + ci * 3.0
                card_blocks.append(f"""
    sl.addShape(pres.shapes.RECTANGLE, {{
      x: {cx}, y: 1.6, w: 2.8, h: 3.2,
      fill: {{ color: "{a}" }},
      shadow: {{ type: "outer", color: "000000", blur: 4, offset: 2, opacity: 0.1 }}
    }});
    sl.addShape(pres.shapes.RECTANGLE, {{
      x: {cx}, y: 1.6, w: 2.8, h: 0.06,
      fill: {{ color: "{p}" }}
    }});
    sl.addText("{ct}", {{
      x: {cx + 0.2}, y: 1.9, w: 2.4, h: 0.6,
      fontSize: 20, fontFace: "Arial", color: "{p}", bold: true
    }});
    sl.addText("{cd}", {{
      x: {cx + 0.2}, y: 2.6, w: 2.4, h: 1.8,
      fontSize: 14, fontFace: "Arial", color: "666666"
    }});""")

            slides_js.append(f"""
  // ── Slide {i+1}: Cards ──
  (function() {{
    let sl = pres.addSlide();
    sl.background = {{ color: "F5F5F5" }};
    sl.addShape(pres.shapes.RECTANGLE, {{
      x: 0, y: 0, w: 10, h: 1.2,
      fill: {{ color: "{p}" }}
    }});
    sl.addText("{title}", {{
      x: 0.5, y: 0.2, w: 9, h: 0.8,
      fontSize: 32, fontFace: "Arial", color: "{tl}", bold: true
    }});
    {"".join(card_blocks)}
  }})();
""")
        elif slide_type == "closing":
            title = js_str(slide.get("title", ""))
            subtitle = js_str(slide.get("subtitle", ""))
            slides_js.append(f"""
  // ── Slide {i+1}: Closing ──
  (function() {{
    let sl = pres.addSlide();
    let img = {img_js};
    if (img && fs.existsSync(img)) {{
      sl.background = {{ path: img }};
      sl.addShape(pres.shapes.RECTANGLE, {{
        x: 0, y: 0, w: 10, h: 5.625,
        fill: {{ color: "000000", transparency: 50 }}
      }});
    }} else {{
      sl.background = {{ color: "{p}" }};
    }}
    sl.addText("{title}", {{
      x: 0.5, y: 1.5, w: 9, h: 1.5,
      fontSize: 48, fontFace: "Arial", color: "{tl}",
      bold: true, align: "center",
      shadow: {{ type: "outer", color: "000000", blur: 8, offset: 3, opacity: 0.6 }}
    }});
    sl.addText("{subtitle}", {{
      x: 1.5, y: 3.2, w: 7, h: 1.2,
      fontSize: 18, fontFace: "Arial", color: "{s}",
      italic: true, align: "center"
    }});
  }})();
""")

    pres_title = js_str(plan.get("title", "Presentation"))
    pres_author = js_str(plan.get("author", "DeerFlow"))

    script = f"""const pptxgen = require("pptxgenjs");
const fs = require("fs");

const outputPath = process.argv[2] || "{output_path}";

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "{pres_author}";
pres.title = "{pres_title}";

{"".join(slides_js)}

pres.writeFile({{ fileName: outputPath }})
  .then(() => console.log("[OK] PPTX created: " + outputPath))
  .catch((err) => console.error("[ERROR]", err));
"""
    return script


# ── Main orchestrator ────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Generate an editable PPTX with AI-generated images"
    )
    parser.add_argument(
        "--plan-file", required=True,
        help="Path to the presentation plan JSON file"
    )
    parser.add_argument(
        "--output-file", required=True,
        help="Output path for the generated PPTX file"
    )
    parser.add_argument(
        "--skip-images", action="store_true",
        help="Skip AI image generation (use solid color backgrounds)"
    )
    args = parser.parse_args()

    # Load plan
    with open(args.plan_file, "r") as f:
        plan = json.load(f)

    print(f"[INFO] Loaded plan: {plan.get('title', 'Untitled')}")
    print(f"[INFO] Slides: {len(plan.get('slides', []))}")

    # Generate images
    image_map = {}
    output_dir = os.path.dirname(args.output_file) or "."
    os.makedirs(output_dir, exist_ok=True)

    if not args.skip_images:
        for i, slide in enumerate(plan.get("slides", [])):
            prompt = slide.get("image_prompt")
            if prompt:
                img_path = os.path.join(output_dir, f"slide{i+1}-bg.jpg")
                if generate_image(prompt, img_path):
                    image_map[i] = img_path

    print(f"[INFO] Generated {len(image_map)} images")

    # Build and run Node.js script
    node_script = build_nodejs_script(plan, image_map, args.output_file)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".js", delete=False, dir=output_dir
    ) as f:
        f.write(node_script)
        js_path = f.name

    try:
        node_env = os.environ.copy()
        # Ensure global npm modules are findable
        npm_root = subprocess.run(
            ["npm", "root", "-g"], capture_output=True, text=True
        ).stdout.strip()
        if npm_root:
            node_env["NODE_PATH"] = npm_root

        result = subprocess.run(
            ["node", js_path, args.output_file],
            capture_output=True, text=True, env=node_env, timeout=30
        )
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        if result.returncode != 0:
            print(f"[ERROR] Node.js exited with code {result.returncode}")
            sys.exit(1)
    finally:
        os.unlink(js_path)

    print(f"[DONE] Presentation ready: {args.output_file}")


if __name__ == "__main__":
    main()
