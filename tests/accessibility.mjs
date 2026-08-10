import AxeBuilder from "@axe-core/playwright";
import { chromium } from "playwright";

const targetUrl = process.env.A11Y_URL ?? "http://127.0.0.1:8766/index.html";
const viewports = [
  { name: "desktop", width: 1280, height: 720 },
  { name: "mobile", width: 390, height: 844 },
];

const browser = await chromium.launch({ headless: true });
const failures = [];

try {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport });
    const page = await context.newPage();
    await page.goto(targetUrl, { waitUntil: "load" });
    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    for (const violation of results.violations) {
      failures.push(
        `${viewport.name}: ${violation.id} (${violation.impact}) - ${violation.help}`,
      );
    }
    await context.close();
  }
} finally {
  await browser.close();
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log(`Axe passed ${viewports.length} viewports: ${targetUrl}`);
