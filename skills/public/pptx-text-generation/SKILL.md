---
name: pptx-text-generation
description: "Use this skill to create professional, editable PowerPoint presentations with real text, shapes, charts, and images. Creates .pptx files with actual text elements (not image-based slides). Supports rich formatting, icons, tables, charts, and professional design. Trigger when user wants an editable presentation, deck, or slides."
---

# PPTX Text-Based Generation Skill

## Overview

This skill creates **editable** PowerPoint presentations using PptxGenJS (JavaScript). Unlike image-based slides, these contain real text, shapes, charts, and icons that can be edited in PowerPoint.

## Quick Reference

| Task | Guide |
|------|-------|
| Create from scratch | Read [pptxgenjs.md](/mnt/skills/public/pptx-text-generation/pptxgenjs.md) |
| Edit existing | Read [editing.md](/mnt/skills/public/pptx-text-generation/editing.md) |

---

## Setup

`pptxgenjs` is pre-installed globally. No setup needed.

---

## Creating from Scratch

**Read [pptxgenjs.md](/mnt/skills/public/pptx-text-generation/pptxgenjs.md) for the full API reference.**

### Workflow

1. Create a JavaScript file in `/mnt/user-data/workspace/` that builds the presentation
2. **IMPORTANT**: The script MUST accept the output file path from the command line via `process.argv[2]`
3. Run it with Node.js, passing the output path as an argument
4. Output the .pptx to `/mnt/user-data/outputs/`

### Basic Example

Create `/mnt/user-data/workspace/create-pptx.js`:

```javascript
const pptxgen = require("pptxgenjs");

// IMPORTANT: Always get the output path from command line arguments
const outputPath = process.argv[2];
if (!outputPath) {
  console.error("Usage: node create-pptx.js <output-path>");
  process.exit(1);
}

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'DeerFlow';
pres.title = 'My Presentation';

// Title slide
let slide1 = pres.addSlide();
slide1.background = { color: "1E2761" };
slide1.addText("My Presentation", {
  x: 0.5, y: 1.5, w: 9, h: 2,
  fontSize: 44, fontFace: "Arial", color: "FFFFFF",
  bold: true, align: "center"
});
slide1.addText("Created with DeerFlow", {
  x: 0.5, y: 3.5, w: 9, h: 1,
  fontSize: 20, fontFace: "Arial", color: "CADCFC",
  align: "center"
});

// Content slide
let slide2 = pres.addSlide();
slide2.background = { color: "FFFFFF" };
slide2.addText("Key Points", {
  x: 0.5, y: 0.3, w: 9, h: 0.8,
  fontSize: 36, fontFace: "Arial", color: "1E2761", bold: true
});
slide2.addText([
  { text: "First important point", options: { bullet: true, breakLine: true } },
  { text: "Second important point", options: { bullet: true, breakLine: true } },
  { text: "Third important point", options: { bullet: true } }
], {
  x: 0.5, y: 1.5, w: 8, h: 3, fontSize: 18, fontFace: "Arial", color: "363636"
});

// Write to the output path provided via command line
pres.writeFile({ fileName: outputPath });
```

Then run (**pass the output path as an argument**):

```bash
node /mnt/user-data/workspace/create-pptx.js /mnt/user-data/outputs/presentation.pptx
```

> **CRITICAL**: Always pass the output file path as an argument to `node`, never hardcode `/mnt/user-data/` paths inside the JavaScript file. The bash command handles path resolution automatically.

---

## AI-Generated Images (Recommended)

**NEVER use web-searched images** — they may have copyright issues. Instead, generate custom images using the image-generation skill (Gemini API) and embed them in slides.

### Workflow

1. Read the image-generation skill: `/mnt/skills/public/image-generation/SKILL.md`
2. Generate images FIRST, then create the PPTX script that references them
3. Pass ALL file paths (images + output) as `process.argv` arguments

### Step 1: Generate Images

For each slide that needs an image, create a prompt JSON and generate it:

```bash
# Write the prompt
cat > /mnt/user-data/workspace/slide1-prompt.json << 'EOF'
{
  "prompt": "Modern abstract illustration of artificial intelligence in healthcare, showing a glowing neural network overlaid on a stylized medical cross, dark navy background (#1E2761), clean vector style, no text",
  "style": "Professional tech illustration, modern flat design with depth",
  "color_palette": "Navy #1E2761, ice blue #CADCFC, white accents"
}
EOF

# Generate the image
python /mnt/skills/public/image-generation/scripts/generate.py \
  --prompt-file /mnt/user-data/workspace/slide1-prompt.json \
  --output-file /mnt/user-data/outputs/slide1-bg.jpg \
  --aspect-ratio 16:9
```

### Step 2: Create PPTX with Generated Images

The JS script should accept image paths as additional CLI arguments:

```javascript
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

// Get output path and image paths from command line
const outputPath = process.argv[2];
const imagePaths = process.argv.slice(3); // All remaining args are image paths

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';

// Title slide with AI-generated background image
let slide1 = pres.addSlide();
if (imagePaths[0] && fs.existsSync(imagePaths[0])) {
  slide1.background = { path: imagePaths[0] };
} else {
  slide1.background = { color: "1E2761" };
}
slide1.addText("AI in Healthcare", {
  x: 0.5, y: 1.5, w: 9, h: 2,
  fontSize: 44, fontFace: "Arial", color: "FFFFFF",
  bold: true, align: "center",
  shadow: { type: "outer", color: "000000", blur: 6, offset: 2, opacity: 0.5 }
});

// Content slide with AI-generated inline image
let slide2 = pres.addSlide();
slide2.background = { color: "F5F5F5" };
slide2.addText("Key Benefits", {
  x: 0.5, y: 0.3, w: 5, h: 0.8,
  fontSize: 36, fontFace: "Arial", color: "1E2761", bold: true
});
slide2.addText([
  { text: "Faster diagnosis", options: { bullet: true, breakLine: true } },
  { text: "Reduced human error", options: { bullet: true, breakLine: true } },
  { text: "24/7 patient monitoring", options: { bullet: true } }
], {
  x: 0.5, y: 1.3, w: 5, h: 3, fontSize: 18, fontFace: "Arial", color: "363636"
});
// Right-side image
if (imagePaths[1] && fs.existsSync(imagePaths[1])) {
  slide2.addImage({ path: imagePaths[1], x: 5.5, y: 0.5, w: 4.2, h: 4.5 });
}

pres.writeFile({ fileName: outputPath });
```

### Step 3: Run with All Paths as Arguments

```bash
node /mnt/user-data/workspace/create-pptx.js \
  /mnt/user-data/outputs/presentation.pptx \
  /mnt/user-data/outputs/slide1-bg.jpg \
  /mnt/user-data/outputs/slide2-img.jpg
```

> **TIP**: Generate images that complement the slide content — abstract backgrounds for title slides, illustrative graphics for content slides, and data visualizations for stats slides. Always specify "no text" in image prompts since text will be added via PptxGenJS.

---

## Design Ideas

**Don't create boring slides.** Consider these for each slide:

### Color Palettes

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| **Forest & Moss** | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| **Ocean Gradient** | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| **Charcoal Minimal** | `36454F` (charcoal) | `F2F2F2` (off-white) | `212121` (black) |

### Layout Principles

- **Every slide needs a visual element** — icon, shape, chart, or image
- Two-column, icon + text rows, or 2x2 grids work well
- Large stat callouts (big numbers 60-72pt with small labels)
- 0.5" minimum margins, leave breathing room

### Typography

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

### Avoid

- Don't repeat the same layout across slides
- Don't center body text — left-align paragraphs
- Don't default to blue — pick topic-specific colors
- NEVER use `#` with hex colors (causes file corruption)
- NEVER encode opacity in hex color strings
- NEVER reuse option objects between calls (PptxGenJS mutates them)

---

## Output Handling

After generation:
- The PPTX file is saved in `/mnt/user-data/outputs/`
- Share the file with user using `present_files` tool
- The file is **fully editable** in PowerPoint/Google Slides

---

## Dependencies

- `pptxgenjs` (npm) — creating presentations from scratch
- `react-icons react react-dom sharp` (npm, optional) — for icons
- `markitdown[pptx]` (pip, optional) — text extraction from existing files
