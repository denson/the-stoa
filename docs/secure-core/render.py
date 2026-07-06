#!/usr/bin/env python
"""Render deployment-plan.md -> deployment-plan.html (self-contained, styled).
Re-run after editing the markdown:  python docs/secure-core/render.py
Author: Denson Smith."""
import markdown, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "deployment-plan.md"
OUT = HERE / "deployment-plan.html"

text = SRC.read_text(encoding="utf-8")
# drop the leading author HTML comment from the rendered view
text = re.sub(r'^<!--.*?-->\n', '', text, count=1, flags=re.S)
# pull the title (first H1) for the banner; keep it in the body too
m = re.search(r'^#\s+(.+)$', text, flags=re.M)
title = m.group(1).strip() if m else "Deployment Plan"

md = markdown.Markdown(
    extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"],
    extension_configs={"toc": {"permalink": False, "toc_depth": "2-3"}},
)
body = md.convert(text)
toc = md.toc

TPL = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="Denson Smith">
<title>__TITLE__</title>
<style>
  :root{--ink:#1c2230;--muted:#5b6573;--line:#e3e7ee;--bg:#fff;--soft:#f6f8fb;
    --accent:#2f6df6;--good:#15803d;--code:#0f172a;--code-bg:#f5f6f8;--warn:#9a3412;--warn-soft:#fff7ed}
  *{box-sizing:border-box}html{scroll-behavior:smooth}
  body{margin:0;background:var(--bg);color:var(--ink);
    font:16.5px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;-webkit-font-smoothing:antialiased}
  .wrap{max-width:880px;margin:0 auto;padding:0 22px 120px}
  header.banner{max-width:880px;margin:0 auto;padding:38px 22px 4px}
  .badge{display:inline-block;font-size:12.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;
    color:var(--good);background:#e9f7ef;border:1px solid #bfe6cd;border-radius:999px;padding:4px 12px}
  .badge.live{color:#1f3a8a;background:#eaf1ff;border-color:#cfe0ff;margin-left:6px}
  h1.title{font-size:29px;line-height:1.2;margin:14px 0 6px;letter-spacing:-.01em}
  .sub{color:var(--muted);font-size:15px;margin:0}
  .toc{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:10px 18px;margin:22px 0}
  .toc::before{content:"Contents";display:block;font-weight:700;font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);margin:4px 0 6px}
  .toc ul{margin:0;padding-left:18px}.toc>ul{padding-left:2px;list-style:none}.toc>ul>li{margin:3px 0}
  .toc a{color:#2b3a55;text-decoration:none}.toc a:hover{text-decoration:underline;color:var(--accent)}
  .doc h1{font-size:23px;margin:6px 0 8px}
  .doc h1:first-child{position:absolute;left:-9999px}  /* hide duplicate title (it's in the banner) */
  .doc h2{font-size:21px;margin:36px 0 10px;padding-top:16px;border-top:2px solid var(--line)}
  .doc h3{font-size:16.5px;margin:22px 0 6px;color:#22304a}
  .doc p{margin:10px 0}.doc a{color:var(--accent)}.doc strong{color:#16203a}
  .doc ul,.doc ol{margin:10px 0;padding-left:24px}.doc li{margin:5px 0}
  .doc hr{border:0;border-top:1px solid var(--line);margin:30px 0}
  .doc>p:first-of-type,.doc>p:nth-of-type(2){background:var(--soft);border-left:4px solid var(--accent);
    border-radius:0 8px 8px 0;padding:10px 16px;margin:12px 0}
  code{font-family:"SFMono-Regular",ui-monospace,"Cascadia Code",Consolas,monospace;font-size:13.5px;
    background:var(--code-bg);color:var(--code);padding:1.5px 5px;border-radius:5px}
  pre{background:var(--code-bg);border:1px solid var(--line);border-radius:10px;padding:14px 16px;overflow:auto;margin:14px 0}
  pre code{background:none;padding:0;font-size:13px}
  table{border-collapse:collapse;width:100%;margin:16px 0;font-size:14.5px;display:block;overflow-x:auto}
  th,td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top}
  th{background:var(--soft);font-weight:700;color:#22304a}
  tbody tr:nth-child(even){background:#fbfcfe}
  em{color:var(--warn)}
  .foot{margin-top:48px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:13.5px}
  @media print{.toc{break-inside:avoid}body{font-size:11pt}}
</style></head>
<body>
<header class="banner">
  <span class="badge">Design approved &middot; mock-only until provisioning</span><span class="badge live">Living document</span>
  <h1 class="title">__TITLE__</h1>
  <p class="sub">Secure service core for the Science Stoa &mdash; plan, runbook, and the basis for the Zeotek architecture &amp; security review.</p>
</header>
<div class="wrap">
  __TOC__
  <article class="doc">
  __BODY__
  </article>
  <div class="foot">Prepared for Denson Smith &middot; living document. Nothing in this plan is built, deployed, or provisioned until the Phase&nbsp;2 steps, which require an explicit go and a spend cap.</div>
</div></body></html>
"""

out = TPL.replace("__TITLE__", title).replace("__TOC__", toc).replace("__BODY__", body)
OUT.write_text(out, encoding="utf-8")
print("wrote", OUT, f"({len(out)} bytes)")
