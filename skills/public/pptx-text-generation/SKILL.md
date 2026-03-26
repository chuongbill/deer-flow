---
name: pptx-text-generation
description: "Use this skill to create professional, editable PowerPoint presentations with real text, shapes, charts, and AI-generated images. Creates .pptx files with actual editable text elements. Supports rich formatting, tables, charts, and professional design. Trigger when user wants an editable presentation, deck, or slides."
---

# PPTX Text-Based Generation Skill

## Overview

This skill creates **editable** PowerPoint presentations with **AI-generated images** and real text. Unlike image-only slides, the text is fully editable in PowerPoint/Google Slides.

## Setup

All dependencies are pre-installed. No setup needed.

---

## Workflow (One-Shot)

The entire presentation is created from a **single plan JSON file** using one command:

1. Create a plan JSON file in `/mnt/user-data/workspace/`
2. Run the generator script
3. Output is saved to `/mnt/user-data/outputs/`

### Step 1: Create Plan JSON

Write a plan file to `/mnt/user-data/workspace/plan.json`:

```json
{
    "title": "The Future of AI in Healthcare",
    "author": "DeerFlow",
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
            "title": "The Future of AI\nin Healthcare",
            "subtitle": "Transforming Patient Care Through Intelligence",
            "image_prompt": "Modern abstract AI healthcare illustration, glowing neural network on medical cross, dark navy background, futuristic, no text"
        },
        {
            "type": "content",
            "title": "Key Benefits",
            "bullets": [
                "Faster, more accurate diagnosis",
                "Reduced human error by up to 85%",
                "24/7 patient monitoring and alerts",
                "Personalized treatment plans"
            ],
            "image_prompt": "Doctor using holographic AI interface with patient vitals, futuristic hospital, soft blue lighting, no text",
            "image_position": "right"
        },
        {
            "type": "stats",
            "title": "By The Numbers",
            "stats": [
                {"value": "$150B", "label": "Global AI Healthcare\nMarket by 2030"},
                {"value": "85%", "label": "Reduction in\nDiagnostic Errors"},
                {"value": "3.6M", "label": "Lives Saved\nAnnually"}
            ]
        },
        {
            "type": "cards",
            "title": "Real-World Applications",
            "cards": [
                {"title": "Radiology", "description": "AI-powered image analysis detects tumors with 94% accuracy"},
                {"title": "Drug Discovery", "description": "ML reduces development time from 10 years to 2"},
                {"title": "Mental Health", "description": "NLP chatbots provide 24/7 therapeutic support"}
            ]
        },
        {
            "type": "closing",
            "title": "The Future is Now",
            "subtitle": "AI will not replace doctors.\nBut doctors who use AI will replace those who don't.",
            "image_prompt": "Serene futuristic hospital room with glowing soft blue AI avatar, warm ambient lighting, deep navy shadows, hopeful, no text"
        }
    ]
}
```

### Step 2: Run the Generator

```bash
python /mnt/skills/public/pptx-text-generation/scripts/generate_deck.py \
    --plan-file /mnt/user-data/workspace/plan.json \
    --output-file /mnt/user-data/outputs/presentation.pptx
```

That's it! The script automatically:
1. Generates AI images via Gemini for slides with `image_prompt`
2. Creates the PPTX with editable text, shapes, and the generated images
3. Saves everything to the output path

[!NOTE]
Do NOT read the generate_deck.py script. Just create the plan JSON and call it with the parameters above.

---

## Slide Types

### `title` — Title Slide
Full-bleed AI background with dark overlay, centered title + subtitle.

### `content` — Content Slide
Left-aligned title + bullet points, optional AI image on the right (or left with `"image_position": "left"`).

### `stats` — Statistics Slide
Big number callouts (up to 3) on dark background. Use `"image_prompt"` for background.

### `cards` — Card Grid Slide
Up to 3 cards with title + description on light background. Top accent bar.

### `closing` — Closing Slide
Full-bleed AI background with dark overlay, centered title + italic subtitle.

---

## Color Palettes

| Theme | primary | secondary | accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` | `CADCFC` | `FFFFFF` |
| **Forest & Moss** | `2C5F2D` | `97BC62` | `F5F5F5` |
| **Coral Energy** | `F96167` | `F9E795` | `FFFFFF` |
| **Warm Terracotta** | `B85042` | `E7E8D1` | `FFFFFF` |
| **Ocean Gradient** | `065A82` | `1C7293` | `FFFFFF` |
| **Charcoal Minimal** | `36454F` | `F2F2F2` | `FFFFFF` |

---

## Image Prompt Tips

- Always end with **"no text"** — real text is added by PptxGenJS
- Include the primary color code for visual consistency: `"dark navy background (#1E2761)"`
- Keep prompts specific: describe style, lighting, composition
- Use abstract/illustrative styles — they work best as backgrounds

---

## Advanced Usage

For full control over slide layouts, read [pptxgenjs.md](/mnt/skills/public/pptx-text-generation/pptxgenjs.md) and create a custom Node.js script. Pass the output path as `process.argv[2]`:

```bash
node /mnt/user-data/workspace/custom-script.js /mnt/user-data/outputs/deck.pptx
```

---

## Output Handling

After generation:
- The PPTX file is saved in `/mnt/user-data/outputs/`
- Share with user using `present_files` tool
- The file is **fully editable** in PowerPoint/Google Slides
