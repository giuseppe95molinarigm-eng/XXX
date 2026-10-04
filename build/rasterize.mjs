// Rasterize SVG files at a fixed pixel width (used to derive outline flags).
// Usage: node build/rasterize.mjs <width_px> <out_dir> <in.svg>...
import { chromium } from 'playwright';
import fs from 'fs'; import path from 'path';
const [,, width, outDir, ...files] = process.argv;
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const page = await browser.newPage();
for (const f of files) {
  const svg = fs.readFileSync(f, 'utf8');
  const vb = svg.match(/viewBox="([^"]+)"/)[1].trim().split(/[\s,]+/).map(Number);
  const W = Number(width), H = Math.round(W * vb[3] / vb[2]);
  await page.setViewportSize({ width: W, height: H });
  await page.setContent(`<html><body style="margin:0;background:#fff">${svg.replace(/<svg /, `<svg width="${W}" height="${H}" `)}</body></html>`);
  await page.screenshot({ path: path.join(outDir, path.basename(f, '.svg') + '.png'), clip: { x: 0, y: 0, width: W, height: H } });
}
await browser.close();
