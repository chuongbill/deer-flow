/**
 * crop_image.js — Crop/resize images to target aspect ratios for slide placement.
 *
 * The built-in generate_image tool always outputs square (1024x1024) images.
 * This script center-crops them to standard presentation ratios so they
 * don't get stretched or badly cropped when placed in slides.
 *
 * Usage (CLI):
 *   node crop_image.js <input> <output> <ratio>
 *   node crop_image.js bg.png bg_wide.png 16:9
 *   node crop_image.js photo.png photo_portrait.png 3:4
 *
 * Usage (require):
 *   const { cropToRatio } = require("./crop_image");
 *   await cropToRatio("bg.png", "bg_wide.png", 16, 9);
 */

const sharp = require("sharp");
const path = require("path");

/**
 * Center-crop an image to a target aspect ratio.
 *
 * @param {string} inputPath  — Absolute path to source image
 * @param {string} outputPath — Absolute path for cropped output
 * @param {number} ratioW     — Target width ratio (e.g. 16)
 * @param {number} ratioH     — Target height ratio (e.g. 9)
 * @returns {Promise<{w: number, h: number, path: string}>}
 */
async function cropToRatio(inputPath, outputPath, ratioW, ratioH) {
  const meta = await sharp(inputPath).metadata();
  const srcW = meta.width;
  const srcH = meta.height;
  const targetRatio = ratioW / ratioH;
  const srcRatio = srcW / srcH;

  let cropW, cropH;
  if (srcRatio > targetRatio) {
    // Source is wider than target — crop sides
    cropH = srcH;
    cropW = Math.round(srcH * targetRatio);
  } else {
    // Source is taller than target — crop top/bottom
    cropW = srcW;
    cropH = Math.round(srcW / targetRatio);
  }

  // Center the crop region
  const left = Math.round((srcW - cropW) / 2);
  const top = Math.round((srcH - cropH) / 2);

  await sharp(inputPath)
    .extract({ left, top, width: cropW, height: cropH })
    .toFile(outputPath);

  console.log(
    `Cropped ${path.basename(inputPath)} (${srcW}x${srcH}) → ` +
    `${path.basename(outputPath)} (${cropW}x${cropH}) [${ratioW}:${ratioH}]`
  );

  return { w: cropW, h: cropH, path: outputPath };
}

/**
 * Batch crop multiple images.
 *
 * @param {Array<{input: string, output: string, ratio: [number, number]}>} jobs
 * @returns {Promise<Array<{w: number, h: number, path: string}>>}
 */
async function cropBatch(jobs) {
  return Promise.all(
    jobs.map((j) => cropToRatio(j.input, j.output, j.ratio[0], j.ratio[1]))
  );
}

// ── CLI mode ────────────────────────────────────────────────
if (require.main === module) {
  const [, , input, output, ratio] = process.argv;
  if (!input || !output || !ratio) {
    console.log("Usage: node crop_image.js <input> <output> <ratio>");
    console.log("  ratio: 16:9, 4:3, 3:4, 1:1, etc.");
    process.exit(1);
  }
  const [rw, rh] = ratio.split(":").map(Number);
  cropToRatio(input, output, rw, rh).catch((err) => {
    console.error(err);
    process.exit(1);
  });
}

module.exports = { cropToRatio, cropBatch };
