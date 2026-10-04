// Render an HTML file to PDF (A4, print backgrounds) and/or PNG previews with Chromium.
// Usage: node build/render.mjs <in.html> <out.pdf|-> [png_prefix] [scale]
import { chromium } from 'playwright';
import path from 'path';
const [,, input, outPdf, pngPrefix, scale] = process.argv;
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const page = await browser.newPage({ deviceScaleFactor: Number(scale || 2) });
await page.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(500);
if (outPdf && outPdf !== '-') {
  await page.pdf({ path: outPdf, preferCSSPageSize: true, printBackground: true });
}
if (pngPrefix) {
  await page.emulateMedia({ media: 'print' });
  const sheets = await page.$$('.page');
  for (let i = 0; i < sheets.length; i++) {
    await sheets[i].screenshot({ path: `${pngPrefix}-${String(i + 1).padStart(2, '0')}.png` });
  }
}
await browser.close();
