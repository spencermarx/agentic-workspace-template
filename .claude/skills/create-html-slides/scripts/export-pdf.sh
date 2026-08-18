#!/usr/bin/env bash
# =============================================================================
# export-pdf.sh — Export an HTML slide deck to PDF via Playwright
#
# Captures each slide as a screenshot at 1920x1080 (16:9, Google Slides
# compatible) and assembles them into a multi-page PDF.
#
# Usage:
#   bash tools/scripts/sh/create-html-slides/export-pdf.sh \
#     --input path/to/deck.html \
#     --output path/to/deck.pdf \
#     --width 1920 \
#     --height 1080
#
# Requirements: Node.js (v18+), npx, Playwright (`npx playwright install chromium`)
# =============================================================================
set -euo pipefail

# --- Defaults ---
INPUT=""
OUTPUT=""
WIDTH=1920
HEIGHT=1080

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --input)  INPUT="$2";  shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --width)  WIDTH="$2";  shift 2 ;;
    --height) HEIGHT="$2"; shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$INPUT" ]]; then
  echo "Error: --input is required" >&2
  exit 1
fi

if [[ ! -f "$INPUT" ]]; then
  echo "Error: Input file not found: $INPUT" >&2
  exit 1
fi

# Resolve absolute path for file:// URL
INPUT_ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"

# Default output: same name with .pdf extension
if [[ -z "$OUTPUT" ]]; then
  OUTPUT="${INPUT_ABS%.html}.pdf"
fi

echo "Exporting slide deck to PDF..." >&2
echo "  Input:  $INPUT_ABS" >&2
echo "  Output: $OUTPUT" >&2
echo "  Viewport: ${WIDTH}x${HEIGHT}" >&2

# --- Locate Playwright's parent node_modules from npx cache ---
PW_PKG=$(find ~/.npm/_npx -path "*/node_modules/playwright/package.json" -print -quit 2>/dev/null || true)

if [[ -z "$PW_PKG" ]]; then
  echo "Playwright not found in npx cache. Installing..." >&2
  npx --yes playwright install chromium > /dev/null 2>&1
  PW_PKG=$(find ~/.npm/_npx -path "*/node_modules/playwright/package.json" -print -quit 2>/dev/null || true)
fi

if [[ -z "$PW_PKG" ]]; then
  echo "Error: Could not locate Playwright module after install." >&2
  exit 1
fi

# The script must run from a directory where `node_modules/playwright` is resolvable.
# npx cache structure: ~/.npm/_npx/<hash>/node_modules/playwright/
# So we cd to ~/.npm/_npx/<hash>/ and run from there.
PW_NM="$(dirname "$(dirname "$PW_PKG")")"  # .../node_modules
PW_ROOT="$(dirname "$PW_NM")"               # .../<hash>/
echo "  Playwright: $PW_ROOT" >&2

# --- Write the capture script to a temp file ---
SCRIPT="$(mktemp /tmp/pw-export-XXXXXX.mjs)"
trap 'rm -f "$SCRIPT"' EXIT

cat > "$SCRIPT" << 'SCRIPT_EOF'
import { chromium } from 'playwright';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';

const [inputUrl, outputPath, w, h] = process.argv.slice(2);
const width = parseInt(w);
const height = parseInt(h);

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width, height });
  await page.goto(inputUrl, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);

  // Detect slides — try both class conventions
  const slideCount = await page.evaluate(() => {
    const s = document.querySelectorAll('.s');
    return s.length > 0 ? s.length : document.querySelectorAll('.slide').length;
  });

  if (slideCount === 0) {
    console.error('No slides found (looked for .s and .slide classes)');
    process.exit(1);
  }
  console.log(`Found ${slideCount} slides`);

  // Hide nav chrome (both conventions)
  await page.evaluate(() => {
    document.querySelectorAll('.prog, .progress-bar, .dots, .nav-dots')
      .forEach(el => el.style.display = 'none');
  });

  // Screenshot each slide
  const tmpDir = dirname(outputPath);
  const screenshots = [];
  for (let i = 0; i < slideCount; i++) {
    await page.evaluate((idx) => {
      let slides = document.querySelectorAll('.s');
      if (slides.length === 0) slides = document.querySelectorAll('.slide');
      slides[idx].scrollIntoView({ behavior: 'instant' });
      slides[idx].classList.add('vis');
      slides[idx].classList.add('visible');
    }, i);

    await page.waitForTimeout(800);
    const path = `/tmp/pw-slide-${String(i).padStart(3, '0')}.png`;
    await page.screenshot({ path, type: 'png' });
    screenshots.push(path);
    console.log(`  Captured slide ${i + 1}/${slideCount}`);
  }

  // Assemble PDF
  const pdfPage = await browser.newPage();
  await pdfPage.setViewportSize({ width, height });

  const slideImages = screenshots.map(p =>
    `data:image/png;base64,${readFileSync(p).toString('base64')}`
  );

  await pdfPage.setContent(`<!DOCTYPE html>
<html><head><style>
  * { margin: 0; padding: 0; }
  @page { size: ${width}px ${height}px; margin: 0; }
  .page { width: ${width}px; height: ${height}px; page-break-after: always; overflow: hidden; }
  .page:last-child { page-break-after: auto; }
  .page img { width: 100%; height: 100%; object-fit: contain; }
</style></head><body>
  ${slideImages.map(src => `<div class="page"><img src="${src}" /></div>`).join('\n  ')}
</body></html>`, { waitUntil: 'load' });

  await pdfPage.waitForTimeout(500);
  await pdfPage.pdf({
    path: outputPath,
    width: `${width}px`,
    height: `${height}px`,
    printBackground: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 }
  });

  // Cleanup temp screenshots
  screenshots.forEach(p => { try { require('fs').unlinkSync(p); } catch {} });

  console.log(`PDF saved to: ${outputPath}`);
  await browser.close();
})();
SCRIPT_EOF

# --- Copy script into the Playwright cache root so imports resolve naturally ---
cp "$SCRIPT" "$PW_ROOT/pw-export.mjs"
node "$PW_ROOT/pw-export.mjs" \
  "file://$INPUT_ABS" \
  "$OUTPUT" \
  "$WIDTH" \
  "$HEIGHT"
rm -f "$PW_ROOT/pw-export.mjs"

echo "Done. PDF exported to: $OUTPUT"
