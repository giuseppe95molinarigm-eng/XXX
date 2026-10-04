// Render book/html/part-*.html to PDF chunks (waits for fonts and in-page layout scripts).
// Usage: node build/render_book.mjs [pattern]
import { chromium } from 'playwright';
import fs from 'fs'; import path from 'path';
const dir = path.resolve('book/html');
const out = path.resolve('book/pdf'); fs.mkdirSync(out, { recursive: true });
const only = process.argv[2];
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && (!only || f.includes(only))).sort();
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined });
const page = await browser.newPage({ deviceScaleFactor: 4 });
await page.emulateMedia({ media: 'print' });
for (const f of files) {
  await page.goto('file://' + path.join(dir, f), { waitUntil: 'load', timeout: 300000 });
  await page.waitForFunction(() => document.body.dataset.done === '1', null, { timeout: 300000 });
  const overflow = await page.evaluate(() => document.body.dataset.overflow);
  if (overflow) console.log('OVERFLOW in', f);
  await page.pdf({ path: path.join(out, f.replace('.html', '.pdf')), preferCSSPageSize: true, printBackground: true, timeout: 300000 });
  console.log('rendered', f);
}
await browser.close();
