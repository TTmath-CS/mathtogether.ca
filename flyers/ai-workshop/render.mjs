import { chromium } from 'playwright';
import path from 'path';

const dir = process.cwd();
const url = 'file://' + path.join(dir, 'flyer-print.html');

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 900, height: 1120 }, deviceScaleFactor: 3 });
const page = await ctx.newPage();
await page.goto(url, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(400);

// overflow check
const metrics = await page.evaluate(() => {
  const s = document.querySelector('.sheet');
  const r = s.getBoundingClientRect();
  const last = document.querySelector('.band').getBoundingClientRect();
  return { sheetH: r.height, contentBottom: last.bottom - r.top, scrollH: s.scrollHeight };
});
console.log('metrics', JSON.stringify(metrics));

await page.locator('.sheet').screenshot({ path: 'TTMath-AI-Workshop-flyer.png' });
await page.emulateMedia({ media: 'print' });
await page.pdf({ path: 'TTMath-AI-Workshop-flyer.pdf', width: '8.5in', height: '11in',
                 printBackground: true, margin: { top: '0', bottom: '0', left: '0', right: '0' } });
await browser.close();
console.log('done');
