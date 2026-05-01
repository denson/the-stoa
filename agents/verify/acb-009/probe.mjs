#!/usr/bin/env node
// VERA verification harness for acb-009 — drives Chrome via CDP to exercise
// the DoD criteria ADA's headless-Chrome smoke run could not cover (back/forward,
// palette URL nav, default-stripping, refresh-survival, unknown-route fallback).
//
// Author: Denson Smith (via VERA dispatch on acb-009).

import { spawn } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const BASE = "http://localhost:5176";
const CHROME = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe";
const CDP_PORT = 9333;

const userDataDir = mkdtempSync(join(tmpdir(), "vera-cdp-"));

const chrome = spawn(CHROME, [
  `--remote-debugging-port=${CDP_PORT}`,
  `--user-data-dir=${userDataDir}`,
  "--headless=new",
  "--no-first-run",
  "--no-default-browser-check",
  "--disable-features=TranslateUI",
  `${BASE}/`,
], { stdio: "ignore" });

await new Promise((r) => setTimeout(r, 1500));

async function getTabs() {
  const r = await fetch(`http://127.0.0.1:${CDP_PORT}/json`);
  return r.json();
}

let tabs = await getTabs();
let target = tabs.find((t) => t.type === "page");
if (!target) {
  console.error("no page target found");
  process.exit(2);
}

const ws = new (await import("ws")).WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.once("open", r));

let msgId = 0;
const pending = new Map();
const events = [];
ws.on("message", (data) => {
  const msg = JSON.parse(data.toString());
  if (msg.id != null && pending.has(msg.id)) {
    const { resolve, reject } = pending.get(msg.id);
    pending.delete(msg.id);
    if (msg.error) reject(new Error(msg.error.message));
    else resolve(msg.result);
  } else {
    events.push(msg);
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
  const r = await send("Runtime.evaluate", {
    expression: expr,
    returnByValue: true,
    awaitPromise,
  });
  if (r.exceptionDetails) {
    throw new Error("eval exception: " + JSON.stringify(r.exceptionDetails));
  }
  return r.result.value;
}

async function navigate(url) {
  await send("Page.enable");
  await send("Page.navigate", { url });
  await new Promise((r) => setTimeout(r, 700));
}

async function goBack() {
  await eval_(`window.history.back()`);
  await new Promise((r) => setTimeout(r, 400));
}

async function goForward() {
  await eval_(`window.history.forward()`);
  await new Promise((r) => setTimeout(r, 400));
}

async function getUrl() {
  return await eval_(`location.href`);
}

async function getStoaState() {
  return await eval_(
    `JSON.parse(JSON.stringify({
       dark: window.STOA_STATE?.dark,
       currentTab: window.STOA_STATE?.currentTab,
       selectedOfficerName: window.STOA_STATE?.selectedOfficer?.name ?? null,
       roster: window.STOA_STATE?.roster,
       archetypeFilter: window.STOA_STATE?.archetypeFilter,
     }))`
  );
}

async function getH1() {
  return await eval_(`document.querySelector('h1')?.textContent ?? null`);
}

async function pageContains(text) {
  return await eval_(`document.body.innerText.includes(${JSON.stringify(text)})`);
}

const results = [];
function record(name, pass, detail) {
  results.push({ name, pass, detail });
  const tag = pass === true ? "PASS" : pass === false ? "FAIL" : "PARTIAL";
  console.log(`[${tag}] ${name}: ${detail}`);
}

try {
  // ===== DoD #1 — Direct deep-link load =====
  await navigate(`${BASE}/#/officer/MAJOR_PLINY?roster=default`);
  await new Promise((r) => setTimeout(r, 600));
  let url = await getUrl();
  let h1 = await getH1();
  let stoa = await getStoaState();
  // Per Decision 5, roster=default should be stripped on first round-trip,
  // BUT the spec §9.7 says it's honored on initial load and stripped only
  // on next setSearchParams. So URL may still contain roster=default until
  // a filter toggle. State shape is what matters here.
  record(
    "DoD#1 deep-link officer/MAJOR_PLINY",
    h1?.includes("MAJOR_PLINY") &&
      stoa.selectedOfficerName === "MAJOR_PLINY" &&
      stoa.currentTab === "team" &&
      stoa.roster === "default",
    `url=${url} h1=${JSON.stringify(h1)} stoa=${JSON.stringify(stoa)}`
  );

  // ===== DoD #2 — Browser back/forward =====
  await navigate(`${BASE}/`);
  await navigate(`${BASE}/#/officer/MAJOR_PLINY`);
  await new Promise((r) => setTimeout(r, 400));
  let urlAfterNav = await getUrl();
  let stoaAfter = await getStoaState();

  await goBack();
  let urlBack = await getUrl();
  let stoaBack = await getStoaState();

  await goForward();
  let urlFwd = await getUrl();
  let stoaFwd = await getStoaState();

  const backForwardPass =
    stoaAfter.selectedOfficerName === "MAJOR_PLINY" &&
    stoaBack.selectedOfficerName === null &&
    stoaBack.currentTab === "team" &&
    stoaFwd.selectedOfficerName === "MAJOR_PLINY";
  record(
    "DoD#2 back/forward navigation",
    backForwardPass,
    `nav=${urlAfterNav} back=${urlBack} fwd=${urlFwd}; ` +
      `stoa.selected after=${stoaAfter.selectedOfficerName} back=${stoaBack.selectedOfficerName} fwd=${stoaFwd.selectedOfficerName}`
  );

  // Skills <-> Meta back
  await navigate(`${BASE}/#/skills`);
  await navigate(`${BASE}/#/meta`);
  await goBack();
  let stoaSkillsBack = await getStoaState();
  record(
    "DoD#2 skills→meta→back returns to skills",
    stoaSkillsBack.currentTab === "skills",
    `currentTab after back=${stoaSkillsBack.currentTab}`
  );

  // ===== DoD #3 — Refresh survives =====
  await navigate(`${BASE}/#/officer/MAJOR_PLINY?archetype=architect`);
  await new Promise((r) => setTimeout(r, 400));
  await send("Page.reload");
  await new Promise((r) => setTimeout(r, 1200));
  let urlAfterReload = await getUrl();
  let h1AfterReload = await getH1();
  let stoaAfterReload = await getStoaState();
  record(
    "DoD#3 refresh-survives officer+archetype",
    h1AfterReload?.includes("MAJOR_PLINY") &&
      stoaAfterReload.archetypeFilter === "architect",
    `url=${urlAfterReload} h1=${JSON.stringify(h1AfterReload)} archetype=${stoaAfterReload.archetypeFilter}`
  );

  // Refresh on /#/skills
  await navigate(`${BASE}/#/skills`);
  await send("Page.reload");
  await new Promise((r) => setTimeout(r, 1000));
  let stoaSkillsRefresh = await getStoaState();
  record(
    "DoD#3 refresh-survives /skills",
    stoaSkillsRefresh.currentTab === "skills",
    `currentTab after refresh=${stoaSkillsRefresh.currentTab}`
  );

  // ===== DoD #4 — Palette navigates by URL =====
  await navigate(`${BASE}/`);
  await new Promise((r) => setTimeout(r, 500));
  // Open palette via Cmd+K — synthesize a keydown event on window
  await eval_(`(() => {
    const e = new KeyboardEvent('keydown', { key: 'k', metaKey: true, bubbles: true });
    window.dispatchEvent(e);
  })()`);
  await new Promise((r) => setTimeout(r, 300));
  // Type into palette input and pick MAJOR_PLINY by clicking first matching row
  // The palette input has data-testid based on Components.tsx; let's target via placeholder/role
  // We'll inspect available testids to find the palette + officer rows
  const paletteOpen = await eval_(
    `!!document.querySelector('[data-testid="command-palette"]') ||
     !!Array.from(document.querySelectorAll('input')).find(i => i.placeholder && i.placeholder.toLowerCase().includes("search"))`
  );
  // Try common palette structure: input + list of rows
  await eval_(`(() => {
    const inputs = Array.from(document.querySelectorAll('input'));
    const palInput = inputs.find(i => i.placeholder && /search|command/i.test(i.placeholder)) || inputs[inputs.length - 1];
    if (palInput) {
      palInput.focus();
      palInput.value = 'MAJOR_PLINY';
      palInput.dispatchEvent(new Event('input', { bubbles: true }));
    }
  })()`);
  await new Promise((r) => setTimeout(r, 300));
  // Find a clickable row containing "MAJOR_PLINY" and click it
  const clicked = await eval_(`(() => {
    const candidates = Array.from(document.querySelectorAll('div, button, a, li'));
    const row = candidates.find(el => {
      const t = el.textContent || '';
      return t.includes('MAJOR_PLINY') &&
             el.offsetParent !== null &&
             (el.onclick || el.getAttribute('role') === 'option' || el.tagName === 'BUTTON' || el.tagName === 'A' ||
              window.getComputedStyle(el).cursor === 'pointer');
    });
    if (row) { row.click(); return row.tagName + '|' + (row.getAttribute('data-testid') || ''); }
    return null;
  })()`);
  await new Promise((r) => setTimeout(r, 500));
  let urlAfterPalette = await getUrl();
  let stoaAfterPalette = await getStoaState();
  record(
    "DoD#4 palette navigates by URL",
    urlAfterPalette.includes("/officer/MAJOR_PLINY") &&
      stoaAfterPalette.selectedOfficerName === "MAJOR_PLINY",
    `paletteOpenDetected=${paletteOpen} clicked=${clicked} url=${urlAfterPalette} stoa.selected=${stoaAfterPalette.selectedOfficerName}`
  );

  // ===== DoD #6 — STOA_STATE bridge reads URL-driven fields =====
  // Verify shape and reactivity
  await navigate(`${BASE}/`);
  let stoaShape1 = await getStoaState();
  await navigate(`${BASE}/#/officer/MAJOR_PLINY`);
  await new Promise((r) => setTimeout(r, 400));
  let stoaShape2 = await getStoaState();
  await navigate(`${BASE}/#/skills`);
  await new Promise((r) => setTimeout(r, 400));
  let stoaShape3 = await getStoaState();
  // Reference inequality probe — check that consecutive renders produce new objects
  const refIneq = await eval_(`(() => {
    const a = window.STOA_STATE;
    return new Promise(res => {
      // Toggle URL by pushing a query
      window.location.hash = '#/?archetype=architect';
      requestAnimationFrame(() => requestAnimationFrame(() => {
        const b = window.STOA_STATE;
        res(a !== b);
      }));
    });
  })()`, true);

  const shapeOk =
    stoaShape1.currentTab === "team" && stoaShape1.selectedOfficerName === null &&
    stoaShape2.currentTab === "team" && stoaShape2.selectedOfficerName === "MAJOR_PLINY" &&
    stoaShape3.currentTab === "skills";
  record(
    "DoD#6 STOA_STATE bridge URL-driven + reactive",
    shapeOk && refIneq === true,
    `shape1=${JSON.stringify(stoaShape1)} shape2.selected=${stoaShape2.selectedOfficerName} shape3.tab=${stoaShape3.currentTab} refIneq=${refIneq}`
  );

  // ===== Unknown route fallback =====
  await navigate(`${BASE}/#/garbage`);
  await new Promise((r) => setTimeout(r, 600));
  let urlGarbage = await getUrl();
  let stoaGarbage = await getStoaState();
  record(
    "Unknown-route Navigate replace to /",
    (urlGarbage.endsWith("/#/") || urlGarbage.endsWith("/")) &&
      stoaGarbage.currentTab === "team" &&
      stoaGarbage.selectedOfficerName === null,
    `url=${urlGarbage} stoa=${JSON.stringify(stoaGarbage)}`
  );

  // ===== Unknown officer 404 =====
  await navigate(`${BASE}/#/officer/NOT_A_REAL_OFFICER`);
  await new Promise((r) => setTimeout(r, 500));
  const has404Msg = await pageContains("not found");
  const hasBackLink = await pageContains("Back to Team");
  record(
    "Unknown-officer renders 404 + back link (no crash)",
    has404Msg && hasBackLink,
    `notFoundMsg=${has404Msg} backLink=${hasBackLink}`
  );

  // ===== Default-stripping edge case =====
  await navigate(`${BASE}/#/?roster=default&archetype=architect`);
  await new Promise((r) => setTimeout(r, 400));
  let urlBeforeToggle = await getUrl();
  // Click an archetype filter to trigger setArchetype which round-trips through stripDefaultSearchParams
  // Simpler: directly probe that a setSearchParams round-trip strips roster=default
  await eval_(`(() => {
    // Find a filter chip — they're rendered in FilterSidebar; click any archetype chip
    const chips = Array.from(document.querySelectorAll('div, button')).filter(el => {
      const t = (el.textContent || '').trim();
      return t.length > 0 && t.length < 30 && window.getComputedStyle(el).cursor === 'pointer';
    });
    // Try to find an archetype-like chip and click; falls back to no-op
    const arch = chips.find(c => /architect|verifier|reviewer|reasoner/i.test(c.textContent || ''));
    if (arch) arch.click();
  })()`);
  await new Promise((r) => setTimeout(r, 500));
  let urlAfterToggle = await getUrl();
  record(
    "Default-stripping (roster=default removed after toggle round-trip)",
    !urlAfterToggle.includes("roster=default"),
    `before=${urlBeforeToggle} after=${urlAfterToggle}`
  );

  console.log("\n=== SUMMARY ===");
  for (const r of results) {
    const tag = r.pass === true ? "PASS" : r.pass === false ? "FAIL" : "PARTIAL";
    console.log(`[${tag}] ${r.name}`);
  }
} catch (e) {
  console.error("HARNESS ERROR:", e);
} finally {
  ws.close();
  chrome.kill();
  try { rmSync(userDataDir, { recursive: true, force: true }); } catch {}
  process.exit(0);
}
