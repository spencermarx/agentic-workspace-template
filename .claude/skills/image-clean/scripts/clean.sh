#!/usr/bin/env bash
# Blog Image Cleaner
# Strips AI metadata (EXIF, C2PA provenance) by rendering through Playwright.
# Takes an AI-generated image, renders it in a minimal HTML page, and screenshots
# it to produce a "born clean" PNG with no embedded metadata.
#
# Output: Saves as {basename}-clean.png next to the source image by default.
#
# Usage:
#   bash ${CLAUDE_SKILL_DIR}/scripts/clean.sh \
#     --image "path/to/images/post-image.png" \
#     [--output "path/to/clean.png"] \
#     [--width 1536] \
#     [--height 1024]

set -euo pipefail

# --- Parse arguments ---
IMAGE=""
OUTPUT=""
IMG_WIDTH=""
IMG_HEIGHT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --image) IMAGE="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --width) IMG_WIDTH="$2"; shift 2 ;;
    --height) IMG_HEIGHT="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$IMAGE" ]]; then
  echo "Error: --image is required"
  exit 1
fi

# Default output: {basename}-clean.png next to source image
if [[ -z "$OUTPUT" ]]; then
  IMAGE_DIR=$(dirname "$IMAGE")
  IMAGE_BASE=$(basename "$IMAGE" .png)
  OUTPUT="${IMAGE_DIR}/${IMAGE_BASE}-clean.png"
fi

# Find Python with Pillow
PYTHON_CMD="python3"
if [[ -f /tmp/imgtools/bin/python3 ]]; then
  PYTHON_CMD="/tmp/imgtools/bin/python3"
fi

# Get image dimensions
if [[ -z "$IMG_WIDTH" || -z "$IMG_HEIGHT" ]]; then
  DIMS=$($PYTHON_CMD -c "
from PIL import Image
img = Image.open('$IMAGE')
print(f'{img.width} {img.height}')
" 2>/dev/null || echo "1536 1024")
  IMG_WIDTH=$(echo "$DIMS" | cut -d' ' -f1)
  IMG_HEIGHT=$(echo "$DIMS" | cut -d' ' -f2)
fi

# Convert image to absolute path
ABS_IMAGE=$(cd "$(dirname "$IMAGE")" && pwd)/$(basename "$IMAGE")

# --- Generate minimal HTML ---
TMPHTML=$(mktemp /tmp/clean-XXXXXX.html)

cat > "$TMPHTML" << HTMLEOF
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: ${IMG_WIDTH}px;
    height: ${IMG_HEIGHT}px;
    overflow: hidden;
  }
  .container {
    position: relative;
    width: ${IMG_WIDTH}px;
    height: ${IMG_HEIGHT}px;
  }
  .container img.bg {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }
</style>
</head>
<body>
<div class="container">
  <img class="bg" src="file://${ABS_IMAGE}" />
</div>
</body>
</html>
HTMLEOF

echo "Image: $(basename "$ABS_IMAGE") (${IMG_WIDTH}x${IMG_HEIGHT})"
echo "Cleaning metadata via Playwright screenshot..."

# --- Screenshot with Playwright ---
npx playwright screenshot \
  --viewport-size="${IMG_WIDTH},${IMG_HEIGHT}" \
  --wait-for-timeout 1000 \
  --full-page \
  "file://${TMPHTML}" \
  "$OUTPUT" 2>&1

# Crop to exact dimensions if needed
$PYTHON_CMD -c "
from PIL import Image
img = Image.open('$OUTPUT')
if img.size != ($IMG_WIDTH, $IMG_HEIGHT):
    img = img.crop((0, 0, $IMG_WIDTH, $IMG_HEIGHT))
    img.save('$OUTPUT', quality=95)
    print(f'Cropped to ${IMG_WIDTH}x${IMG_HEIGHT}')
else:
    print('Dimensions correct')
" 2>/dev/null

rm -f "$TMPHTML"
echo "Done: $OUTPUT"
