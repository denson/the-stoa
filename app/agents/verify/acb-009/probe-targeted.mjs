#!/usr/bin/env node
// Re-probe DoD#4 (palette nav by URL) and DoD#6 (STOA_STATE reactivity)
// using the actual testids from acb-008. Author: Denson Smith.

import { spawn } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const BASE = "http://localhost:5176";
const CHROME = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe";
const CDP_PORT = 9334;

const userDataDir = mkdtempSync(join(tmpdir(), "vera-cdp-"));
const chrome = spawn(CHROME, [
  `--remote-debugging-port=${CDP_PORT}`,
  `--user-data-dir=${userDataDir}`,
  "--headless=new",
  "--no-first-run",
  "--no-default-browser-check",
  `${BASE}/`,
], { stdio: "ignore" });

await new Promise((r) => setTimeout(r, 1500));

const tabs = await (await fetch(`http://127.0.0.1:${CDP_PORT}/json`)).json();
const target = tabs.find((t) => t.type === "page");
const ws = new (await import("ws")).WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.once("open", r));

let msgId = 0;
const pending = new Map();
ws.on("message", (data) => {
  const msg = JSON.parse(data.toString());
  if (msg.id != null && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    if (msg.error) reject(new Error(msg.error.message));
    else resolve(msg.result);
  }
});
function send(method, params = {}) {
  const id = ++msgId;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
  });
}
async function eval_(expr, awaitPromise = false) {
  const r = await send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise });
  if (r.exceptionDetails) throw new Error(JSON.stringify(r.exceptionDetails));
  return r.result.value;
}
async function navigate(url) {
  await send("Page.enable");
  await send("Page.navigate", { url });
  await new Promise((r) => setTimeout(r, 800));
}

try {
  // ===== Re-probe DoD#4: palette by testid =====
  await navigate(`${BASE}/`);
  await new Promise((r) => setTimeout(r, 500));

  // Open palette via Cmd+K
  const openResult = await eval_(`(() => {
    const e = new KeyboardEvent('keydown', { key: 'k', metaKey: true, bubbles: true, cancelable: true });
    window.dispatchEvent(e);
    return true;
  })()`);
  await new Promise((r) => setTimeout(r, 300));

  const paletteInputPresent = await eval_(
    `!!document.querySelector('[data-testid="palette-input"]')`
  );
  console.log(`palette-input present: ${paletteInputPresent}`);

  // Type into palette-input
  await eval_(`(() => {
    const inp = document.querySelector('[data-testid="palette-input"]');
    if (inp) {
      inp.focus();
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      setter.call(inp, 'PLINY');
      inp.dispatchEvent(new Event('input', { bubbles: true }));
    }
    return inp ? 'input-set' : 'no-input';
  })()`);
  await new Promise((r) => setTimeout(r, 300));

  // Click the testid'd row for MAJOR_PLINY
  const clickResult = await eval_(`(() => {
    const row = document.querySelector('[data-testid="palette-result-officer-MAJOR_PLINY"]');
    if (!row) {
      const all = Array.from(document.querySelectorAll('[data-testid^="palette-result-"]')).map(e => e.getAttribute('data-testid'));
      return { found: false, allRows: all };
    }
    row.click();
    return { found: true, testid: row.getAttribute('data-testid') };
  })()`);
  console.log(`click result: ${JSON.stringify(clickResult)}`);
  await new Promise((r) => setTimeout(r, 500));

  const urlAfter = await eval_(`location.href`);
  const stoaAfter = await eval_(
    `({ tab: window.STOA_STATE?.currentTab, sel: window.STOA_STATE?.selectedOfficer?.name })`
  );
  const paletteStillOpen = await eval_(
    `!!document.querySelector('[data-testid="palette-input"]')`
  );
  console.log(`url after palette pick: ${urlAfter}`);
  console.log(`stoa after palette pick: ${JSON.stringify(stoaAfter)}`);
  console.log(`palette still open after pick: ${paletteStillOpen}`);

  const palettePass =
    urlAfter.includes("/officer/MAJOR_PLINY") &&
    stoaAfter.sel === "MAJOR_PLINY" &&
    !paletteStillOpen;
  console.log(`DoD#4 result: ${palettePass ? "PASS" : "FAIL"}`);

  // ===== Re-probe DoD#6: refIneq with longer wait =====
  await navigate(`${BASE}/`);
  await new Promise((r) => setTimeout(r, 500));
  const refIneq2 = await eval_(`(async () => {
    const a = window.STOA_STATE;
    window.location.hash = '#/skills';
    await new Promise(r => setTimeout(r, 400));
    const b = window.STOA_STATE;
    return {
      sameRef: a === b,
      shapeA: { tab: a?.currentTab, sel: a?.selectedOfficer?.name ?? null },
      shapeB: { tab: b?.currentTab, sel: b?.selectedOfficer?.name ?? null },
    };
  })()`, true);
  console.log(`refIneq probe v2: ${JSON.stringify(refIneq2)}`);

  // Probe shape vs requirement
  await navigate(`${BASE}/#/officer/ADA?roster=minimal&archetype=executor`);
  await new Promise((r) => setTimeout(r, 600));
  const shape = await eval_(`(() => {
    const s = window.STOA_STATE;
    return {
      keys: Object.keys(s).sort(),
      dark: typeof s.dark,
      currentTab: s.currentTab,
      selectedOfficerName: s.selectedOfficer?.name,
      roster: s.roster,
      archetypeFilter: s.archetypeFilter,
    };
  })()`);
  console.log(`STOA_STATE shape after URL change: ${JSON.stringify(shape)}`);
  const expectedKeys = ["archetypeFilter", "currentTab", "dark", "roster", "selectedOfficer"];
  const shapeOk =
    JSON.stringify(shape.keys) === JSON.stringify(expectedKeys) &&
    shape.currentTab === "team" &&
    shape.selectedOfficerName === "ADA" &&
    shape.roster === "minimal" &&
    shape.archetypeFilter === "executor";
  console.log(`DoD#6 shape match: ${shapeOk ? "PASS" : "FAIL"}`);
} catch (e) {
  console.error("ERR:", e);
} finally {
  ws.close();
  chrome.kill();
  try { rmSync(userDataDir, { recursive: true, force: true }); } catch {}
  process.exit(0);
}
