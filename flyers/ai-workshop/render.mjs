import { chromium } from 'playwright';
import path from 'path';

const editions = [
  { page: 'flyer-print.html',    png: 'TTMath-AI-Workshop-flyer.png',    pdf: 'TTMath-AI-Workshop-flyer.pdf' },
  { page: 'flyer-print-zh.html', png: 'TTMath-AI-Workshop-flyer-zh.png', pdf: 'TTMath-AI-Workshop-flyer-zh.pdf' },
];

const browser = await chromium.launch();
for (const e of editions) {
  const ctx = await browser.newContext({ viewport: { width: 900, height: 1120 }, deviceScaleFactor: 3 });
  const page = await ctx.newPage();
  await page.goto('file://' + path.join(process.cwd(), e.page), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);

  const fit = await page.evaluate(() => {
    const s = document.querySelector('.sheet').getBoundingClientRect();
    const b = document.querySelector('.band').getBoundingClientRect();
    return { bandBottom: +(b.bottom - s.top).toFixed(1), bottomMargin: +(s.bottom - b.bottom).toFixed(1) };
  });
  console.log(e.page, JSON.stringify(fit), fit.bottomMargin < 12 ? '  <-- TOO TIGHT' : '');

  await page.locator('.sheet').screenshot({ path: e.png });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: e.pdf, width: '8.5in', height: '11in', printBackground: true,
                   margin: { top: '0', bottom: '0', left: '0', right: '0' } });
  await ctx.close();
}
await browser.close();
console.log('done');
