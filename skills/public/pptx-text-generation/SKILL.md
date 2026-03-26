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
