import { mkdirSync } from "node:fs";
import { resolve } from "node:path";
import { chromium } from "playwright";

const targetUrl = process.env.QA_URL ?? "http://127.0.0.1:8766/index.html";
const auditDir = resolve("docs/audits/2026-08-10-release-candidate");
mkdirSync(auditDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const failures = [];

async function inspect(name, viewport, captures) {
  const context = await browser.newContext({ viewport });
  const page = await context.newPage();
  const consoleErrors = [];
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  page.on("pageerror", (error) => consoleErrors.push(error.message));
  await page.goto(targetUrl, { waitUntil: "networkidle" });

  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
  );
  if (overflow) failures.push(`${name}: horizontal page overflow`);
  if (consoleErrors.length) failures.push(`${name}: ${consoleErrors.join(" | ")}`);

  for (const [selector, filename] of captures) {
    const target = page.locator(selector);
    if ((await target.count()) !== 1) {
      failures.push(`${name}: expected one ${selector}`);
      continue;
    }
    await target.screenshot({ path: resolve(auditDir, filename) });
  }

  if ((await page.locator(".sparkline").count()) < 1) failures.push(`${name}: no sparklines`);
  if ((await page.locator("#anomaly-monitor").count()) !== 1) failures.push(`${name}: no anomaly monitor`);
  if ((await page.locator("#validator-leaderboard tbody tr").count()) !== 10) {
    failures.push(`${name}: validator leaderboard does not have 10 rows`);
  }
  await context.close();
}

try {
  await inspect("desktop", { width: 1440, height: 1000 }, [
    ["#overview", "12-final-overview.png"],
    ["#validators", "13-final-validators.png"],
  ]);
  await inspect("mobile", { width: 360, height: 800 }, [
    ["#overview", "14-final-mobile.png"],
  ]);
} finally {
  await browser.close();
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log(`Visual QA passed desktop and mobile: ${targetUrl}`);
