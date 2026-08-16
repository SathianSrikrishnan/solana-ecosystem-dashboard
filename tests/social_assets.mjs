import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";

const assets = [
  ["assets/brand/crypto-101-social.html", 1200, 630],
  ["assets/brand/social-cover.html", 1200, 630],
  ["assets/brand/six-question-map.html", 1200, 1200],
];

const flagshipSocial = readFileSync("assets/brand/crypto-101-social.html", "utf8");
assert.match(flagshipSocial, /Saraswati, Lakshmi/);
assert.match(flagshipSocial, /flagship-hero\.png/);

const browser = await chromium.launch({ headless: true });
try {
  for (const [source, width, height] of assets) {
    const page = await browser.newPage({ viewport: { width, height } });
    await page.goto(pathToFileURL(resolve(source)).href, { waitUntil: "load" });
    const bounds = await page.evaluate(() => ({
      width: document.body.scrollWidth,
      height: document.body.scrollHeight,
    }));
    assert.equal(bounds.width, width, `${source} overflows horizontally`);
    assert.equal(bounds.height, height, `${source} overflows vertically`);
    await page.close();
  }
} finally {
  await browser.close();
}

console.log(`Social assets fit ${assets.length} exact viewports.`);
