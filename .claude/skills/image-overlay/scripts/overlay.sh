#!/usr/bin/env bash
# Image Text Overlay Script
# Generates an HTML page with the image + styled text overlay + the workspace logo,
# then screenshots it with Playwright to produce the final PNG.
#
# Output: Saves as {basename}-final.png next to the source image by default.
#
# Usage:
#   bash tools/scripts/sh/image-overlay/overlay.sh \
#     --image "path/to/images/post-image.png" \
#     --text "Your overlay text." \
#     [--subtext "Secondary text."] \
#     [--position "bottom-left"] \
#     [--subposition "bottom-right"] \
#     [--fontsize 72] \
#     [--logo-variant "white"|"primary"|"none"] \
#     [--output "path/to/output.png"]
#
# Logo-only mode (for infographics and data visualizations that already
# carry their own typography):
#   bash tools/scripts/sh/image-overlay/overlay.sh \
#     --image "path/to/infographic.png" \
#     --logo-only \
#     [--output "path/to/output.png"]
# In logo-only mode, --text is not required. The script skips all text
# rendering and only stamps the the workspace logo (variant auto-selected by
# WCAG contrast analysis against the logo region).

set -euo pipefail

# Resolve script directory and project root for finding logo assets
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
# The brand kit owns brand assets. Override either path to point elsewhere.
BRAND_LOGOS="${BRAND_LOGOS_DIR:-$PROJECT_ROOT/.claude/skills/get-brand-kit/assets/logos}"
LOGO_WHITE="${BRAND_LOGO_WHITE:-$BRAND_LOGOS/logo-white.svg}"
LOGO_PRIMARY="${BRAND_LOGO_PRIMARY:-$BRAND_LOGOS/logo-primary.svg}"

# --- Parse arguments ---
IMAGE=""
TEXT=""
SUBTEXT=""
POSITION="bottom-left"
SUBPOSITION="bottom-right"
FONTSIZE=""
LOGO_VARIANT="auto"
LOGO_ONLY="false"
OUTPUT=""
IMG_WIDTH=""
IMG_HEIGHT=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --image) IMAGE="$2"; shift 2 ;;
    --text) TEXT="$2"; shift 2 ;;
    --subtext) SUBTEXT="$2"; shift 2 ;;
    --position) POSITION="$2"; shift 2 ;;
    --subposition) SUBPOSITION="$2"; shift 2 ;;
    --fontsize) FONTSIZE="$2"; shift 2 ;;
    --logo-variant) LOGO_VARIANT="$2"; shift 2 ;;
    --logo-only) LOGO_ONLY="true"; shift 1 ;;
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

if [[ "$LOGO_ONLY" != "true" && -z "$TEXT" ]]; then
  echo "Error: --text is required (or pass --logo-only for logo-only mode)"
  exit 1
fi

# Default output: {basename}-final.png next to source image
if [[ -z "$OUTPUT" ]]; then
  IMAGE_DIR=$(dirname "$IMAGE")
  IMAGE_BASE=$(basename "$IMAGE" .png)
  OUTPUT="${IMAGE_DIR}/${IMAGE_BASE}-final.png"
fi

# Find Python with Pillow — required for contrast analysis and image dimensions
PYTHON_CMD=""
# Pillow is the one dependency. Prefer an explicit venv, then a project-local
# one, then the system interpreter. IMGTOOLS_VENV overrides the location.
IMGTOOLS="${IMGTOOLS_VENV:-$PROJECT_ROOT/.scratchpad/imgtools}"
if [[ -x "$IMGTOOLS/bin/python3" ]] && "$IMGTOOLS/bin/python3" -c "from PIL import Image" 2>/dev/null; then
  PYTHON_CMD="$IMGTOOLS/bin/python3"
elif python3 -c "from PIL import Image" 2>/dev/null; then
  PYTHON_CMD="python3"
else
  echo "ERROR: Pillow is not installed." >&2
  echo "  python3 -m venv \"$IMGTOOLS\" && \"$IMGTOOLS/bin/pip\" install Pillow" >&2
  exit 1
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

# --- Contrast analysis using WCAG relative luminance ---
# Uses proper contrast ratio calculations for both logo and text regions.
# Logo region matches actual logo footprint (22% width, top 3% to ~10%) with padding.
# Text region matches the position parameter.
CONTRAST_RESULT=$(LOGO_WHITE_PATH="$LOGO_WHITE" LOGO_PRIMARY_PATH="$LOGO_PRIMARY" $PYTHON_CMD -c "
from PIL import Image
import math, os, re

img = Image.open('$IMAGE').convert('RGB')
w, h = img.size

def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def relative_luminance(r, g, b):
    return 0.2126 * srgb_to_linear(r) + 0.7152 * srgb_to_linear(g) + 0.0722 * srgb_to_linear(b)

def avg_luminance(region):
    pixels = list(region.getdata()) if hasattr(region, 'getdata') else list(region.convert('RGB').getdata())
    return sum(relative_luminance(*p) for p in pixels) / len(pixels)

def contrast_ratio(l1, l2):
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def svg_luminance(path, fallback):
    '''Mean relative luminance of the fills in an SVG.

    Reading it from the file is what makes the brand swappable: the hardcoded
    constants this replaces were derived from one brand's hexes, so replacing
    the logos would have silently inverted variant selection while every check
    still passed.
    '''
    try:
        with open(path, encoding='utf-8') as fh:
            body = fh.read()
    except OSError:
        return fallback
    hexes = re.findall(r'#([0-9a-fA-F]{6})\b', body)
    if not hexes:
        return fallback
    lums = [relative_luminance(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            for h in hexes]
    return sum(lums) / len(lums)

# Logo region: matches CSS position (top: 3%, right: 3%, width: 22%)
# Add 2% padding on all sides for safety
logo_x1 = int(w * 0.73)   # 3% from right = 97% - 22% width = 75%, minus 2% pad
logo_y1 = int(h * 0.01)   # 3% from top minus 2% pad
logo_x2 = min(w, int(w * 0.99))   # right edge + 2% pad
logo_y2 = int(h * 0.14)   # ~10% logo height + 2% pad below
logo_region = img.crop((logo_x1, logo_y1, logo_x2, logo_y2))
bg_luminance = avg_luminance(logo_region)

# Derived from the fills in the SVGs actually being composited, so swapping the
# brand's logos cannot silently invert variant selection. Overridable for a mark
# whose dominant fill is not its first.
white_logo_lum = float(os.environ.get("BRAND_LOGO_WHITE_LUMINANCE") or svg_luminance(os.environ["LOGO_WHITE_PATH"], 0.95))
primary_logo_lum = float(os.environ.get("BRAND_LOGO_PRIMARY_LUMINANCE") or svg_luminance(os.environ["LOGO_PRIMARY_PATH"], 0.20))

white_contrast = contrast_ratio(white_logo_lum, bg_luminance)
primary_contrast = contrast_ratio(primary_logo_lum, bg_luminance)

# Pick whichever gives better contrast (WCAG AA minimum is 4.5:1)
logo_var = 'white' if white_contrast >= primary_contrast else 'primary'
best_contrast = max(white_contrast, primary_contrast)

# Text region brightness depends on position
pos = '$POSITION'
if 'top' in pos:
    ty1, ty2 = 0, int(h * 0.30)
elif 'center' in pos and 'top' not in pos and 'bottom' not in pos:
    ty1, ty2 = int(h * 0.35), int(h * 0.65)
else:  # bottom
    ty1, ty2 = int(h * 0.65), h

if 'left' in pos:
    tx1, tx2 = 0, int(w * 0.65)
elif 'right' in pos:
    tx1, tx2 = int(w * 0.35), w
else:  # center
    tx1, tx2 = int(w * 0.10), int(w * 0.90)

text_region = img.crop((tx1, ty1, tx2, ty2))
text_bg_lum = avg_luminance(text_region)
white_text_lum = 0.95
text_contrast = contrast_ratio(white_text_lum, text_bg_lum)

# If white text contrast < 3:1 against the text region, add enhanced shadow
needs_backdrop = 'true' if text_contrast < 3.0 else 'false'

print(f'{logo_var} {needs_backdrop} {text_contrast:.1f} {best_contrast:.1f}')
"
)

if [[ -z "$CONTRAST_RESULT" ]]; then
  echo "ERROR: Contrast analysis failed. Check that Pillow is installed and the image is valid."
  exit 1
fi

DETECTED_LOGO=$(echo "$CONTRAST_RESULT" | cut -d' ' -f1)
TEXT_NEEDS_BACKDROP=$(echo "$CONTRAST_RESULT" | cut -d' ' -f2)
TEXT_CONTRAST=$(echo "$CONTRAST_RESULT" | cut -d' ' -f3)
LOGO_CONTRAST=$(echo "$CONTRAST_RESULT" | cut -d' ' -f4)

DETECTED_LOGO=$(echo "$CONTRAST_RESULT" | cut -d' ' -f1)
TEXT_NEEDS_BACKDROP=$(echo "$CONTRAST_RESULT" | cut -d' ' -f2)
TEXT_BRIGHTNESS=$(echo "$CONTRAST_RESULT" | cut -d' ' -f3)

# Always use the WCAG-calculated variant. Agent overrides are ignored.
# The algorithm picks whichever logo (white or primary) has the highest
# contrast ratio against the actual logo region of this specific image.
LOGO_VARIANT="$DETECTED_LOGO"

# Auto-calculate font size if not provided (bumped up from previous version)
if [[ -z "$FONTSIZE" ]]; then
  if [[ "$LOGO_ONLY" == "true" ]]; then
    FONTSIZE=52
  else
    TEXT_LEN=${#TEXT}
    if [[ $TEXT_LEN -le 10 ]]; then
      FONTSIZE=140
    elif [[ $TEXT_LEN -le 20 ]]; then
      FONTSIZE=110
    elif [[ $TEXT_LEN -le 35 ]]; then
      FONTSIZE=84
    elif [[ $TEXT_LEN -le 55 ]]; then
      FONTSIZE=68
    else
      FONTSIZE=52
    fi
  fi
fi

# Calculate subtext font size (roughly 50% of main)
SUB_FONTSIZE=$((FONTSIZE * 50 / 100))
if [[ $SUB_FONTSIZE -lt 28 ]]; then
  SUB_FONTSIZE=28
fi

# Convert image to absolute path
ABS_IMAGE=$(cd "$(dirname "$IMAGE")" && pwd)/$(basename "$IMAGE")

# --- Text shadow CSS based on contrast ---
# If the text region is bright, add a stronger shadow/backdrop for legibility
if [[ "$TEXT_NEEDS_BACKDROP" == "true" ]]; then
  TEXT_SHADOW="text-shadow: 1px 1px 4px rgba(0,0,0,0.9), 0 0 20px rgba(0,0,0,0.7), 0 0 60px rgba(0,0,0,0.5);"
  echo "Text contrast ${TEXT_CONTRAST}:1 (below 3:1) -> enhanced shadow for legibility"
else
  TEXT_SHADOW="text-shadow: 2px 2px 8px rgba(0,0,0,0.7);"
  echo "Text contrast ${TEXT_CONTRAST}:1 (above 3:1) -> standard shadow"
fi

# --- Map position to CSS ---
position_to_css() {
  local pos=$1
  local font=$2
  case $pos in
    top-left)      echo "top: 5%; left: 5%; text-align: left; font-size: ${font}px;" ;;
    top-center)    echo "top: 5%; left: 50%; transform: translateX(-50%); text-align: center; font-size: ${font}px;" ;;
    top-right)     echo "top: 5%; right: 5%; text-align: right; font-size: ${font}px;" ;;
    center)        echo "top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; font-size: ${font}px;" ;;
    bottom-left)   echo "bottom: 5%; left: 5%; text-align: left; font-size: ${font}px;" ;;
    bottom-center) echo "bottom: 5%; left: 50%; transform: translateX(-50%); text-align: center; font-size: ${font}px;" ;;
    bottom-right)  echo "bottom: 5%; right: 5%; text-align: right; font-size: ${font}px;" ;;
    *)             echo "bottom: 5%; left: 5%; text-align: left; font-size: ${font}px;" ;;
  esac
}

MAIN_CSS=$(position_to_css "$POSITION" "$FONTSIZE")
SUB_CSS=$(position_to_css "$SUBPOSITION" "$SUB_FONTSIZE")

# Logo HTML — inline SVG, scaled to 180px wide for visibility
LOGO_HTML=""
if [[ "$LOGO_VARIANT" != "none" ]]; then
  LOGO_FILE="$LOGO_WHITE"
  if [[ "$LOGO_VARIANT" == "primary" ]]; then
    LOGO_FILE="$LOGO_PRIMARY"
  fi
  if [[ -f "$LOGO_FILE" ]]; then
    SVG_CONTENT=$(cat "$LOGO_FILE")
    LOGO_HTML="<div style=\"position: absolute; top: 3%; right: 3%; width: 22%; min-width: 300px; opacity: 0.92; filter: drop-shadow(0 1px 4px rgba(0,0,0,0.3));\">${SVG_CONTENT}</div>"
  fi
fi

# Main text HTML (skipped entirely in logo-only mode)
MAIN_TEXT_HTML=""
if [[ "$LOGO_ONLY" != "true" ]]; then
  MAIN_TEXT_HTML="<div class=\"overlay-text main\" style=\"${MAIN_CSS}\">${TEXT}</div>"
fi

# Subtext HTML (skipped in logo-only mode, and when no subtext provided)
SUBTEXT_HTML=""
if [[ "$LOGO_ONLY" != "true" && -n "$SUBTEXT" ]]; then
  SUBTEXT_HTML="<div class=\"overlay-text subtext\" style=\"${SUB_CSS}\">${SUBTEXT}</div>"
fi

# --- Generate HTML ---
TMPHTML=$(mktemp /tmp/overlay-XXXXXX.html)

cat > "$TMPHTML" << HTMLEOF
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@900&display=swap" rel="stylesheet">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: ${IMG_WIDTH}px;
    height: ${IMG_HEIGHT}px;
    overflow: hidden;
    font-family: 'Roboto', sans-serif;
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
  .overlay-text {
    position: absolute;
    color: #FFFFFF;
    font-family: 'Roboto', sans-serif;
    font-weight: 900;
    max-width: 90%;
    line-height: 1.08;
    ${TEXT_SHADOW}
    letter-spacing: -0.02em;
  }
  .overlay-text.subtext {
    font-weight: 900;
    opacity: 0.92;
    line-height: 1.15;
    letter-spacing: 0;
  }
  div svg { width: 100%; height: auto; }
</style>
</head>
<body>
<div class="container">
  <img class="bg" src="file://${ABS_IMAGE}" />
  ${MAIN_TEXT_HTML}
  ${SUBTEXT_HTML}
  ${LOGO_HTML}
</div>
</body>
</html>
HTMLEOF

echo "Image: $(basename "$ABS_IMAGE") (${IMG_WIDTH}x${IMG_HEIGHT})"
if [[ "$LOGO_ONLY" == "true" ]]; then
  echo "Mode: logo-only (no text overlay)"
  echo "Logo: ${LOGO_VARIANT} (contrast: ${LOGO_CONTRAST}:1)"
else
  echo "Text: ${TEXT} | Font: ${FONTSIZE}px | Position: ${POSITION}"
  if [[ -n "$SUBTEXT" ]]; then
    echo "Subtext: ${SUBTEXT} | Font: ${SUB_FONTSIZE}px | Position: ${SUBPOSITION}"
  fi
  echo "Logo: ${LOGO_VARIANT} (contrast: ${LOGO_CONTRAST}:1) | Text contrast: ${TEXT_CONTRAST}:1 | Enhanced shadow: ${TEXT_NEEDS_BACKDROP}"
fi

# --- Screenshot with Playwright ---
echo "Rendering..."
npx playwright screenshot \
  --viewport-size="${IMG_WIDTH},${IMG_HEIGHT}" \
  --wait-for-timeout 2000 \
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
