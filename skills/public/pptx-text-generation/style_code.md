# Style Code Snippets

Ready-to-use PptxGenJS code for each style. Instead of deriving code from scratch, copy the style config + layout functions below.

**How to use:**
1. Copy the **Common Setup** section
2. Pick a **Style Config** and assign it to `STYLE`
3. Use the **Layout Functions** to build slides
4. Customize content — the layout and styling are handled

---

## Common Setup

Every presentation starts with this. Copy it, then pick a style config.

```javascript
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

// ── Icon Utilities ──────────────────────────────────────────
function renderIconSvg(IconComponent, color, size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color, size: String(size) })
  );
}
async function iconToBase64Png(IconComponent, color, size = 256) {
  const svg = renderIconSvg(IconComponent, color, size);
  const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
  return "image/png;base64," + pngBuffer.toString("base64");
}

// ── Presentation Init ───────────────────────────────────────
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10" × 5.625"
```

---

## Style Configs

Each config defines the complete design system. Pick one and assign it to `const STYLE = ...`.

### Config Structure

```javascript
const STYLE = {
  name: "Style Name",

  // Backgrounds
  bg: {
    dark: "hex",       // Title, conclusion, section dividers
    medium: "hex",     // Content card fills, alternate content bg
    light: "hex",      // Primary content background
  },

  // Typography colors
  text: {
    title: "hex",      // Slide titles (large bold)
    primary: "hex",    // Body text
    secondary: "hex",  // Captions, footnotes, muted text
    accent: "hex",     // Highlighted text, key values, section labels
    onDark: "hex",     // Text on dark backgrounds
    onLight: "hex",    // Text on light backgrounds
  },

  // Fonts
  fonts: {
    header: "Font Name",
    body: "Font Name",
  },

  // Cards and content blocks
  card: {
    fill: "hex",          // Card background color
    border: null,         // null = no border, or { color: "hex", pt: 1 }
    radius: 0,            // 0 = sharp, 0.05-0.2 = rounded
    shadow: true,         // Whether cards get drop shadows
    accentBar: null,      // null = no bar, or { w: 0.08, color: "hex" }
  },

  // Decorative elements
  motif: {
    type: "accent-bars",  // See motif types below
    color: "hex",         // Motif element color
    weight: 0.08,         // Line/bar thickness in inches
  },

  // Image generation
  imagePrompt: "style-specific prompt suffix, no text",
};
```

**Motif types:**
- `"accent-bars"` — Colored accent bars on left edge of cards (Dark Professional, Rational Blue)
- `"thin-lines"` — Thin horizontal/vertical divider lines (Pure Minimal, Academic, Nordic Research)
- `"thick-borders"` — Thick visible borders around content blocks (Neo-Brutalist, Comic)
- `"color-blocks"` — Large geometric color areas dividing the slide (Memphis, Geometric Bold, Bauhaus)
- `"frames"` — Elegant borders and image frames (Academic Curator, Documentary)
- `"none"` — No decorative elements, content floats freely (Apple Style, Cinematic Minimal)

---

### 🎓 Academic
```javascript
const STYLE = {
  name: "Academic",
  bg: { dark: "1B2838", medium: "F5F0E8", light: "F5F0E8" },
  text: { title: "1B2838", primary: "2C2C2C", secondary: "666666", accent: "8B0000", onDark: "F5F0E8", onLight: "2C2C2C" },
  fonts: { header: "Georgia", body: "Calibri" },
  card: { fill: "FFFFFF", border: { color: "D0C8B8", pt: 1 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "thin-lines", color: "8B0000", weight: 0.02 },
  imagePrompt: "academic, scholarly, clean illustration, textbook diagram style, no text",
};
```

### ✨ Pure Minimal
```javascript
const STYLE = {
  name: "Pure Minimal",
  bg: { dark: "F5F5F5", medium: "FAFAFA", light: "FFFFFF" },
  text: { title: "111111", primary: "333333", secondary: "999999", accent: "111111", onDark: "333333", onLight: "333333" },
  fonts: { header: "Calibri Light", body: "Calibri Light" },
  card: { fill: null, border: null, radius: 0, shadow: false, accentBar: null },
  motif: { type: "thin-lines", color: "CCCCCC", weight: 0.01 },
  imagePrompt: "minimalist, high key, clean white background, simple line art, no text",
};
```

### 🌙 Dark Professional
```javascript
const STYLE = {
  name: "Dark Professional",
  bg: { dark: "0D0D1A", medium: "1A1A2E", light: "16213E" },
  text: { title: "FFFFFF", primary: "E0E0E0", secondary: "A0A0A0", accent: "00D4FF", onDark: "E0E0E0", onLight: "1A1A2E" },
  fonts: { header: "Arial Black", body: "Calibri Light" },
  card: { fill: "1A1A2E", border: null, radius: 0, shadow: true, accentBar: { w: 0.08, color: "00D4FF" } },
  motif: { type: "accent-bars", color: "00D4FF", weight: 0.08 },
  imagePrompt: "dark mode aesthetic, futuristic, tech, clean, moody lighting, no text",
};
```

### 🌿 Botanical
```javascript
const STYLE = {
  name: "Botanical",
  bg: { dark: "2D4A22", medium: "F7F3E9", light: "F7F3E9" },
  text: { title: "2D4A22", primary: "2D2D2D", secondary: "6B6B5A", accent: "8B6914", onDark: "F7F3E9", onLight: "2D2D2D" },
  fonts: { header: "Palatino", body: "Garamond" },
  card: { fill: "FFFFFF", border: null, radius: 0.15, shadow: true, accentBar: null },
  motif: { type: "thin-lines", color: "8B6914", weight: 0.02 },
  imagePrompt: "botanical illustration, watercolor leaves, nature, soft natural lighting, no text",
};
```

### 🏺 Wabi-Sabi
```javascript
const STYLE = {
  name: "Wabi-Sabi",
  bg: { dark: "4A4238", medium: "E8E0D4", light: "F0EBE3" },
  text: { title: "3C3428", primary: "3C3428", secondary: "7A7062", accent: "8C7B6B", onDark: "E8E0D4", onLight: "3C3428" },
  fonts: { header: "Georgia", body: "Calibri" },
  card: { fill: "F0EBE3", border: null, radius: 0.1, shadow: false, accentBar: null },
  motif: { type: "none", color: "8C7B6B", weight: 0 },
  imagePrompt: "wabi-sabi aesthetic, natural textures, weathered surfaces, ceramic, earth tones, imperfect beauty, no text",
};
```

### 🔺 Memphis
```javascript
const STYLE = {
  name: "Memphis",
  bg: { dark: "2C3E50", medium: "F5F5F5", light: "FFFFFF" },
  text: { title: "2C3E50", primary: "2C3E50", secondary: "666666", accent: "FF6B6B", onDark: "FFFFFF", onLight: "2C3E50" },
  fonts: { header: "Impact", body: "Arial" },
  card: { fill: "FFFFFF", border: { color: "2C3E50", pt: 2 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "color-blocks", color: "FF6B6B", weight: 0 },
  imagePrompt: "memphis design pattern, geometric shapes, squiggles, 80s graphic design, bold primary colors, no text",
  extraColors: ["4ECDC4", "FFE66D"],
};
```

### ⚒️ Constructivism
```javascript
const STYLE = {
  name: "Constructivism",
  bg: { dark: "1A1A1A", medium: "CC0000", light: "E8D5A3" },
  text: { title: "E8D5A3", primary: "E8D5A3", secondary: "B0A080", accent: "CC0000", onDark: "E8D5A3", onLight: "1A1A1A" },
  fonts: { header: "Impact", body: "Arial" },
  card: { fill: "1A1A1A", border: { color: "CC0000", pt: 2 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "color-blocks", color: "CC0000", weight: 0 },
  imagePrompt: "constructivist art, soviet poster style, bold geometric, propaganda aesthetic, red and black, angular, no text",
};
```

### 🧱 Neo-Brutalist
```javascript
const STYLE = {
  name: "Neo-Brutalist",
  bg: { dark: "FFFFFF", medium: "F0F0F0", light: "FFFFFF" },
  text: { title: "000000", primary: "000000", secondary: "444444", accent: "FF5252", onDark: "000000", onLight: "000000" },
  fonts: { header: "Consolas", body: "Calibri" },
  card: { fill: "FFFFFF", border: { color: "000000", pt: 3 }, radius: 0, shadow: true, accentBar: null },
  motif: { type: "thick-borders", color: "000000", weight: 3 },
  imagePrompt: "brutalist design, raw, monochrome, high contrast, stark, no text",
};
// NOTE: Use hard shadows — { type: "outer", color: "000000", blur: 0, offset: 4, angle: 135, opacity: 1.0 }
```

### 👾 8-bit Pixel
```javascript
const STYLE = {
  name: "8-bit Pixel",
  bg: { dark: "0D0D2B", medium: "1A1A4E", light: "0D0D2B" },
  text: { title: "FFFFFF", primary: "FFFFFF", secondary: "8888CC", accent: "00FF41", onDark: "00FF41", onLight: "0D0D2B" },
  fonts: { header: "Consolas", body: "Consolas" },
  card: { fill: "1A1A4E", border: { color: "00FF41", pt: 2 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "thick-borders", color: "00FF41", weight: 2 },
  imagePrompt: "pixel art, 8-bit retro, arcade game style, low resolution pixels, neon colors on dark background, no text",
  extraColors: ["FF00FF"],
};
```

### ⚡ Electric Pop
```javascript
const STYLE = {
  name: "Electric Pop",
  bg: { dark: "1A1A2E", medium: "6C2BD9", light: "1A1A2E" },
  text: { title: "FFFFFF", primary: "FFFFFF", secondary: "C0C0E0", accent: "00D4AA", onDark: "FFFFFF", onLight: "1A1A2E" },
  fonts: { header: "Arial Black", body: "Calibri" },
  card: { fill: "2A1A4E", border: null, radius: 0.15, shadow: true, accentBar: { w: 0.08, color: "FF2D95" } },
  motif: { type: "accent-bars", color: "FF2D95", weight: 0.08 },
  imagePrompt: "neon gradients, vibrant electric colors, purple pink cyan, modern digital art, glowing, no text",
  extraColors: ["6C2BD9", "FF2D95"],
};
```

### 🔷 Geometric Bold
```javascript
const STYLE = {
  name: "Geometric Bold",
  bg: { dark: "1B3A5C", medium: "E8913A", light: "F5F5F5" },
  text: { title: "FFFFFF", primary: "FFFFFF", secondary: "C0D0E0", accent: "E8913A", onDark: "FFFFFF", onLight: "1B3A5C" },
  fonts: { header: "Arial Black", body: "Calibri" },
  card: { fill: "1B3A5C", border: { color: "E8913A", pt: 2 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "color-blocks", color: "E8913A", weight: 0 },
  imagePrompt: "bold geometric shapes, color blocks, abstract geometric art, strong lines, no text",
};
```

### 🎨 Morandi
```javascript
const STYLE = {
  name: "Morandi",
  bg: { dark: "6B5E52", medium: "C4B6A6", light: "F5F0EB" },
  text: { title: "3C3C3C", primary: "3C3C3C", secondary: "8A8278", accent: "D4A9A9", onDark: "F5F0EB", onLight: "3C3C3C" },
  fonts: { header: "Cambria", body: "Calibri Light" },
  card: { fill: "F5F0EB", border: null, radius: 0, shadow: true, accentBar: null },
  motif: { type: "none", color: "D4A9A9", weight: 0 },
  imagePrompt: "morandi colors, soft muted pastel tones, still life, understated elegance, oil painting, no text",
  extraColors: ["A3B5A6"],
};
```

### ❄️ Nordic Research
```javascript
const STYLE = {
  name: "Nordic Research",
  bg: { dark: "2B3A4A", medium: "E8ECF0", light: "F5F7FA" },
  text: { title: "2B3A4A", primary: "2B3A4A", secondary: "6B7B8A", accent: "4A90D9", onDark: "E8ECF0", onLight: "2B3A4A" },
  fonts: { header: "Trebuchet MS", body: "Calibri" },
  card: { fill: "FFFFFF", border: { color: "D0D8E0", pt: 1 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "thin-lines", color: "D0D8E0", weight: 0.01 },
  imagePrompt: "scandinavian design, clean minimal, data visualization, cold blue tones, clinical precision, no text",
};
```

### 🌊 Fluid Sensory
```javascript
const STYLE = {
  name: "Fluid Sensory",
  bg: { dark: "1A3A3A", medium: "2D6B6B", light: "1A3A3A" },
  text: { title: "F0EDE8", primary: "F0EDE8", secondary: "A0B8B0", accent: "E0A86E", onDark: "F0EDE8", onLight: "1A3A3A" },
  fonts: { header: "Georgia", body: "Calibri" },
  card: { fill: "2D6B6B", border: null, radius: 0.2, shadow: true, accentBar: null },
  motif: { type: "none", color: "E0A86E", weight: 0 },
  imagePrompt: "fluid gradient mesh, organic flowing shapes, liquid abstract, teal and gold tones, smooth organic, no text",
};
```

### 🎬 Cinematic Minimal
```javascript
const STYLE = {
  name: "Cinematic Minimal",
  bg: { dark: "0A0A0A", medium: "1A1A1A", light: "0A0A0A" },
  text: { title: "F5F5F5", primary: "F5F5F5", secondary: "888888", accent: "C4A35A", onDark: "F5F5F5", onLight: "0A0A0A" },
  fonts: { header: "Georgia", body: "Calibri Light" },
  card: { fill: "1A1A1A", border: null, radius: 0, shadow: false, accentBar: null },
  motif: { type: "thin-lines", color: "C4A35A", weight: 0.01 },
  imagePrompt: "cinematic photography, film still, dramatic lighting, moody atmosphere, shallow depth of field, no text",
};
```

### 🔵 Rational Blue
```javascript
const STYLE = {
  name: "Rational Blue",
  bg: { dark: "1E3A5F", medium: "2C5F8A", light: "F5F5F5" },
  text: { title: "FFFFFF", primary: "FFFFFF", secondary: "B0C8E0", accent: "E8913A", onDark: "FFFFFF", onLight: "1E3A5F" },
  fonts: { header: "Calibri", body: "Calibri" },
  card: { fill: "FFFFFF", border: null, radius: 0.05, shadow: true, accentBar: { w: 0.08, color: "1E3A5F" } },
  motif: { type: "accent-bars", color: "1E3A5F", weight: 0.08 },
  imagePrompt: "corporate professional, clean business, blue tones, structured, data-driven, no text",
};
```

### 🤎 Warm Neutral Venture
```javascript
const STYLE = {
  name: "Warm Neutral Venture",
  bg: { dark: "3D3D2E", medium: "F2EDE4", light: "F8F5F0" },
  text: { title: "3D3D2E", primary: "3D3D2E", secondary: "8A8070", accent: "B8860B", onDark: "F2EDE4", onLight: "3D3D2E" },
  fonts: { header: "Georgia", body: "Calibri" },
  card: { fill: "FFFFFF", border: null, radius: 0.1, shadow: true, accentBar: null },
  motif: { type: "thin-lines", color: "B8860B", weight: 0.02 },
  imagePrompt: "warm neutral tones, natural materials, sustainable, earthy, organic textures, artisan, no text",
};
```

### 📐 Contemporary Academic
```javascript
const STYLE = {
  name: "Contemporary Academic",
  bg: { dark: "4A5568", medium: "F7FAFC", light: "FFFFFF" },
  text: { title: "2D3748", primary: "2D3748", secondary: "718096", accent: "3182CE", onDark: "F7FAFC", onLight: "2D3748" },
  fonts: { header: "Calibri", body: "Calibri Light" },
  card: { fill: "FFFFFF", border: { color: "E2E8F0", pt: 1 }, radius: 0, shadow: true, accentBar: null },
  motif: { type: "thin-lines", color: "E2E8F0", weight: 0.01 },
  imagePrompt: "modern academic, clean research diagram, contemporary educational illustration, light neutral, no text",
};
```

### 🏛️ Academic Curator
```javascript
const STYLE = {
  name: "Academic Curator",
  bg: { dark: "2C2C2C", medium: "F5F2ED", light: "F5F2ED" },
  text: { title: "2C2C2C", primary: "2C2C2C", secondary: "8A8278", accent: "8B7355", onDark: "F5F2ED", onLight: "2C2C2C" },
  fonts: { header: "Palatino", body: "Garamond" },
  card: { fill: "FFFFFF", border: { color: "D0C8B8", pt: 0.5 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "frames", color: "8B7355", weight: 0.5 },
  imagePrompt: "museum exhibition, gallery photography, architectural photography, curated, elegant framing, no text",
};
```

### 🍎 Apple Style
```javascript
const STYLE = {
  name: "Apple Style",
  bg: { dark: "000000", medium: "FFFFFF", light: "FFFFFF" },
  text: { title: "1D1D1F", primary: "1D1D1F", secondary: "86868B", accent: "0071E3", onDark: "FFFFFF", onLight: "1D1D1F" },
  fonts: { header: "Calibri", body: "Calibri Light" },
  card: { fill: null, border: null, radius: 0, shadow: false, accentBar: null },
  motif: { type: "none", color: "0071E3", weight: 0 },
  imagePrompt: "Apple product photography style, clean white background, studio lighting, premium, minimalist, no text",
};
// NOTE: Apple style uses very few elements per slide. Increase font sizes — titles 48-72pt, statements 36pt+.
```

### 🧸 3D Clay
```javascript
const STYLE = {
  name: "3D Clay",
  bg: { dark: "4E342E", medium: "FFE8D6", light: "FFF5EE" },
  text: { title: "4E342E", primary: "4E342E", secondary: "8D6E63", accent: "FF8A65", onDark: "FFF5EE", onLight: "4E342E" },
  fonts: { header: "Calibri", body: "Calibri" },
  card: { fill: "FFFFFF", border: null, radius: 0.2, shadow: true, accentBar: null },
  motif: { type: "none", color: "FF8A65", weight: 0 },
  imagePrompt: "3D clay art, plasticine characters, soft pastel colors, cute cartoon, Pixar clay style, rounded, friendly, no text",
  extraColors: ["81C784"],
};
```

### 🔶 Bauhaus
```javascript
const STYLE = {
  name: "Bauhaus",
  bg: { dark: "000000", medium: "FFFFFF", light: "FFFFFF" },
  text: { title: "000000", primary: "000000", secondary: "666666", accent: "E53935", onDark: "FFFFFF", onLight: "000000" },
  fonts: { header: "Arial Black", body: "Arial" },
  card: { fill: "FFFFFF", border: { color: "000000", pt: 3 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "color-blocks", color: "E53935", weight: 0 },
  imagePrompt: "bauhaus design, primary colors, geometric shapes, circles triangles squares, red yellow blue, modernist art, no text",
  extraColors: ["FDD835", "1E88E5"],
};
```

### 📘 Blueprint
```javascript
const STYLE = {
  name: "Blueprint",
  bg: { dark: "003366", medium: "004488", light: "003366" },
  text: { title: "FFFFFF", primary: "FFFFFF", secondary: "88AACC", accent: "FFFFFF", onDark: "FFFFFF", onLight: "003366" },
  fonts: { header: "Consolas", body: "Calibri" },
  card: { fill: null, border: { color: "FFFFFF", pt: 1 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "thin-lines", color: "FFFFFF", weight: 0.25 },
  imagePrompt: "blueprint technical drawing, white lines on blue, engineering diagram, architectural plan, schematic, wireframe, no text",
};
// NOTE: No filled cards — use outline-only boxes on blue backgrounds.
```

### 💬 Comic
```javascript
const STYLE = {
  name: "Comic",
  bg: { dark: "2C2C2C", medium: "FFE066", light: "FFFFFF" },
  text: { title: "000000", primary: "000000", secondary: "444444", accent: "FF4444", onDark: "FFFFFF", onLight: "000000" },
  fonts: { header: "Impact", body: "Arial" },
  card: { fill: "FFFFFF", border: { color: "000000", pt: 3 }, radius: 0, shadow: true, accentBar: null },
  motif: { type: "thick-borders", color: "000000", weight: 3 },
  imagePrompt: "comic book style, pop art, halftone dots, bold black outlines, vintage comic illustration, speech bubbles, action style, no text",
  extraColors: ["4488FF"],
};
// NOTE: Use hard shadows — { type: "outer", color: "000000", blur: 0, offset: 4, angle: 135, opacity: 1.0 }
// Use UPPERCASE for all headers.
```

### 📽️ Documentary
```javascript
const STYLE = {
  name: "Documentary",
  bg: { dark: "2C2416", medium: "F0E6D2", light: "F5F0E5" },
  text: { title: "2C2416", primary: "2C2416", secondary: "7A6B55", accent: "8B7355", onDark: "F0E6D2", onLight: "2C2416" },
  fonts: { header: "Georgia", body: "Calibri" },
  card: { fill: "F5F0E5", border: { color: "C8B89A", pt: 1 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "thin-lines", color: "8B7355", weight: 0.02 },
  imagePrompt: "documentary photography, sepia tone, historical, archival photo, grainy texture, vintage, photojournalism, no text",
};
```

### ✏️ Sketch
```javascript
const STYLE = {
  name: "Sketch",
  bg: { dark: "3C3832", medium: "F0EDE5", light: "FAFAF5" },
  text: { title: "333333", primary: "333333", secondary: "888880", accent: "E85D3A", onDark: "FAFAF5", onLight: "333333" },
  fonts: { header: "Georgia", body: "Calibri" },
  card: { fill: "FFFFFF", border: { color: "C0BBB0", pt: 1 }, radius: 0, shadow: false, accentBar: null },
  motif: { type: "none", color: "E85D3A", weight: 0 },
  imagePrompt: "hand-drawn sketch, pencil illustration, ink drawing, sketchbook style, line art, vintage illustration, no text",
};
```

### 🇨🇭 Swiss
```javascript
const STYLE = {
  name: "Swiss",
  bg: { dark: "000000", medium: "F0F0F0", light: "FFFFFF" },
  text: { title: "000000", primary: "000000", secondary: "666666", accent: "FF0000", onDark: "FFFFFF", onLight: "000000" },
  fonts: { header: "Arial", body: "Arial" },
  card: { fill: null, border: null, radius: 0, shadow: false, accentBar: null },
  motif: { type: "thin-lines", color: "000000", weight: 0.02 },
  imagePrompt: "swiss international typographic style, helvetica, grid-based design, minimal, red and black on white, no text",
};
// NOTE: Swiss style uses oversized numbers/letters as visual elements. Title fonts can go 60-80pt.
```

---

## Layout Functions

These functions accept a `STYLE` config and build slides. They handle all the styling; you just provide the content.

### Helper: Crop Images to Correct Aspect Ratio

**⚠️ The `generate_image` tool always outputs square (1024×1024) images.** Placing a square image into a 16:9 slide area will stretch it. **Always crop before placing.**

Use `scripts/crop_image.js` (CLI or programmatic):

```bash
# CLI — crop to standard ratios
node /mnt/skills/public/pptx-text-generation/scripts/crop_image.js input.png output.png 16:9   # backgrounds
node /mnt/skills/public/pptx-text-generation/scripts/crop_image.js input.png output.png 3:4    # portrait panels
node /mnt/skills/public/pptx-text-generation/scripts/crop_image.js input.png output.png 4:3    # landscape insets
```

```javascript
// Programmatic — use inside your presentation script
const { cropToRatio, cropBatch } = require("/mnt/skills/public/pptx-text-generation/scripts/crop_image");

// Single image
await cropToRatio("bg_square.png", "bg_wide.png", 16, 9);

// Batch — crop multiple images at once
await cropBatch([
  { input: "bg.png",    output: "bg_16x9.png",    ratio: [16, 9] },
  { input: "photo.png", output: "photo_3x4.png",   ratio: [3, 4]  },
  { input: "chart.png", output: "chart_4x3.png",   ratio: [4, 3]  },
]);

// Then place the cropped image — still use sizing as a safety net
slide.addImage({
  path: "bg_16x9.png",
  x: 0, y: 0, w: 10, h: 5.625,
  sizing: { type: "cover", w: 10, h: 5.625 },
});
```

### Helper: Shadow Factory

```javascript
// ALWAYS use a factory — PptxGenJS mutates shadow objects.
function makeShadow() {
  if (!STYLE.card.shadow) return undefined;
  // Neo-Brutalist and Comic get hard shadows
  if (STYLE.motif.type === "thick-borders") {
    return { type: "outer", color: "000000", blur: 0, offset: 4, angle: 135, opacity: 1.0 };
  }
  return { type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.15 };
}
```

### Helper: Section Label

Most styles use a small uppercase label above the title (e.g. "KEY METRICS").

```javascript
function addSectionLabel(slide, text, x = 0.8, y = 0.4) {
  const isDark = slide.background?.color === STYLE.bg.dark || slide.background?.color === STYLE.bg.medium;
  slide.addText(text.toUpperCase(), {
    x, y, w: 4, h: 0.35,
    fontSize: 10, fontFace: STYLE.fonts.body,
    color: STYLE.text.accent,
    charSpacing: 4, margin: 0,
  });
}
```

### Helper: Slide Title

```javascript
function addSlideTitle(slide, text, x = 0.8, y = 0.7, opts = {}) {
  const bgColor = slide.background?.color;
  const isOnDark = bgColor === STYLE.bg.dark || bgColor === STYLE.bg.medium;
  slide.addText(text, {
    x, y, w: opts.w || 8.4, h: opts.h || 0.7,
    fontSize: opts.fontSize || 32, fontFace: STYLE.fonts.header,
    color: isOnDark ? STYLE.text.onDark : STYLE.text.title,
    bold: true, margin: 0,
    ...opts,
  });
}
```

### Helper: Card with Motif

Draws a styled content card. Handles accent bars, thick borders, shadows, and rounding per the style config.

```javascript
function addCard(slide, x, y, w, h) {
  const c = STYLE.card;
  // Card background
  if (c.fill) {
    const shapeType = c.radius > 0 ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE;
    const cardOpts = {
      x, y, w, h,
      fill: { color: c.fill },
      shadow: makeShadow(),
    };
    if (c.radius > 0 && shapeType === pres.shapes.ROUNDED_RECTANGLE) cardOpts.rectRadius = c.radius;
    if (c.border) cardOpts.line = { color: c.border.color, width: c.border.pt };
    slide.addShape(shapeType, cardOpts);
  }

  // Accent bar (left edge, only on RECTANGLE cards — doesn't work with ROUNDED_RECTANGLE)
  if (c.accentBar && c.radius === 0) {
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y, w: c.accentBar.w, h,
      fill: { color: c.accentBar.color },
    });
  }
}
```

---

### Layout: Title Slide

Full-bleed background image with overlay, title, and subtitle.

```javascript
function titleSlide(pres, { title, subtitle, tagline, bgImagePath, date }) {
  const slide = pres.addSlide();

  // Background image + overlay
  if (bgImagePath) {
    slide.addImage({
      path: bgImagePath,
      x: 0, y: 0, w: 10, h: 5.625,
      sizing: { type: "cover", w: 10, h: 5.625 },
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 5.625,
      fill: { color: STYLE.bg.dark, transparency: 40 },
    });
  } else {
    slide.background = { color: STYLE.bg.dark };
  }

  // Optional top accent line
  if (STYLE.motif.type !== "none") {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.05,
      fill: { color: STYLE.motif.color },
    });
  }

  // Title
  slide.addText(title, {
    x: 0.8, y: 1.5, w: 8.4, h: 1.2,
    fontSize: 44, fontFace: STYLE.fonts.header,
    color: STYLE.text.onDark, bold: true,
    charSpacing: 3, margin: 0,
  });

  // Subtitle
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.8, y: 2.8, w: 8.4, h: 0.5,
      fontSize: 18, fontFace: STYLE.fonts.body,
      color: STYLE.text.accent, margin: 0,
    });
  }

  // Tagline
  if (tagline) {
    slide.addText(tagline, {
      x: 0.8, y: 3.5, w: 6, h: 0.5,
      fontSize: 14, fontFace: STYLE.fonts.body,
      color: STYLE.text.secondary, margin: 0,
    });
  }

  // Date footer
  if (date) {
    slide.addText(date, {
      x: 0.8, y: 5.1, w: 8.4, h: 0.35,
      fontSize: 10, fontFace: STYLE.fonts.body,
      color: STYLE.text.secondary, align: "right", margin: 0,
    });
  }

  return slide;
}
```

---

### Layout: Stat Cards (2–4 metrics)

```javascript
function statSlide(pres, { label, title, stats, footnote }) {
  // stats = [{ value: "98.7%", label: "Uptime", icon: base64Data }, ...]
  const slide = pres.addSlide();
  slide.background = { color: STYLE.bg.dark };

  addSectionLabel(slide, label);
  addSlideTitle(slide, title);

  const count = stats.length;
  const gap = 0.3;
  const totalW = 8.4;
  const cardW = (totalW - gap * (count - 1)) / count;

  stats.forEach((stat, i) => {
    const x = 0.8 + i * (cardW + gap);
    const y = 1.7;
    const h = 2.8;

    addCard(slide, x, y, cardW, h);

    const textX = x + (STYLE.card.accentBar ? STYLE.card.accentBar.w + 0.2 : 0.3);
    const textW = cardW - (STYLE.card.accentBar ? STYLE.card.accentBar.w + 0.5 : 0.6);

    // Icon
    if (stat.icon) {
      slide.addImage({ data: stat.icon, x: textX, y: y + 0.3, w: 0.45, h: 0.45 });
    }

    // Value
    slide.addText(stat.value, {
      x: textX, y: y + (stat.icon ? 0.9 : 0.4), w: textW, h: 0.9,
      fontSize: 40, fontFace: STYLE.fonts.header,
      color: STYLE.text.accent, bold: true, margin: 0,
    });

    // Label
    slide.addText(stat.label, {
      x: textX, y: y + (stat.icon ? 1.8 : 1.3), w: textW, h: 0.5,
      fontSize: 14, fontFace: STYLE.fonts.body,
      color: STYLE.text.secondary, margin: 0,
    });
  });

  if (footnote) {
    slide.addText(footnote, {
      x: 0.8, y: 5.0, w: 8, h: 0.3,
      fontSize: 10, fontFace: STYLE.fonts.body,
      color: STYLE.text.secondary, margin: 0,
    });
  }

  return slide;
}
```

---

### Layout: Two-Column (text + image)

```javascript
function twoColumnSlide(pres, { label, title, bullets, imagePath, imageOnLeft }) {
  // bullets = [{ icon: base64Data, text: "Description" }, ...]
  const slide = pres.addSlide();
  slide.background = { color: STYLE.bg.medium };

  addSectionLabel(slide, label);
  addSlideTitle(slide, title);

  const textX = imageOnLeft ? 5.3 : 0.8;
  const imgX = imageOnLeft ? 0.8 : 6.0;
  const textW = 4.2;
  const imgW = 3.5;
  const imgH = 3.5;

  // Bullet points
  bullets.forEach((b, i) => {
    const y = 1.6 + i * 0.85;
    if (b.icon) {
      slide.addImage({ data: b.icon, x: textX, y: y + 0.05, w: 0.35, h: 0.35 });
    }
    slide.addText(b.text, {
      x: textX + (b.icon ? 0.55 : 0), y, w: textW - (b.icon ? 0.55 : 0), h: 0.45,
      fontSize: 14, fontFace: STYLE.fonts.body,
      color: STYLE.text.primary, valign: "middle", margin: 0,
    });
  });

  // Image
  slide.addImage({
    path: imagePath,
    x: imgX, y: 1.3, w: imgW, h: imgH,
    sizing: { type: "cover", w: imgW, h: imgH },
  });

  return slide;
}
```

---

### Layout: Card Grid (2×2 or 2×3)

```javascript
function cardGridSlide(pres, { label, title, items, cols }) {
  // items = [{ icon: base64Data, title: "Title", desc: "Description" }, ...]
  // cols = 2 or 3
  const slide = pres.addSlide();
  slide.background = { color: STYLE.bg.dark };

  addSectionLabel(slide, label);
  addSlideTitle(slide, title);

  cols = cols || 3;
  const gap = 0.3;
  const totalW = 8.4;
  const cardW = (totalW - gap * (cols - 1)) / cols;
  const rows = Math.ceil(items.length / cols);
  const cardH = rows === 1 ? 2.8 : (3.5 / rows);
  const rowGap = rows === 1 ? 0 : 0.3;

  items.forEach((item, i) => {
    const col = i % cols;
    const row = Math.floor(i / cols);
    const x = 0.8 + col * (cardW + gap);
    const y = 1.6 + row * (cardH + rowGap);

    addCard(slide, x, y, cardW, cardH);

    const textX = x + (STYLE.card.accentBar ? STYLE.card.accentBar.w + 0.2 : 0.25);
    const textW = cardW - (STYLE.card.accentBar ? STYLE.card.accentBar.w + 0.5 : 0.5);

    // Icon in circle
    if (item.icon) {
      const circleSize = 0.5;
      slide.addShape(pres.shapes.OVAL, {
        x: textX, y: y + 0.15, w: circleSize, h: circleSize,
        fill: { color: STYLE.bg.light || STYLE.bg.medium },
      });
      slide.addImage({
        data: item.icon,
        x: textX + 0.08, y: y + 0.23, w: circleSize - 0.16, h: circleSize - 0.16,
      });
    }

    // Title
    slide.addText(item.title, {
      x: textX, y: y + (item.icon ? 0.75 : 0.15), w: textW, h: 0.3,
      fontSize: 13, fontFace: STYLE.fonts.body,
      color: STYLE.text.onDark, bold: true, margin: 0,
    });

    // Description
    if (item.desc) {
      slide.addText(item.desc, {
        x: textX, y: y + (item.icon ? 1.0 : 0.45), w: textW, h: 0.5,
        fontSize: 10, fontFace: STYLE.fonts.body,
        color: STYLE.text.secondary, margin: 0,
      });
    }
  });

  return slide;
}
```

---

### Layout: Image + Stats (team/company slide)

```javascript
function imageStatsSlide(pres, { label, title, imagePath, stats }) {
  // stats = [{ value: "120+", label: "Engineers", desc: "across 8 offices" }, ...]
  const slide = pres.addSlide();
  slide.background = { color: STYLE.bg.medium };

  addSectionLabel(slide, label);
  addSlideTitle(slide, title);

  // Left: image
  slide.addImage({
    path: imagePath,
    x: 0.8, y: 1.5, w: 4.0, h: 3.3,
    sizing: { type: "cover", w: 4.0, h: 3.3 },
  });

  // Right: stat cards
  stats.forEach((s, i) => {
    const x = 5.3;
    const y = 1.5 + i * 1.1;
    const w = 4.0;
    const h = 0.95;

    addCard(slide, x, y, w, h);

    const textX = x + (STYLE.card.accentBar ? STYLE.card.accentBar.w + 0.2 : 0.2);
    slide.addText(s.value, {
      x: textX, y: y + 0.08, w: 1.2, h: 0.8,
      fontSize: 28, fontFace: STYLE.fonts.header,
      color: STYLE.text.accent, bold: true, valign: "middle", margin: 0,
    });
    slide.addText([
      { text: s.label, options: { bold: true, fontSize: 14, color: STYLE.text.onDark, breakLine: true } },
      { text: s.desc, options: { fontSize: 11, color: STYLE.text.secondary } },
    ], {
      x: textX + 1.3, y: y + 0.08, w: 2.3, h: 0.8,
      fontFace: STYLE.fonts.body, valign: "middle", margin: 0,
    });
  });

  return slide;
}
```

---

### Layout: Conclusion / CTA

```javascript
function conclusionSlide(pres, { title, subtitle, contact, bgImagePath }) {
  const slide = pres.addSlide();

  if (bgImagePath) {
    slide.addImage({
      path: bgImagePath,
      x: 0, y: 0, w: 10, h: 5.625,
      sizing: { type: "cover", w: 10, h: 5.625 },
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 5.625,
      fill: { color: STYLE.bg.dark, transparency: 50 },
    });
  } else {
    slide.background = { color: STYLE.bg.dark };
  }

  // Top accent line
  if (STYLE.motif.type !== "none") {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 0.05,
      fill: { color: STYLE.motif.color },
    });
  }

  // CTA title
  slide.addText(title, {
    x: 1, y: 1.5, w: 8, h: 1.0,
    fontSize: 40, fontFace: STYLE.fonts.header,
    color: STYLE.text.onDark, bold: true, align: "center", margin: 0,
  });

  // Subtitle
  if (subtitle) {
    slide.addText(subtitle, {
      x: 1, y: 2.6, w: 8, h: 0.6,
      fontSize: 18, fontFace: STYLE.fonts.body,
      color: STYLE.text.accent, align: "center", margin: 0,
    });
  }

  // Contact card
  if (contact) {
    addCard(slide, 3, 3.5, 4, 1.0);
    const contactLines = [];
    if (contact.email) contactLines.push({ text: contact.email, options: { fontSize: 14, color: STYLE.text.accent, breakLine: true } });
    if (contact.url) contactLines.push({ text: contact.url, options: { fontSize: 12, color: STYLE.text.secondary } });
    slide.addText(contactLines, {
      x: 3, y: 3.5, w: 4, h: 1.0,
      fontFace: STYLE.fonts.body, align: "center", valign: "middle", margin: 0,
    });
  }

  return slide;
}
```

---

### Layout: Timeline / Process Flow

```javascript
function timelineSlide(pres, { label, title, steps }) {
  // steps = [{ number: "01", title: "Step Name", desc: "Details" }, ...]
  const slide = pres.addSlide();
  slide.background = { color: STYLE.bg.dark };

  addSectionLabel(slide, label);
  addSlideTitle(slide, title);

  const count = steps.length;
  const gap = 0.2;
  const totalW = 8.4;
  const stepW = (totalW - gap * (count - 1)) / count;

  // Connecting line
  slide.addShape(pres.shapes.LINE, {
    x: 0.8 + stepW / 2, y: 2.0,
    w: totalW - stepW, h: 0,
    line: { color: STYLE.motif.color || STYLE.text.secondary, width: 1, dashType: "dash" },
  });

  steps.forEach((step, i) => {
    const x = 0.8 + i * (stepW + gap);

    // Number circle
    slide.addShape(pres.shapes.OVAL, {
      x: x + stepW / 2 - 0.25, y: 1.75, w: 0.5, h: 0.5,
      fill: { color: STYLE.text.accent },
    });
    slide.addText(step.number, {
      x: x + stepW / 2 - 0.25, y: 1.75, w: 0.5, h: 0.5,
      fontSize: 14, fontFace: STYLE.fonts.header,
      color: STYLE.bg.dark, align: "center", valign: "middle", bold: true, margin: 0,
    });

    // Step content
    addCard(slide, x, 2.5, stepW, 2.4);

    const textX = x + (STYLE.card.accentBar ? STYLE.card.accentBar.w + 0.15 : 0.15);
    const textW = stepW - (STYLE.card.accentBar ? STYLE.card.accentBar.w + 0.3 : 0.3);

    slide.addText(step.title, {
      x: textX, y: 2.65, w: textW, h: 0.4,
      fontSize: 14, fontFace: STYLE.fonts.body,
      color: STYLE.text.onDark, bold: true, margin: 0,
    });
    slide.addText(step.desc, {
      x: textX, y: 3.05, w: textW, h: 1.5,
      fontSize: 11, fontFace: STYLE.fonts.body,
      color: STYLE.text.secondary, margin: 0,
    });
  });

  return slide;
}
```

---

### Layout: Quote / Highlight

```javascript
function quoteSlide(pres, { quote, attribution, bgImagePath }) {
  const slide = pres.addSlide();

  if (bgImagePath) {
    slide.addImage({
      path: bgImagePath,
      x: 0, y: 0, w: 10, h: 5.625,
      sizing: { type: "cover", w: 10, h: 5.625 },
    });
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 10, h: 5.625,
      fill: { color: STYLE.bg.dark, transparency: 60 },
    });
  } else {
    slide.background = { color: STYLE.bg.dark };
  }

  // Large opening quote mark
  slide.addText("\u201C", {
    x: 1, y: 0.8, w: 1, h: 1.2,
    fontSize: 100, fontFace: STYLE.fonts.header,
    color: STYLE.text.accent, margin: 0,
  });

  // Quote text
  slide.addText(quote, {
    x: 1.5, y: 1.6, w: 7, h: 2.0,
    fontSize: 24, fontFace: STYLE.fonts.header,
    color: STYLE.text.onDark, italic: true, margin: 0,
  });

  // Attribution
  if (attribution) {
    // Thin accent line
    slide.addShape(pres.shapes.LINE, {
      x: 1.5, y: 3.9, w: 1.5, h: 0,
      line: { color: STYLE.text.accent, width: 1 },
    });
    slide.addText(attribution, {
      x: 1.5, y: 4.1, w: 7, h: 0.5,
      fontSize: 14, fontFace: STYLE.fonts.body,
      color: STYLE.text.secondary, margin: 0,
    });
  }

  return slide;
}
```

---

## Usage Example

Putting it all together:

```javascript
const pptxgen = require("pptxgenjs");
const { FaRocket, FaChartLine, FaUsers } = require("react-icons/fa");

// 1. Pick your style
const STYLE = { /* paste a config from above */ };

// 2. Init presentation
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

// 3. Generate icons in style colors
const icons = {
  rocket: await iconToBase64Png(FaRocket, "#" + STYLE.text.accent),
  chart: await iconToBase64Png(FaChartLine, "#" + STYLE.text.accent),
  users: await iconToBase64Png(FaUsers, "#" + STYLE.text.accent),
};

// 4. Build slides using layout functions
titleSlide(pres, {
  title: "YOUR TITLE HERE",
  subtitle: "Subtitle or tagline",
  bgImagePath: "/path/to/generated/bg.png",
  date: "March 2026",
});

statSlide(pres, {
  label: "Key Metrics",
  title: "Performance at a Glance",
  stats: [
    { value: "98.7%", label: "Uptime", icon: icons.rocket },
    { value: "2.4M", label: "Users", icon: icons.users },
    { value: "+47%", label: "Growth", icon: icons.chart },
  ],
});

twoColumnSlide(pres, {
  label: "Overview",
  title: "Platform Features",
  bullets: [
    { icon: icons.rocket, text: "Real-time processing" },
    { icon: icons.chart, text: "ML-powered analytics" },
  ],
  imagePath: "/path/to/illustration.png",
});

conclusionSlide(pres, {
  title: "READY TO START?",
  subtitle: "Let's build something great.",
  contact: { email: "hello@example.com", url: "www.example.com" },
  bgImagePath: "/path/to/bg.png",
});

// 5. Save
await pres.writeFile({ fileName: "output.pptx" });
```

---

## Light-Background Styles

For styles where `bg.light` is white/cream (Academic, Pure Minimal, Botanical, Nordic Research, Swiss, etc.), the layout functions above use `bg.dark` for title/conclusion slides and `bg.medium` or `bg.light` for content slides. The `text.onDark` and `text.onLight` colors automatically handle contrast.

**Key differences for light styles:**
- Stat/grid slides may use `bg.light` instead of `bg.dark` — override `slide.background` as needed
- Cards use borders more than shadows for definition
- Icon circle backgrounds use `STYLE.bg.medium` or a tinted light color
- Full-bleed images still get overlays, but use the style's dark color

When building a light-style deck, swap `slide.background = { color: STYLE.bg.dark }` to `STYLE.bg.light` for content slides and keep `STYLE.bg.dark` for title/conclusion only.
