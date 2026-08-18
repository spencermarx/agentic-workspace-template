#!/usr/bin/env node
// Lean, browser-free Excalidraw compiler.
//
// Input: a small declarative diagram spec (nodes / edges / texts / regions)
// authored by the agent. Output: an Obsidian-native `.excalidraw.md` file
// (and optionally a plain `.excalidraw`) with real bound arrows and bound
// text labels — the editability guarantees — without ever loading a browser.
//
// The one thing @excalidraw/excalidraw's `convertToExcalidrawElements` does
// that we reimplement here: expand each labelled shape into a shape + a bound
// text element, and each edge into an arrow with startBinding/endBinding and
// computed points. Excalidraw's own `restore()` (run by the Obsidian plugin
// on open) fills every field we omit (fractional index, normalized defaults),
// so we emit the minimal-but-complete element objects and let it normalize.
//
// Usage:
//   node build.mjs --spec path/to/spec.json --out path/to/diagram.excalidraw.md
//   node build.mjs --spec spec.json --out diagram.excalidraw.md --plain   # also write .excalidraw
//
// No dependencies. Node >= 18.

import fs from "node:fs";
import path from "node:path";

// ---------------------------------------------------------------------------
// args
// ---------------------------------------------------------------------------
function parseArgs(argv) {
  const a = { plain: false };
  for (let i = 2; i < argv.length; i++) {
    const t = argv[i];
    if (t === "--spec") a.spec = argv[++i];
    else if (t === "--out") a.out = argv[++i];
    else if (t === "--plain") a.plain = true;
    else if (t === "--stdin") a.stdin = true;
  }
  return a;
}

// ---------------------------------------------------------------------------
// deterministic ids + seeds (stable git diffs across reruns)
// ---------------------------------------------------------------------------
function mulberry32(seed) {
  let s = seed >>> 0;
  return function () {
    s |= 0;
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function hashStr(str) {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}
const ID_CHARS =
  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_";
function makeGen(seedStr) {
  const rnd = mulberry32(hashStr(seedStr));
  const seen = new Set();
  return {
    id() {
      let out;
      do {
        out = "";
        for (let i = 0; i < 9; i++)
          out += ID_CHARS[Math.floor(rnd() * ID_CHARS.length)];
      } while (seen.has(out));
      seen.add(out);
      return out;
    },
    int() {
      return Math.floor(rnd() * 2 ** 31);
    },
  };
}

// ---------------------------------------------------------------------------
// fonts + colors
// ---------------------------------------------------------------------------
const FONT = { hand: 5, normal: 2, code: 3 }; // Excalidraw fontFamily codes

// Relative luminance → pick a readable label color for a filled shape.
function bestLabelColor(bg) {
  if (!bg || bg === "transparent") return null;
  const hex = bg.replace("#", "");
  if (hex.length < 6) return null;
  const r = parseInt(hex.slice(0, 2), 16) / 255;
  const g = parseInt(hex.slice(2, 4), 16) / 255;
  const b = parseInt(hex.slice(4, 6), 16) / 255;
  const lin = (c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  const L = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
  return L > 0.5 ? "#1e1e1e" : "#ffffff";
}

// ---------------------------------------------------------------------------
// text metrics (Excalifont ~0.5em/char; lineHeight 1.25)
// ---------------------------------------------------------------------------
const CHAR_W = 0.5;
const LINE_H = 1.25;
function textSize(text, fontSize) {
  const lines = String(text).split("\n");
  const longest = lines.reduce((m, l) => Math.max(m, l.length), 0);
  return {
    width: Math.max(10, Math.round(longest * fontSize * CHAR_W)),
    height: Math.round(lines.length * fontSize * LINE_H),
  };
}

// ---------------------------------------------------------------------------
// element factory — full element with every field the schema wants
// ---------------------------------------------------------------------------
function baseEl(gen, type, o) {
  return {
    id: o.id ?? gen.id(),
    type,
    x: o.x,
    y: o.y,
    width: o.width,
    height: o.height,
    angle: 0,
    strokeColor: o.strokeColor ?? "#1e1e1e",
    backgroundColor: o.backgroundColor ?? "transparent",
    fillStyle: o.fillStyle ?? "solid",
    strokeWidth: o.strokeWidth ?? 2,
    strokeStyle: o.strokeStyle ?? "solid",
    roughness: o.roughness ?? 1,
    opacity: o.opacity ?? 100,
    groupIds: o.groupIds ?? [],
    frameId: null,
    roundness: o.roundness ?? null,
    seed: gen.int(),
    version: 1,
    versionNonce: gen.int(),
    isDeleted: false,
    boundElements: o.boundElements ?? [],
    updated: 1,
    link: null,
    locked: false,
    hasTextLink: false,
  };
}

// clip a segment from a shape center toward a target, to the shape edge + gap
function clipToEdge(shape, tx, ty, gap) {
  const cx = shape.x + shape.width / 2;
  const cy = shape.y + shape.height / 2;
  const dx = tx - cx;
  const dy = ty - cy;
  if (dx === 0 && dy === 0) return { x: cx, y: cy };
  const w = shape.width / 2;
  const h = shape.height / 2;
  const tHor = dx !== 0 ? (w + gap) / Math.abs(dx) : Infinity;
  const tVer = dy !== 0 ? (h + gap) / Math.abs(dy) : Infinity;
  const t = Math.min(tHor, tVer);
  return { x: cx + dx * t, y: cy + dy * t };
}

// ---------------------------------------------------------------------------
// compile
// ---------------------------------------------------------------------------
function compile(spec) {
  const gen = makeGen(spec.title ?? "excalidraw");
  const fontFamily = FONT[spec.font ?? "hand"] ?? 5;
  const elements = [];
  const byId = new Map(); // node id -> shape element
  const errors = [];

  // 1) regions (behind everything) — a background rect + optional label
  for (const r of spec.regions ?? []) {
    const rect = baseEl(gen, "rectangle", {
      x: r.x,
      y: r.y,
      width: r.w,
      height: r.h,
      backgroundColor: r.bg ?? "#f1f3f5",
      fillStyle: r.fillStyle ?? "solid",
      strokeColor: r.stroke ?? "#adb5bd",
      strokeStyle: r.strokeStyle ?? "solid",
      roundness: { type: 3 },
    });
    elements.push(rect);
    if (r.label) {
      const fs2 = r.fontSize ?? 20;
      const sz = textSize(r.label, fs2);
      const align = r.labelAlign ?? "top-left";
      let tx = r.x + 16;
      let ty = r.y + 12;
      if (align.includes("center")) tx = r.x + (r.w - sz.width) / 2;
      const t = baseEl(gen, "text", {
        x: tx,
        y: ty,
        width: sz.width,
        height: sz.height,
        strokeColor: r.labelColor ?? "#495057",
      });
      Object.assign(t, textProps(r.label, fs2, fontFamily, "left"));
      elements.push(t);
    }
  }

  // 2) nodes (shapes) + bound labels
  for (const n of spec.nodes ?? []) {
    if (n.id == null) {
      errors.push(`node missing id: ${JSON.stringify(n)}`);
      continue;
    }
    if (byId.has(n.id)) errors.push(`duplicate node id: ${n.id}`);
    const shapeType =
      n.shape === "ellipse" || n.shape === "diamond" ? n.shape : "rectangle";
    const shape = baseEl(gen, shapeType, {
      x: n.x,
      y: n.y,
      width: n.w,
      height: n.h,
      backgroundColor: n.bg ?? "transparent",
      strokeColor: n.stroke ?? "#1e1e1e",
      strokeStyle: n.strokeStyle,
      fillStyle: n.fillStyle,
      roughness: n.roughness,
      groupIds: n.group ? [n.group] : [],
      roundness:
        shapeType === "rectangle" && !n.sharp ? { type: 3 } : null,
    });
    shape.customData = { legacyTextWrap: true };
    elements.push(shape);
    byId.set(n.id, shape);

    if (n.label != null && n.label !== "") {
      const fs2 = n.fontSize ?? 16;
      const sz = textSize(n.label, fs2);
      const color = n.labelColor ?? bestLabelColor(n.bg) ?? "#1e1e1e";
      const align = n.align ?? "center"; // left | center | right
      const valign = n.valign ?? "middle"; // top | middle | bottom
      const padX = 10;
      let tx = n.x + (n.w - sz.width) / 2;
      if (align === "left") tx = n.x + padX;
      else if (align === "right") tx = n.x + n.w - sz.width - padX;
      let ty = n.y + (n.h - sz.height) / 2;
      if (valign === "top") ty = n.y + 8;
      else if (valign === "bottom") ty = n.y + n.h - sz.height - 8;
      const t = baseEl(gen, "text", {
        x: tx,
        y: ty,
        width: sz.width,
        height: sz.height,
        strokeColor: color,
      });
      Object.assign(t, textProps(n.label, fs2, fontFamily, align));
      t.containerId = shape.id;
      t.verticalAlign = valign;
      shape.boundElements.push({ type: "text", id: t.id });
      elements.push(t);
    }
  }

  // 3) edges → bound arrows (+ optional bound labels)
  const GAP = 6;
  for (const e of spec.edges ?? []) {
    const a = byId.get(e.from);
    const b = byId.get(e.to);
    if (!a || !b) {
      errors.push(`edge references unknown node(s): ${e.from} -> ${e.to}`);
      continue;
    }
    const acx = a.x + a.width / 2;
    const acy = a.y + a.height / 2;
    const bcx = b.x + b.width / 2;
    const bcy = b.y + b.height / 2;
    const p0 = clipToEdge(a, bcx, bcy, GAP);
    const p1 = clipToEdge(b, acx, acy, GAP);
    const arrow = baseEl(gen, "arrow", {
      x: p0.x,
      y: p0.y,
      width: Math.abs(p1.x - p0.x),
      height: Math.abs(p1.y - p0.y),
      strokeColor: e.stroke ?? "#1e1e1e",
      strokeStyle: e.style ?? "solid",
      roundness: e.curved === false ? null : { type: 2 },
    });
    arrow.points = [
      [0, 0],
      [p1.x - p0.x, p1.y - p0.y],
    ];
    arrow.startBinding = { elementId: a.id, focus: 0, gap: GAP };
    arrow.endBinding = { elementId: b.id, focus: 0, gap: GAP };
    arrow.startArrowhead = e.start ?? null;
    arrow.endArrowhead = e.end === undefined ? "arrow" : e.end;
    arrow.elbowed = false;
    arrow.moveMidPointsWithElement = false;
    a.boundElements.push({ type: "arrow", id: arrow.id });
    b.boundElements.push({ type: "arrow", id: arrow.id });
    elements.push(arrow);

    if (e.label != null && e.label !== "") {
      const fs2 = e.fontSize ?? 14;
      const sz = textSize(e.label, fs2);
      const midx = (p0.x + p1.x) / 2;
      const midy = (p0.y + p1.y) / 2;
      const t = baseEl(gen, "text", {
        x: midx - sz.width / 2,
        y: midy - sz.height / 2,
        width: sz.width,
        height: sz.height,
        strokeColor: e.labelColor ?? "#1e1e1e",
        backgroundColor: "#ffffff",
      });
      Object.assign(t, textProps(e.label, fs2, fontFamily, "center"));
      t.containerId = arrow.id;
      t.verticalAlign = "middle";
      arrow.boundElements.push({ type: "text", id: t.id });
      elements.push(t);
    }
  }

  // 4) free-floating texts (titles, annotations)
  for (const tx of spec.texts ?? []) {
    const fs2 = tx.fontSize ?? 20;
    const sz = textSize(tx.text, fs2);
    const t = baseEl(gen, "text", {
      x: tx.x,
      y: tx.y,
      width: tx.w ?? sz.width,
      height: sz.height,
      strokeColor: tx.stroke ?? "#1e1e1e",
    });
    Object.assign(t, textProps(tx.text, fs2, fontFamily, tx.align ?? "left"));
    elements.push(t);
  }

  if (errors.length) {
    throw new Error("spec errors:\n  - " + errors.join("\n  - "));
  }

  const scene = {
    type: "excalidraw",
    version: 2,
    source: "https://github.com/zsviczian/obsidian-excalidraw-plugin",
    elements,
    appState: {
      gridSize: null,
      viewBackgroundColor: spec.background ?? "#ffffff",
    },
    files: {},
  };
  return scene;
}

function textProps(text, fontSize, fontFamily, textAlign) {
  const raw = String(text);
  return {
    text: raw,
    rawText: raw,
    originalText: raw,
    fontSize,
    fontFamily,
    textAlign,
    verticalAlign: "top",
    autoResize: true,
    lineHeight: LINE_H,
    roundness: null,
    containerId: null,
  };
}

// ---------------------------------------------------------------------------
// Obsidian .excalidraw.md wrapper
// ---------------------------------------------------------------------------
function toObsidianMd(scene) {
  const texts = scene.elements.filter((e) => e.type === "text");
  const textBlocks = texts
    .map((t) => `${t.text} ^${t.id}`)
    .join("\n\n");

  const drawing = JSON.stringify(scene, null, "\t");

  return `---

excalidraw-plugin: parsed
tags: [excalidraw]

---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==

# Excalidraw Data

## Text Elements
${textBlocks}

%%
## Drawing
\`\`\`json
${drawing}
\`\`\`
%%`;
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------
function main() {
  const args = parseArgs(process.argv);
  let raw;
  if (args.stdin) {
    raw = fs.readFileSync(0, "utf8");
  } else if (args.spec) {
    raw = fs.readFileSync(args.spec, "utf8");
  } else {
    console.error(
      "usage: node build.mjs --spec spec.json --out diagram.excalidraw.md [--plain]",
    );
    process.exit(2);
  }
  if (!args.out) {
    console.error("error: --out is required");
    process.exit(2);
  }

  let spec;
  try {
    spec = JSON.parse(raw);
  } catch (err) {
    console.error("error: spec is not valid JSON:", err.message);
    process.exit(1);
  }

  let scene;
  try {
    scene = compile(spec);
  } catch (err) {
    console.error("error: " + err.message);
    process.exit(1);
  }

  // structural self-check
  const ids = new Set(scene.elements.map((e) => e.id));
  for (const el of scene.elements) {
    if (el.containerId && !ids.has(el.containerId))
      throw new Error(`dangling containerId: ${el.containerId}`);
    for (const b of el.boundElements ?? [])
      if (!ids.has(b.id)) throw new Error(`dangling boundElement: ${b.id}`);
    if (el.startBinding && !ids.has(el.startBinding.elementId))
      throw new Error(`dangling startBinding: ${el.startBinding.elementId}`);
    if (el.endBinding && !ids.has(el.endBinding.elementId))
      throw new Error(`dangling endBinding: ${el.endBinding.elementId}`);
  }

  const outMd = args.out.endsWith(".md") ? args.out : args.out + ".md";
  fs.mkdirSync(path.dirname(path.resolve(outMd)), { recursive: true });
  fs.writeFileSync(outMd, toObsidianMd(scene));
  const summary = {
    out: outMd,
    elements: scene.elements.length,
    nodes: (spec.nodes ?? []).length,
    edges: (spec.edges ?? []).length,
  };
  if (args.plain) {
    const plain = outMd.replace(/\.excalidraw\.md$|\.md$/, "") + ".excalidraw";
    fs.writeFileSync(plain, JSON.stringify(scene, null, 2));
    summary.plain = plain;
  }
  console.log(JSON.stringify(summary, null, 2));
}

main();
