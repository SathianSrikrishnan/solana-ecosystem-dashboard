import AxeBuilder from "@axe-core/playwright";
import { mkdirSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";

const targetUrl = process.env.COMPANION_URL ?? pathToFileURL(resolve("output/crypto-101.html")).href;
const auditDir = resolve("docs/audits/2026-08-11-crypto-101-draft");
mkdirSync(auditDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const failures = [];

try {
  for (const viewport of [
    { name: "desktop", width: 1440, height: 1000 },
    { name: "mobile", width: 390, height: 844 },
  ]) {
    const context = await browser.newContext({ viewport });
    const page = await context.newPage();
    const consoleErrors = [];
    page.on("console", (message) => {
      if (message.type() === "error") consoleErrors.push(message.text());
    });
    page.on("pageerror", (error) => consoleErrors.push(error.message));
    await page.goto(targetUrl, { waitUntil: "load" });

    if (await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth)) {
      failures.push(`${viewport.name}: horizontal overflow`);
    }
    if (consoleErrors.length) failures.push(`${viewport.name}: ${consoleErrors.join(" | ")}`);
    if ((await page.locator("h1").innerText()).replace(/\s+/g, " ").trim() !== "Saraswati, Lakshmi, and the Ledger") {
      failures.push(`${viewport.name}: title mismatch`);
    }
    const images = page.locator("main img");
    if ((await images.count()) < 5) failures.push(`${viewport.name}: expected a visual story with at least five images`);
    for (let index = 0; index < await images.count(); index += 1) {
      if (!(await images.nth(index).evaluate((image) => image.complete && image.naturalWidth > 0))) {
        failures.push(`${viewport.name}: image ${index + 1} did not load`);
      }
    }
    const firstQuestion = page.locator("[data-test-question]").first();
    await firstQuestion.check();
    if (!(await page.locator("[data-test-result]").innerText()).includes("Saraswati")) {
      failures.push(`${viewport.name}: framework test did not update`);
    }
    const axe = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    for (const violation of axe.violations) {
      const targets = violation.nodes.map((node) => node.target.join(" ")).join(", ");
      failures.push(`${viewport.name}: ${violation.id} (${targets})`);
    }
    await page.screenshot({ path: resolve(auditDir, `${viewport.name}.png`), fullPage: true });
    await context.close();
  }
} finally {
  await browser.close();
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log(`Companion page passed visual and Axe QA: ${targetUrl}`);
