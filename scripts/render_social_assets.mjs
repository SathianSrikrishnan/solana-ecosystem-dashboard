import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";

const jobs = [
  {
    source: "assets/brand/crypto-101-social.html",
    output: "output/crypto-101-social.png",
    width: 1200,
    height: 630,
  },
  {
    source: "assets/brand/social-cover.html",
    output: "output/solana-observatory-cover.png",
    width: 1200,
    height: 630,
  },
  {
    source: "assets/brand/six-question-map.html",
    output: "output/solana-six-question-map.png",
    width: 1200,
    height: 1200,
  },
];

const browser = await chromium.launch({ headless: true });
try {
  for (const job of jobs) {
    const context = await browser.newContext({
      viewport: { width: job.width, height: job.height },
      deviceScaleFactor: 1,
    });
    const page = await context.newPage();
    await page.goto(pathToFileURL(resolve(job.source)).href, { waitUntil: "load" });
    await page.screenshot({ path: resolve(job.output) });
    await context.close();
    console.log(job.output);
  }
} finally {
  await browser.close();
}
