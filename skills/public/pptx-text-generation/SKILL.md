---
name: pptx-text-generation
description: "Use this skill to create professional, editable PowerPoint presentations with real text, shapes, charts, and AI-generated images. Creates .pptx files with actual editable text elements. Supports rich formatting, tables, charts, and professional design. Trigger when user wants an editable presentation, deck, or slides."
---

# PPTX Text-Based Generation Skill

## Quick Reference

| Task | Guide |
|------|-------|
| Create from plan JSON (recommended) | See [One-Shot Workflow](#one-shot-workflow) below |
| Create with full control | Read [pptxgenjs.md](pptxgenjs.md) + [style_code.md](style_code.md) |
| Edit or create from template | Read [editing.md](editing.md) |
| Choose a visual style | Read [styles.md](styles.md) |
| Style code snippets | Read [style_code.md](style_code.md) |
| Read/analyze content | `python -m markitdown presentation.pptx` |

---

## One-Shot Workflow (Recommended)

The simplest path: create a **plan JSON file** and run one command.

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

## Slide Types (One-Shot Workflow)

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

## Advanced: Custom Node.js Scripts

For layouts beyond the 5 built-in types (timeline, quote, two-column with icons, image+stats, etc.), write a custom Node.js script using [pptxgenjs.md](pptxgenjs.md) and [style_code.md](style_code.md).

**style_code.md** provides ready-to-use layout functions:
- **Title Slide** — full-bleed background + overlay
- **Stat Cards** — 2-4 metric callouts
- **Two-Column** — text + image side-by-side
- **Card Grid** — 2×2 or 2×3 content cards
- **Image + Stats** — photo with stat sidebar
- **Timeline** — numbered process steps
- **Quote** — large quote with attribution
- **Conclusion/CTA** — closing slide with contact

Pass the output path as `process.argv[2]`:

```bash
node /mnt/user-data/workspace/custom-script.js /mnt/user-data/outputs/deck.pptx
```

---

## Design Ideas

**Don't create boring slides.** Plain bullets on a white background won't impress anyone. Consider ideas from this list for each slide.

### Before Starting

- **Choose a style**: Read [styles.md](styles.md) and pick a style that matches the topic. Each preset bundles palette, typography, shapes, motifs, background strategy, and image prompt modifiers into a cohesive design system. If the user doesn't specify a style, suggest 2–3 options from the [Style Selection Guide](styles.md#style-selection-guide). **If no preset fits, design a custom style** — see [Custom / Freeform](styles.md#-custom--freeform). You may also [blend two compatible styles](styles.md#style-blending).
- **Apply the FULL style, not just colors**: Use the style's fonts, shapes, motif, and background strategy together. Cherry-picking colors alone won't create a cohesive look. This applies equally to presets and custom styles — define the complete system.
- **Dominance over equality**: One color should dominate (60-70% visual weight), with 1-2 supporting tones and one sharp accent. Never give all colors equal weight.
- **Background image discipline**: Reserve full-bleed background images for 2-3 high-impact slides (title, dramatic opener, conclusion). Use clean solid backgrounds for content-heavy slides — text on busy backgrounds is hard to read, even with overlays. Place images as inset illustrations instead (see [Background Strategy](#background-strategy)).
- **Commit to the visual motif**: Each style defines a motif (accent bars, thin lines, geometric shapes, etc.). Carry it across EVERY slide. Consistency is what separates a designed deck from a random one.
- **Use image prompt modifiers**: When generating images with `generate_image`, append the style's image prompt modifier to ensure visual consistency across all slides.

### For Each Slide

**Every slide needs a visual element** — image, chart, icon, or shape. Text-only slides are forgettable.

**Layout options:**
- Two-column (text left, illustration on right)
- Icon + text rows (icon in colored circle, bold header, description below)
- 2x2 or 2x3 grid (image on one side, grid of content blocks on other)
- Half-bleed image (full left or right side) with content overlay

**Data display:**
- Large stat callouts (big numbers 60-72pt with small labels below)
- Comparison columns (before/after, pros/cons, side-by-side options)
- Timeline or process flow (numbered steps, arrows)

**Visual polish:**
- Icons in small colored circles next to section headers
- Italic accent text for key stats or taglines

### Generating Images for Slides

**Don't use placeholders.** When a slide would benefit from an illustration, diagram, or background image, use the `generate_image` tool to create one. Never leave a slide text-only when an image would strengthen the message.

**When to generate images:**
- Title slides that need dramatic background imagery
- Slides explaining geography, logistics, or spatial relationships (maps, diagrams)
- Conceptual illustrations for abstract topics (strategy, growth, risk)
- Infographic-style visuals (process flows, comparison graphics)
- Product or feature showcases
- Any slide where text alone feels flat or forgettable

**Workflow:**
1. Identify which slides need images during the design phase
2. Use the `generate_image` tool with a detailed prompt describing the image you need
3. **⚠️ Crop to the correct aspect ratio** — The `generate_image` tool always outputs **square (1024×1024)** images. Square images get stretched/distorted when placed into non-square slide areas. **After generating, always crop:**
   ```bash
   # Full-bleed backgrounds (16:9)
   node /mnt/skills/public/pptx-text-generation/scripts/crop_image.js input.png output_wide.png 16:9

   # Side panel insets (portrait)
   node /mnt/skills/public/pptx-text-generation/scripts/crop_image.js input.png output_portrait.png 3:4

   # Side panel insets (landscape)
   node /mnt/skills/public/pptx-text-generation/scripts/crop_image.js input.png output_landscape.png 4:3
   ```
   Or use it programmatically in your script:
   ```javascript
   const { cropToRatio } = require("/mnt/skills/public/pptx-text-generation/scripts/crop_image");
   await cropToRatio("input.png", "output_wide.png", 16, 9);
   ```
4. Embed the cropped image using `slide.addImage({ path: "output_wide.png", ... })`
5. **ALWAYS use `sizing`** even on pre-cropped images as a safety net:
   - `sizing: { type: 'cover', w: X, h: Y }` — fills the area, crops excess (backgrounds, panels)
   - `sizing: { type: 'contain', w: X, h: Y }` — fits inside area, may leave gaps (logos, diagrams)

**Image prompt tips for presentations:**
- Include the color palette in the prompt (e.g., "using dark cherry red and navy tones")
- Specify "no text" if the image should be purely visual (text is added via PptxGenJS)
- For backgrounds, request "atmospheric" or "abstract" styles that won't compete with overlaid text
- For diagrams, describe the layout explicitly (e.g., "a simplified map showing the Strait of Hormuz with arrows indicating shipping routes")
- Match the style across all generated images for visual consistency

### Background Strategy

**Don't put background images on every slide.** Full-bleed images behind text create visual noise, reduce contrast, and make content-heavy slides hard to read — even with dark overlays.

Use a **sandwich structure** for image placement:

| Slide Type | Background | Image Usage |
|------------|-----------|-------------|
| **Title / opener** | Full-bleed image + dark overlay | Dramatic first impression |
| **Content slides** | Solid color (dark or light) | Images as **inset illustrations** (side panel, card, or banner) |
| **Conclusion / Q&A** | Full-bleed image + dark overlay | Closing visual impact |

For a typical 8-slide deck, only 2-3 slides should have full-bleed background images. The rest should use your solid palette color.

**Inset image patterns for content slides:**
- Two-column: text on left, image on right (or vice versa)
- Banner: narrow image strip across top or middle, content below
- Card embed: image inside a content card alongside text

**Full-bleed background example (title/conclusion only):**
```
// Generate an image first using the generate_image tool, then:
slide.addImage({
  path: "/absolute/path/to/generated_image.png",
  x: 0, y: 0, w: 10, h: 5.625,  // full-bleed background
  sizing: { type: "cover", w: 10, h: 5.625 }
});
// Add a semi-transparent overlay for text readability
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: "000000", transparency: 50 }
});
// Then add text on top
slide.addText("Title", { x: 1, y: 2, w: 8, h: 1, color: "FFFFFF", fontSize: 44 });
```

**Inset image example (content slides):**
```
// Solid background for readability
slide.background = { color: "0D0D1A" };
// Image as side illustration, not background
slide.addImage({
  path: "/absolute/path/to/image.png",
  x: 6.2, y: 1.3, w: 3.3, h: 3.8,  // right-side inset
  sizing: { type: "cover", w: 3.3, h: 3.8 }
});
// Content on the left has clean, high-contrast background
slide.addText("Content here", { x: 0.5, y: 1.3, w: 5.4, h: 1, color: "E0E0E0", fontSize: 14 });
```

### Typography

**Choose an interesting font pairing** — don't default to Arial. Pick a header font with personality and pair it with a clean body font.

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Cambria | Calibri |
| Trebuchet MS | Calibri |
| Impact | Arial |
| Palatino | Garamond |
| Consolas | Calibri |

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

### Spacing

- 0.5" minimum margins
- 0.3-0.5" between content blocks
- Leave breathing room—don't fill every inch

### Avoid (Common Mistakes)

- **Don't repeat the same layout** — vary columns, cards, and callouts across slides
- **Don't center body text** — left-align paragraphs and lists; center only titles
- **Don't skimp on size contrast** — titles need 36pt+ to stand out from 14-16pt body
- **Don't default to blue** — pick colors that reflect the specific topic
- **Don't mix spacing randomly** — choose 0.3" or 0.5" gaps and use consistently
- **Don't style one slide and leave the rest plain** — commit fully or keep it simple throughout
- **Don't create text-only slides** — add images, icons, charts, or visual elements; avoid plain title + bullets
- **Don't forget text box padding** — when aligning lines or shapes with text edges, set `margin: 0` on the text box or offset the shape to account for padding
- **Don't use low-contrast elements** — icons AND text need strong contrast against the background; avoid light text on light backgrounds or dark text on dark backgrounds
- **NEVER use accent lines under titles** — these are a hallmark of AI-generated slides; use whitespace or background color instead
- **Don't use full-bleed background images on every slide** — this is the most common AI-generated presentation mistake. Background images behind text create visual noise and hurt readability. Reserve them for title and conclusion slides only; use solid backgrounds with inset images for content slides

---

## Color Palettes (Quick Reference)

For the one-shot workflow, use these palettes in `color_scheme`. For the full style system with fonts, shapes, and motifs, see [styles.md](styles.md).

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

## QA (Content Verification)

After generating a presentation, verify the content is correct:

```bash
python -m markitdown output.pptx
```

Check for:
- Missing content, typos, wrong slide order
- Leftover placeholder text
- Content that was truncated or omitted

```bash
# Check for leftover placeholders
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|placeholder"
```

---

## Output Handling

After generation:
- The PPTX file is saved in `/mnt/user-data/outputs/`
- Share with user using `present_files` tool
- The file is **fully editable** in PowerPoint/Google Slides

---

## Dependencies

- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - image processing
- `npm install -g pptxgenjs` - creating from scratch
- `npm install -g react-icons react react-dom sharp` - icons for custom scripts

**Note:** Use `python3` (not `python`) to run scripts in this environment.
