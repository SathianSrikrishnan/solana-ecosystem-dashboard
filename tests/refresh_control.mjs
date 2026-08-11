import assert from "node:assert/strict";
import { chromium } from "playwright";

const targetUrl = process.env.QA_URL ?? "http://127.0.0.1:8766/index.html";
const browser = await chromium.launch({ headless: true });

try {
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto(targetUrl, { waitUntil: "networkidle" });
  await page.getByRole("button", { name: "Check for latest data" }).click();
  await page.getByText("You already have the latest verified snapshot.").waitFor();
  assert.equal(
    await page.locator("#refresh-message").textContent(),
    "You already have the latest verified snapshot.",
  );
} finally {
  await browser.close();
}

console.log(`Refresh control verified against published snapshot: ${targetUrl}`);
