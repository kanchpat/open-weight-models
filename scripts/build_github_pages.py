import base64
import os
import re
import html

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_DIR, "docs")
ASSETS_DIR = os.path.join(DOCS_DIR, "assets")
WP_DIR = os.path.join(REPO_DIR, "whitepaper")
SERIES_DIR = os.path.join(REPO_DIR, "series")

os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(WP_DIR, exist_ok=True)
os.makedirs(SERIES_DIR, exist_ok=True)

IMG_MAP = {
    "infographic_1_openness_spectrum.png": os.path.join(ASSETS_DIR, "infographic_1_openness_spectrum.png"),
    "infographic_2_ecosystem_stack.png": os.path.join(ASSETS_DIR, "infographic_2_ecosystem_stack.png"),
    "infographic_5_runtime_stack.png": os.path.join(ASSETS_DIR, "infographic_5_runtime_stack.png"),
    "infographic_3_harness_and_system1.png": os.path.join(ASSETS_DIR, "infographic_3_harness_and_system1.png"),
}

B64_IMGS = {}
for k, p in IMG_MAP.items():
    if os.path.exists(p):
        with open(p, "rb") as f:
            B64_IMGS[k] = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")

HERO_IMG_PATH = os.path.join(ASSETS_DIR, "hero_google_cloud_open_weights.jpg")
with open(HERO_IMG_PATH, "rb") as f:
    HERO_IMG_B64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("ascii")

YT_THUMB_PATH = os.path.join(ASSETS_DIR, "youtube_explainer_thumbnail.jpg")
with open(YT_THUMB_PATH, "rb") as f:
    YT_THUMB_B64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("ascii")

def sanitize_external(md_text):
    md_text = md_text.replace("`go/System 1-decision-gemma`", "`System 1` Decision Heads")
    md_text = md_text.replace("; `go/decision-models-customer-signals-explainers`", "")
    md_text = re.sub(r"https://docs\.google\.com/document/d/[a-zA-Z0-9_-]+(?:/edit[^\)\s]*)?", "#enterprise-whitepaper", md_text)
    md_text = re.sub(r"https://notebooklm\.google\.com/notebook/[a-zA-Z0-9_-]+", "#8-references", md_text)
    return md_text

with open(os.path.join(WP_DIR, "enterprise-playbook.md"), "r", encoding="utf-8") as f:
    ent_md_raw = f.read()

ent_md_clean = sanitize_external(ent_md_raw)
tech_md_clean = ""

ent_md_html_src = "\n".join(
    ln for ln in ent_md_clean.splitlines()
    if not ln.startswith("**Authored & Built by:**")
    and not ln.startswith("*Unofficial Google Cloud Practitioner Guide")
)

# Removed technical-deep-dive.md per user preference

MODULES = [
    ("part-02-openmaas-serverless", "Part 2 (Nov 13, 2026): Start Serverless — Building Zero-Ops Open-Weight Agents on Vertex AI OpenMaaS", "Vertex AI OpenMaaS (`Gemma 4 31B/26B`, `Qwen 3.8`, `DeepSeek-V4.1-Flash`)", "Demonstrates why OpenMaaS PayGo (`$0.907/1M` output tokens) beats dedicated self-deploy (`$1.29/1M`, `1.42x` penalty) below `73%` GPU utilization, with cURL and Python SDK tool-calling agent templates."),
    ("part-03-adk-harness-system1", "Part 3 (Nov 13, 2026): 'Don't Train the Model, Evolve the Harness' — Multi-Model Routing & Verification with ADK", "Google ADK + OpenMaaS + `System 1` Single-Pass Verification", "Implements tiered in-harness routing (`64%` lower thread cost) and single-pass `System 1` (`output_tokens: 0`, `35x` faster) pre-submission rubric verification gates (`+16.7pp` accuracy)."),
    ("part-04-cloudrun-vllm-qat", "Part 4 (Nov 20, 2026): When & How to Self-Host — Scale-to-Zero vLLM & QAT Open Models on Cloud Run", "Google Cloud Run GPUs (`vLLM` + `Gemma 4` QAT `E4B`/`26B-A4B`)", "Avoids idle GPU burn on bursty custom containers using Cloud Run scale-to-zero GPUs, `vLLM` prefix caching, and `Gemma 4` Quantization-Aware Training (`FP4`/`INT4` with zero tool-call drift)."),
    ("part-05-agent-runtime-vpc", "Part 5 (Nov 20, 2026): Sovereign & Matter-Isolated Agents — In-VPC Open Weights + System 1 Guardrails on Agent Runtime", "Vertex AI Agent Runtime + `System 1` Guardrails & Google Cloud Model Armor", "Deploys `SHA-256`-pinned open weights inside air-gapped VPCs with custom `vLLM` prefill heads, `System 1` guardrails, and bidirectional PII redaction (*Pattern 5*)."),
    ("part-06-lora-grpo-verifiable-rl", "Part 6 (Dec 4, 2026): Beyond the Prompt Tax — LoRA, <$100 Verifiable RL (GRPO), and Multi-LoRA on Vertex AI", "Vertex AI Training + OpenMaaS Multi-LoRA + `SkyRL` GRPO", "Replaces 10,000-token few-shot prompt bloat with Weight Transfer (`LoRA`/`QLoRA`), single-GPU Verifiable RL (`GRPO`, *Pattern 5*: `<$100`, `+9.6%` F1), and dynamic Multi-LoRA serving."),
    ("part-07-frontier-distillation", "Part 7 (Dec 11, 2026): The 'Frontier-to-Open' Distillation Playbook — 10x Cost Cut & <150 ms TTFT", "Vertex AI Distillation (`Gemini 3.1 Pro` Teacher -> `Gemma 4` Student)", "Uses `Gemini 3.1 Pro` to synthesize rubric-verified domain pairs and distills into compact `Gemma 4` (`26B-A4B` / `E4B`) students for `<150 ms` TTFT at 10% of frontier serving cost (*Patterns 2 & 4*)."),
]

for slug, title, surface, desc in MODULES:
    mdir = os.path.join(SERIES_DIR, slug)
    os.makedirs(mdir, exist_ok=True)
    with open(os.path.join(mdir, "README.md"), "w", encoding="utf-8") as f:
        f.write(
            f"# {title}\n\n"
            f"> **Authored & Built by:** Kanchana Patlolla & Anusha Sabbineni · **With guidance from:** Alan Blount  \n"
            f"> **⚠️ Unofficial Google Guide:** Independent practitioner guide — not an officially supported Google product or official Google Cloud documentation. Views expressed are the authors' own.\n\n"
            f"**Stack & Models:** {surface}\n\n"
            f"## Overview\n{desc}\n\n"
            f"*Code notebooks, Dockerfiles, and video walkthrough links unlock with the weekly Friday release.*\n"
        )

print("Scaffolded repo files and README.")


def md_inline(text):
    def repl_link(m):
        lbl, url = m.group(1), m.group(2)
        target = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        return f'<a href="{url}"{target}>{lbl}</a>'
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_link, text)
    text = re.sub(r"`([^`]+)`", lambda m: f"<code>{html.escape(m.group(1))}</code>", text)
    text = re.sub(r"\*\*\*([^*]+)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = text.replace(r"\$", "$")
    text = text.replace(r"$\rightarrow$", "→")
    return text


WIDGET_LICENSE_HTML = """
<div class="interactive-widget" id="widget-license-inline" data-toc-label="⚡ Interactive: License & Auditability Filter">
  <div class="widget-header">
    <div>
      <span class="widget-badge">⚡ EMBEDDED INTERACTIVE TOOLKIT · SECTION 2.1</span>
      <h4>Open-Weight License, Scale &amp; Data Auditability Triage</h4>
    </div>
    <span class="widget-hint">Adjust your valuation, MAU scale, region, and pre-training data auditability sliders</span>
  </div>
  <div class="tco-sliders">
    <div class="slider-group">
      <div class="slider-label">
        <span>Company Valuation Size</span>
        <strong id="lbl-lic-val">$10B (Enterprise Gate)</strong>
      </div>
      <input type="range" id="sld-lic-val" min="1" max="5" step="1" value="4" oninput="updateLicenseFilter()">
      <div class="slider-ticks"><span>$50M</span><span>$500M</span><span>$2B</span><span>$10B Gate</span><span>$50B+</span></div>
    </div>
    <div class="slider-group">
      <div class="slider-label">
        <span>Monthly Active Users (MAU)</span>
        <strong id="lbl-lic-mau">50M MAU</strong>
      </div>
      <input type="range" id="sld-lic-mau" min="1" max="5" step="1" value="3" oninput="updateLicenseFilter()">
      <div class="slider-ticks"><span>&lt;1M</span><span>10M</span><span>50M</span><span>100M Cap</span><span>700M+ Cap</span></div>
    </div>
    <div class="slider-group">
      <div class="slider-label">
        <span>Region &amp; Sovereignty Policy</span>
        <strong id="lbl-lic-reg">Global (Any Origin)</strong>
      </div>
      <input type="range" id="sld-lic-reg" min="1" max="3" step="1" value="1" oninput="updateLicenseFilter()">
      <div class="slider-ticks"><span>Global (Any Origin)</span><span>US / EU Regulated Only</span><span>EU Sovereign Only</span></div>
    </div>
    <div class="slider-group">
      <div class="slider-label">
        <span>Auditability of Pre-Training Data</span>
        <strong id="lbl-lic-aud">Level 1: Weights Only</strong>
      </div>
      <input type="range" id="sld-lic-aud" min="1" max="3" step="1" value="1" oninput="updateLicenseFilter()">
      <div class="slider-ticks"><span>L1: Weights Only</span><span>L2: Open Recipe</span><span>L3: Full Pre-Training Data</span></div>
    </div>
  </div>
  <div id="license-results-grid" class="license-grid"></div>
</div>
"""

WIDGET_TCO_HTML = """
<div class="interactive-widget" id="widget-tco-inline" data-toc-label="⚡ Interactive: OpenMaaS vs. Self-Hosted TCO">
  <div class="widget-header">
    <div>
      <span class="widget-badge">⚡ EMBEDDED INTERACTIVE TOOLKIT · SECTION 6.1 FINOPS CALCULATOR</span>
      <h4>OpenMaaS PayGo vs. Self-Hosted Dedicated GPU Break-Even Calculator</h4>
    </div>
    <span class="widget-hint">Models the 73% duty-cycle barrier &amp; 8M–30M token/day crossover</span>
  </div>
  <div class="tco-sliders">
    <div class="slider-group">
      <div class="slider-label">
        <span>Daily Output Token Volume</span>
        <strong id="lbl-tok-vol">25M tokens/day (750M/mo)</strong>
      </div>
      <input type="range" id="sld-tok-vol" min="1" max="150" value="25" oninput="updateTcoCalc()">
      <div class="slider-ticks"><span>1M/day (Pilot)</span><span>8M–30M/day (Break-Even Zone)</span><span>150M/day (Fleet Scale)</span></div>
    </div>
    <div class="slider-group">
      <div class="slider-label">
        <span>Dedicated GPU Cluster Duty-Cycle Utilization</span>
        <strong id="lbl-duty">35% Duty Cycle (Spiky Enterprise Traffic)</strong>
      </div>
      <input type="range" id="sld-duty" min="10" max="95" value="35" oninput="updateTcoCalc()">
      <div class="slider-ticks"><span>15% (Spiky)</span><span>50% (Business Hrs)</span><span>73% (OpenMaaS Break-Even)</span><span>95% (Batch)</span></div>
    </div>
  </div>
  <div id="tco-bars-container" class="tco-bars"></div>
  <div id="tco-verdict-box" class="tco-verdict"></div>
</div>
"""

WIDGET_QUADRANT_HTML = """
<div class="interactive-widget" id="widget-quadrant-inline" data-toc-label="⚡ Interactive: Workload & Architecture Router">
  <div class="widget-header">
    <div>
      <span class="widget-badge">⚡ EMBEDDED INTERACTIVE TOOLKIT · SECTION 6.2 WORKLOAD ROUTER</span>
      <h4>Interactive 2×2 Workload Router &amp; Google Cloud Architecture Mapper</h4>
    </div>
    <span class="widget-hint">Click any quadrant to inspect its architecture &amp; jump to the matching Google Cloud series module</span>
  </div>
  <div class="quadrant-selector-grid">
    <button class="q-card q-blue active" onclick="selectQuadrant('Q2', this)">
      <div class="q-tag">QUADRANT II · GOVERN &amp; AUDIT</div>
      <div class="q-title">Sovereign &amp; In-VPC Open Weights</div>
      <div class="q-sub">High Sovereignty · Regulated PII/PHI/Legal · SHA-256 Pinning</div>
    </button>
    <button class="q-card q-green" onclick="selectQuadrant('Q1', this)">
      <div class="q-tag">QUADRANT I · OWN THE MOAT (LEADERS)</div>
      <div class="q-title">Post-Trained &amp; Surgically Customized</div>
      <div class="q-sub">High Scale + Custom Encoders, Prefill Rankers &amp; &lt;$100 GRPO RL</div>
    </button>
    <button class="q-card q-slate" onclick="selectQuadrant('Q3', this)">
      <div class="q-tag">QUADRANT III · RENT FOR AGILITY</div>
      <div class="q-title">Closed Frontier APIs &amp; Serverless OpenMaaS</div>
      <div class="q-sub">Spiky QPS (&lt;73% Duty Cycle) · $0 Idle Burn · Frontier R&amp;D</div>
    </button>
    <button class="q-card q-amber" onclick="selectQuadrant('Q4', this)">
      <div class="q-tag">QUADRANT IV · SCALE &amp; OPTIMIZE FINOPS</div>
      <div class="q-title">Sparse Open Weights, Harnesses &amp; System 1</div>
      <div class="q-sub">High-Velocity Coding, ADK Routing &amp; output_tokens: 0 Triage</div>
    </button>
  </div>
  <div id="quadrant-detail-panel" class="quadrant-detail"></div>
</div>
"""


def md_to_html(md_text, inject_widgets=False, prefix=""):
    lines = md_text.splitlines()
    out = []
    in_ul = False
    in_ol = False
    in_bq = False
    in_table = False
    table_rows = []
    last_h3 = ""

    def close_lists():
        nonlocal in_ul, in_ol, in_bq
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False
        if in_bq:
            out.append("</div>")
            in_bq = False

    def flush_table():
        nonlocal in_table, table_rows, last_h3
        if not in_table:
            return
        in_table = False
        if len(table_rows) >= 2:
            headers = [c.strip() for c in table_rows[0].strip("|").split("|")]
            body_rows = table_rows[2:]
            out.append('<div class="table-wrap"><table class="whitepaper-table"><thead><tr>')
            for h in headers:
                out.append(f"<th>{md_inline(h)}</th>")
            out.append("</tr></thead><tbody>")
            for r in body_rows:
                cols = [c.strip() for c in r.strip("|").split("|")]
                out.append("<tr>")
                for c in cols:
                    cell_html = md_inline(c)
                    out.append(f"<td>{cell_html}</td>")
                out.append("</tr>")
            out.append("</tbody></table></div>")
        table_rows = []
        if inject_widgets and "2.1 Navigating the Three Broad Licensing" in last_h3:
            out.append(WIDGET_LICENSE_HTML)

    for raw_line in lines:
        line = raw_line.rstrip()
        if line.startswith("|") and line.endswith("|"):
            close_lists()
            in_table = True
            table_rows.append(line)
            continue
        else:
            flush_table()

        if not line.strip():
            close_lists()
            continue

        m_img = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line.strip())
        if m_img:
            close_lists()
            alt, path = m_img.group(1), m_img.group(2)
            bname = os.path.basename(path)
            src = B64_IMGS.get(bname, path)
            out.append(f'<figure class="arxiv-figure"><img src="{src}" alt="{html.escape(alt)}"><figcaption>{html.escape(alt)}</figcaption></figure>')
            continue

        if line.startswith("# "):
            close_lists()
            continue
        if line.startswith("## "):
            close_lists()
            h_txt = line[3:].strip()
            slug = prefix + re.sub(r"[^a-z0-9]+", "-", h_txt.lower()).strip("-")
            if h_txt.startswith("8. Reference"):
                out.append(f'<details class="refs-accordion" id="{slug}"><summary>8. References &amp; Primary Sources (Click to expand)</summary><div class="refs-body">')
            else:
                out.append(f'<h2 id="{slug}">{md_inline(h_txt)}</h2>')
            last_h3 = h_txt
            continue
        if line.startswith("### "):
            close_lists()
            h_txt = line[4:].strip()
            slug = prefix + re.sub(r"[^a-z0-9]+", "-", h_txt.lower()).strip("-")
            out.append(f'<h3 id="{slug}">{md_inline(h_txt)}</h3>')
            last_h3 = h_txt
            continue

        if line.startswith(">"):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_bq:
                out.append('<div class="callout-box">')
                in_bq = True
            bq_content = line.lstrip("> ").strip()
            if bq_content.startswith("- "):
                out.append(f'<div style="margin:6px 0 6px 12px;">• {md_inline(bq_content[2:])}</div>')
            else:
                out.append(f'<p style="margin:0 0 8px 0;">{md_inline(bq_content)}</p>')
            continue

        m_ul = re.match(r"^(\s*)-\s+(.*)$", line)
        if m_ul:
            if in_bq:
                out.append("</div>")
                in_bq = False
            if in_ol and not m_ul.group(1):
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            item_html = md_inline(m_ul.group(2))
            out.append(f"<li>{item_html}</li>")
            if inject_widgets and "6.1 The 73% Duty-Cycle Rule" in last_h3 and "Enterprise Mitigation:" in m_ul.group(2):
                close_lists()
                out.append(WIDGET_TCO_HTML)
                last_h3 = ""
            continue

        m_ol = re.match(r"^(\d+)\.\s+(.*)$", line)
        if m_ol:
            if in_bq:
                out.append("</div>")
                in_bq = False
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{md_inline(m_ol.group(2))}</li>")
            continue

        close_lists()
        out.append(f"<p>{md_inline(line)}</p>")
        if inject_widgets and "6.2 Interactive Workload & Architecture Router" in last_h3:
            out.append(WIDGET_QUADRANT_HTML)
            last_h3 = ""

    close_lists()
    flush_table()
    joined = "\n".join(out)
    if '<details class="refs-accordion"' in joined:
        joined += "</div></details>"
    return joined

ent_body_html = md_to_html(ent_md_html_src, inject_widgets=True, prefix="")
tech_body_html = md_to_html(tech_md_clean, inject_widgets=False, prefix="tech-")

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Open-Weight AI Models on Google Cloud — Unofficial Enterprise Architect's Guide</title>
<meta name="description" content="Interactive enterprise architecture playbook, FinOps 73% duty-cycle calculator, license-triage filter, 5-minute explainer video, and 7-part Google Cloud code series for open-weight AI models.">
<link rel="canonical" href="https://openweights.cloudrace.info/">
<meta property="og:title" content="Open-Weight AI Models — Enterprise Architect's Playbook &amp; Toolkit">
<meta property="og:description" content="56% of gateway tokens at 14% of spend: interactive license filter, 73% GPU duty-cycle FinOps calculator, 5-min video walkthrough, and 7-part Google Cloud code series.">
<meta property="og:url" content="https://openweights.cloudrace.info/">
<meta property="og:type" content="website">
<meta property="og:image" content="https://openweights.cloudrace.info/assets/youtube_explainer_thumbnail.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Open-Weight AI Models — Enterprise Architect's Playbook &amp; Toolkit">
<meta name="twitter:description" content="Interactive license filter, 73% GPU duty-cycle FinOps calculator, 5-min explainer video, and 7-part Google Cloud code series.">
<meta name="twitter:image" content="https://openweights.cloudrace.info/assets/youtube_explainer_thumbnail.jpg">
<style>
  :root {{
    --bg-app: #FFFFFF;
    --bg-sidebar: #FBFBFB;
    --bg-subtle: #F8FAFC;
    --border-subtle: #DFE3E7;
    --text-primary: #1F1F1F;
    --text-secondary: #444746;
    --text-muted: #5E5E5E;
    --accent-primary: #0B57D0;
    --accent-primary-bg: #EFF6FF;
    --heading-h2: #1F1F1F;
    --heading-h3: #0B57D0;
    --topbar-height: 60px;
    --sans: "Google Sans Flex", "Google Sans", -apple-system, BlinkMacSystemFont, "Inter", system-ui, sans-serif;
    --code: "Google Sans Code", "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
    --pass: #146C2E;
    --pass-surface: #E6F4EA;
    --surface: #F0F4F9;
    --surface-2: #F8FAFD;
  }}
  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; scroll-padding-top: 84px; }}
  body {{
    margin: 0;
    padding: 0;
    background-color: var(--bg-app);
    color: var(--text-primary);
    font-family: var(--sans);
    font-size: 16px;
    line-height: 1.65;
    -webkit-font-smoothing: antialiased;
  }}

  /* =========================================================
     1. TOP NAVIGATION BAR (google.github.io/agents-cli Style)
     ========================================================= */
  .docs-topbar {{
    position: sticky;
    top: 0;
    z-index: 300;
    height: var(--topbar-height);
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border-subtle);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 clamp(20px, 4vw, 48px);
    gap: 24px;
  }}
  .topbar-left {{
    display: flex;
    align-items: center;
    gap: 10px;
    flex: none;
  }}
  .brand-mark {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border-radius: 7px;
    background: linear-gradient(135deg, #4285F4 0%, #0B57D0 100%);
    color: #FFFFFF;
    font-family: var(--code);
    font-weight: 600;
    font-size: 14px;
  }}
  .brand-title {{
    font-family: var(--code);
    font-weight: 500;
    font-size: 16px;
    letter-spacing: -0.02em;
    color: var(--text-primary);
    white-space: nowrap;
  }}
  .brand-badge {{
    font-size: 11px;
    font-weight: 600;
    background: var(--surface);
    color: var(--text-secondary);
    border: 1px solid var(--border-subtle);
    padding: 2px 8px;
    border-radius: 999px;
  }}

  /* Slash-Prefixed Monospace Nav (agents-cli style) */
  .topbar-center {{
    display: flex;
    align-items: stretch;
    gap: 20px;
    height: 100%;
    overflow-x: auto;
  }}
  .slash-nav-link {{
    font-family: var(--code);
    font-size: 14.5px;
    font-weight: 450;
    letter-spacing: -0.01em;
    color: var(--text-secondary);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    white-space: nowrap;
    cursor: pointer;
    background: transparent;
    border: none;
    padding: 0 2px;
    position: relative;
  }}
  .slash-nav-link .slug {{
    color: #9AA0A6;
    margin-right: 1px;
  }}
  .slash-nav-link:hover {{
    color: var(--text-primary);
    text-decoration: none;
  }}
  .slash-nav-link.active {{
    color: var(--text-primary);
    font-weight: 550;
  }}
  .slash-nav-link.active .slug {{
    color: var(--accent-primary);
  }}
  .slash-nav-link.active::after {{
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: var(--text-primary);
  }}

  .topbar-right {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-left: auto;
  }}
  .top-jump-pill {{
    background: var(--surface);
    color: var(--accent-primary);
    border: 1px solid transparent;
    padding: 6px 11px;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
    white-space: nowrap;
    transition: all 0.15s ease;
  }}
  .top-jump-pill:hover {{
    border-color: var(--border-subtle);
    background: #E8F0FE;
    text-decoration: none;
  }}
  .util-btn {{
    background: #FFFFFF;
    color: var(--text-secondary);
    border: 1px solid var(--border-subtle);
    padding: 6px 11px;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    white-space: nowrap;
  }}
  .util-btn:hover {{
    background: var(--surface);
    color: var(--text-primary);
  }}

  /* =========================================================
     1B. GOOGLE CLOUD × OPEN-WEIGHT AI VARIANT HERO, QUESTIONS & MODELS
     ========================================================= */
  .gc-hero-wrap {{
    background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%);
    border-bottom: 1px solid var(--border-subtle);
    padding: 36px clamp(20px, 4vw, 56px) 36px;
    position: relative;
    overflow: hidden;
  }}
  .gc-hero-wrap::before {{
    content: "";
    position: absolute;
    inset: 0;
    pointer-events: none;
    background:
      radial-gradient(38% 50% at 15% 20%, rgba(66, 133, 244, 0.10), transparent 70%),
      radial-gradient(35% 45% at 85% 25%, rgba(52, 168, 83, 0.08), transparent 70%),
      radial-gradient(30% 40% at 75% 80%, rgba(251, 188, 4, 0.08), transparent 70%);
  }}
  .gc-hero-inner {{
    max-width: 1380px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }}
  .gc-split-grid {{
    display: grid;
    grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
    gap: clamp(24px, 3.5vw, 48px);
    align-items: center;
    margin-bottom: 34px;
  }}
  @media (max-width: 980px) {{
    .gc-split-grid {{ grid-template-columns: 1fr; }}
  }}
  .gc-eyebrow-row {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
    margin-bottom: 14px;
  }}
  .gc-pill-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #E8F0FE;
    color: #0B57D0;
    border: 1px solid #BFDBFE;
    font-family: var(--code);
    font-size: 11.5px;
    font-weight: 600;
    padding: 4px 11px;
    border-radius: 999px;
    letter-spacing: 0.02em;
  }}
  .gc-unofficial-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #FFFBEB;
    color: #92400E;
    border: 1px solid #FCD34D;
    font-family: var(--code);
    font-size: 11.5px;
    font-weight: 700;
    padding: 4px 11px;
    border-radius: 999px;
    letter-spacing: 0.02em;
  }}
  .unofficial-top-ribbon {{
    background: #FFFBEB;
    border-bottom: 1px solid #FDE68A;
    color: #78350F;
    font-size: 12.5px;
    line-height: 1.45;
    padding: 8px clamp(20px, 4vw, 48px);
    text-align: center;
  }}
  .unofficial-top-ribbon strong {{
    color: #92400E;
  }}
  .author-credit-panel {{
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-left: 4px solid #0B57D0;
    border-radius: 12px;
    padding: 13px 16px;
    margin: 0 0 20px 0;
    max-width: 64ch;
    box-shadow: 0 4px 14px -6px rgba(15, 23, 42, 0.08);
  }}
  .author-credit-chips {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
  }}
  .author-chip {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1E3A8A;
    font-size: 12.5px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 999px;
  }}
  .author-chip.guidance {{
    background: #F8FAFC;
    border-color: #CBD5E1;
    color: #334155;
  }}
  .author-initials {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #0B57D0;
    color: #FFFFFF;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.02em;
  }}
  .author-chip.guidance .author-initials {{
    background: #475569;
  }}
  .author-disclaimer-line {{
    font-size: 12px;
    line-height: 1.45;
    color: #475569;
    padding-top: 7px;
    border-top: 1px dashed #E2E8F0;
  }}
  .site-global-footer {{
    border-top: 1px solid var(--border-subtle);
    background: #F8FAFC;
    padding: 26px clamp(20px, 4vw, 56px);
    font-size: 13px;
    color: #475569;
  }}
  .site-global-footer-inner {{
    max-width: 1380px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
  }}
  .gc-live-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #ECFDF5;
    color: #065F46;
    border: 1px solid #A7F3D0;
    font-size: 11.5px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 999px;
  }}
  .gc-hero-title {{
    font-size: clamp(30px, 3.4vw, 48px);
    line-height: 1.08;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: var(--text-primary);
    margin: 0 0 14px 0;
  }}
  .gc-hero-title .hl {{
    color: var(--accent-primary);
  }}
  .gc-hero-sub {{
    font-size: 16.5px;
    line-height: 1.52;
    color: var(--text-secondary);
    margin: 0 0 20px 0;
    max-width: 62ch;
  }}
  .gc-cta-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 16px;
  }}
  .btn-pill-dark {{
    border: 1px solid #0B57D0;
    background: #0B57D0;
    color: #FFFFFF;
    height: 38px;
    padding: 0 16px;
    border-radius: 999px;
    font-size: 13.5px;
    font-weight: 500;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
    transition: all 0.15s ease;
  }}
  .btn-pill-dark:hover {{
    background: #1D4ED8;
    color: #FFFFFF;
    text-decoration: none;
  }}
  .btn-pill-ghost {{
    border: 1px solid var(--border-subtle);
    background: #FFFFFF;
    color: var(--text-primary);
    height: 38px;
    padding: 0 15px;
    border-radius: 999px;
    font-size: 13.5px;
    font-weight: 500;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
    transition: all 0.15s ease;
  }}
  .btn-pill-ghost:hover {{
    border-color: #0B57D0;
    color: #0B57D0;
    background: #F8FAFC;
    text-decoration: none;
  }}
  .gc-visual-card {{
    background: #FFFFFF;
    border: 1px solid #DBEAFE;
    border-radius: 16px;
    padding: 14px;
    box-shadow: 0 18px 40px -20px rgba(11, 87, 208, 0.22);
  }}
  .gc-visual-card img {{
    width: 100%;
    height: auto;
    display: block;
    border-radius: 10px;
    border: 1px solid #F1F5F9;
  }}
  .gc-surface-strip {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-top: 10px;
  }}
  @media (max-width: 640px) {{
    .gc-surface-strip {{ grid-template-columns: 1fr 1fr; }}
  }}
  .gc-surf-chip {{
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 6px 8px;
    font-size: 11.5px;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s ease;
    color: var(--text-primary);
    text-decoration: none;
    display: block;
  }}
  .gc-surf-chip:hover {{
    border-color: #0B57D0;
    background: #EFF6FF;
    text-decoration: none;
  }}
  .gc-surf-chip strong {{
    display: block;
    color: #0B57D0;
    font-size: 11.5px;
  }}
  .gc-surf-chip span {{
    font-size: 10.5px;
    color: var(--text-muted);
  }}

  /* Hero Video Trigger Pill + Above-the-Scroll 5-Min Video Spotlight */
  .btn-pill-video {{
    border: 1px solid #0F172A;
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
    color: #FFFFFF;
    height: 38px;
    padding: 0 15px;
    border-radius: 999px;
    font-size: 13.5px;
    font-weight: 600;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 7px;
    text-decoration: none;
    box-shadow: 0 6px 16px -6px rgba(15, 23, 42, 0.35);
    transition: all 0.15s ease;
  }}
  .btn-pill-video:hover {{
    background: linear-gradient(135deg, #0B57D0 0%, #1D4ED8 100%);
    border-color: #0B57D0;
    color: #FFFFFF;
    transform: translateY(-1px);
    text-decoration: none;
  }}
  .vid-dur-tag {{
    font-family: var(--code);
    font-size: 10.5px;
    font-weight: 700;
    background: rgba(56, 189, 248, 0.22);
    color: #7DD3FC;
    padding: 1px 7px;
    border-radius: 999px;
  }}

  .gc-video-spotlight {{
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 55%, #EFF6FF 100%);
    border: 1px solid #BFDBFE;
    border-radius: 18px;
    padding: 18px 22px;
    margin-bottom: 22px;
    box-shadow: 0 16px 36px -20px rgba(11, 87, 208, 0.22);
    display: grid;
    grid-template-columns: minmax(320px, 430px) minmax(0, 1fr);
    gap: 24px;
    align-items: center;
    scroll-margin-top: 84px;
  }}
  .gc-video-spotlight.is-playing {{
    grid-template-columns: minmax(360px, 540px) minmax(0, 1fr);
  }}
  @media (max-width: 1020px) {{
    .gc-video-spotlight,
    .gc-video-spotlight.is-playing {{
      grid-template-columns: 1fr;
    }}
  }}
  .yt-player-stage {{
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    border-radius: 12px;
    overflow: hidden;
    background: #060A15;
    border: 1px solid #CBD5E1;
    box-shadow: 0 14px 30px -12px rgba(15, 23, 42, 0.35);
  }}
  .yt-player-stage iframe {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: 0;
  }}
  .yt-poster-btn {{
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    padding: 0;
    border: 0;
    background: #060A15;
    cursor: pointer;
    display: block;
  }}
  .yt-poster-btn img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.25s ease, filter 0.25s ease;
  }}
  .yt-poster-btn:hover img {{
    transform: scale(1.025);
    filter: brightness(1.06);
  }}
  .yt-play-ring {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: rgba(220, 38, 38, 0.94);
    border: 2.5px solid rgba(255, 255, 255, 0.92);
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.55);
    display: grid;
    place-items: center;
    transition: transform 0.18s ease, background 0.18s ease;
  }}
  .yt-poster-btn:hover .yt-play-ring {{
    transform: translate(-50%, -50%) scale(1.09);
    background: #EF4444;
  }}
  .yt-play-ring svg {{
    width: 26px;
    height: 26px;
    fill: #FFFFFF;
    margin-left: 3px;
  }}
  .yt-dur-badge {{
    position: absolute;
    right: 10px;
    bottom: 10px;
    background: rgba(6, 10, 21, 0.88);
    color: #F8FAFC;
    border: 1px solid rgba(148, 163, 184, 0.35);
    font-family: var(--code);
    font-size: 11px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 6px;
  }}
  .yt-spot-meta {{
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}
  .yt-spot-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .yt-eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #0B57D0;
    background: #DBEAFE;
    padding: 4px 10px;
    border-radius: 999px;
  }}
  .yt-ext-link {{
    font-size: 12px;
    font-weight: 600;
    color: #334155;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    padding: 4px 11px;
    border-radius: 999px;
    text-decoration: none;
    transition: all 0.15s ease;
  }}
  .yt-ext-link:hover {{
    border-color: #0B57D0;
    color: #0B57D0;
    text-decoration: none;
  }}
  .yt-spot-title {{
    margin: 0;
    font-size: 19px;
    font-weight: 750;
    color: #0F172A;
    line-height: 1.28;
    letter-spacing: -0.015em;
  }}
  .yt-spot-sub {{
    margin: 0;
    font-size: 13px;
    color: #475569;
    line-height: 1.45;
  }}
  .yt-chap-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
    margin-top: 2px;
  }}
  @media (max-width: 720px) {{
    .yt-chap-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  }}
  .yt-chap-btn {{
    text-align: left;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 9px;
    padding: 7px 10px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 12px;
    color: #1E293B;
    font-weight: 600;
    transition: all 0.14s ease;
  }}
  .yt-chap-btn:hover,
  .yt-chap-btn.active {{
    border-color: #0B57D0;
    background: #EFF6FF;
    color: #0B57D0;
  }}
  .yt-chap-time {{
    font-family: var(--code);
    font-size: 10.5px;
    font-weight: 700;
    color: #0B57D0;
    background: #EFF6FF;
    padding: 2px 6px;
    border-radius: 5px;
    flex-shrink: 0;
  }}
  .yt-chap-btn.active .yt-chap-time {{
    background: #0B57D0;
    color: #FFFFFF;
  }}
  .yt-chap-lbl {{
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }}

  /* 5 Key Enterprise Architect Questions Grid (Visual Metric Bento) */
  .gc-questions-box {{
    background: rgba(255, 255, 255, 0.92);
    backdrop-filter: blur(10px);
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 22px 24px;
    box-shadow: 0 16px 36px -18px rgba(15, 23, 42, 0.12);
  }}
  .gc-sec-hdr {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
  }}
  .gc-sec-hdr h2 {{
    margin: 0;
    padding: 0;
    border: none;
    font-size: 18.5px;
    font-weight: 700;
    letter-spacing: -0.015em;
    color: var(--text-primary);
  }}
  .gc-sec-hdr span {{
    font-size: 12px;
    font-weight: 500;
    color: #0B57D0;
    background: #EFF6FF;
    padding: 4px 10px;
    border-radius: 999px;
  }}
  .gc-q-grid {{
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 14px;
  }}
  @media (max-width: 1180px) {{
    .gc-q-grid {{ grid-template-columns: repeat(auto-fill, minmax(225px, 1fr)); }}
  }}
  .gc-q-card {{
    background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 16px 15px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    cursor: pointer;
    transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
    text-align: left;
    position: relative;
    overflow: hidden;
  }}
  .gc-q-card::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3.5px;
    background: var(--q-accent, #0B57D0);
  }}
  .gc-q-card:hover {{
    transform: translateY(-4px);
    border-color: var(--q-accent, #0B57D0);
    box-shadow: 0 14px 28px -12px rgba(15, 23, 42, 0.16);
    background: #FFFFFF;
  }}
  .gc-q-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
  }}
  .gc-q-icon {{
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: var(--q-bg, #EFF6FF);
    color: var(--q-accent, #0B57D0);
    display: grid;
    place-items: center;
  }}
  .gc-q-icon svg {{
    width: 19px;
    height: 19px;
  }}
  .gc-q-num {{
    font-family: var(--code);
    font-size: 11px;
    font-weight: 700;
    color: var(--q-accent, #0B57D0);
    background: var(--q-bg, #EFF6FF);
    padding: 3px 8px;
    border-radius: 999px;
  }}
  .gc-q-title {{
    font-size: 15px;
    font-weight: 700;
    color: #0F172A;
    line-height: 1.28;
    margin-bottom: 10px;
    letter-spacing: -0.01em;
  }}
  .gc-q-stat {{
    background: var(--q-bg, #EFF6FF);
    border-radius: 9px;
    padding: 8px 10px;
    margin-bottom: 10px;
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 6px;
  }}
  .gc-q-stat strong {{
    font-size: 16px;
    font-weight: 800;
    color: var(--q-accent, #0B57D0);
    letter-spacing: -0.02em;
  }}
  .gc-q-stat span {{
    font-size: 11px;
    font-weight: 600;
    color: #475569;
  }}
  .gc-q-pills {{
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    margin-bottom: 12px;
  }}
  .gc-q-pill {{
    font-family: var(--code);
    font-size: 10.5px;
    font-weight: 500;
    background: #F1F5F9;
    color: #334155;
    padding: 2px 7px;
    border-radius: 5px;
  }}
  .gc-q-foot {{
    font-size: 12px;
    font-weight: 700;
    color: var(--q-accent, #0B57D0);
    padding-top: 9px;
    border-top: 1px solid #F1F5F9;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }}

  /* Open-Weight Models Directory Showcase Section */
  .models-dir-sec {{
    max-width: 1380px;
    margin: 0 auto;
    padding: 28px clamp(20px, 4vw, 56px) 32px;
    border-bottom: 1px solid var(--border-subtle);
    background: #FFFFFF;
  }}
  .models-filter-bar {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
  }}
  .m-filter-btn {{
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    color: var(--text-secondary);
    padding: 6px 13px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
  }}
  .m-filter-btn:hover {{
    border-color: #0B57D0;
    color: #0B57D0;
  }}
  .m-filter-btn.active {{
    background: #0B57D0;
    border-color: #0B57D0;
    color: #FFFFFF;
    font-weight: 600;
  }}
  .models-showcase-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(295px, 1fr));
    gap: 12px;
  }}
  .m-show-card {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 13px 15px;
    font-size: 12.5px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.15s ease;
  }}
  .m-show-card:hover {{
    border-color: #93C5FD;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
  }}
  .m-show-top {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 6px;
  }}
  .m-show-name {{
    font-size: 14px;
    font-weight: 700;
    color: #0F172A;
  }}
  .m-show-meta {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 8px;
    font-size: 11px;
  }}
  .m-tag-chip {{
    background: #F1F5F9;
    color: #334155;
    padding: 2px 7px;
    border-radius: 5px;
    font-family: var(--code);
    font-size: 11px;
  }}
  .m-cloud-bar {{
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px dashed #E2E8F0;
    font-size: 11.5px;
    color: #0B57D0;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  /* Google 4-color micro-line */
  .google-accent-line {{
    height: 2px;
    width: 100%;
    background: linear-gradient(90deg, #4285F4 0%, #4285F4 25%, #EA4335 25%, #EA4335 50%, #FBBC04 50%, #FBBC04 75%, #34A853 75%, #34A853 100%);
  }}

  /* =========================================================
     2. THREE-PANE DOCS SHELL (Left Nav + Center Paper + Right TOC)
     ========================================================= */
  .docs-shell {{
    display: grid;
    grid-template-columns: 284px minmax(0, 1fr);
    max-width: 1480px;
    margin: 0 auto;
    align-items: start;
  }}

  @media (max-width: 1200px) {{
    .docs-shell {{
      grid-template-columns: 256px minmax(0, 1fr);
    }}
    .docs-right-toc {{
      display: none;
    }}
  }}
  @media (max-width: 860px) {{
    .docs-shell {{
      grid-template-columns: 1fr;
    }}
    .docs-left-sidebar {{
      display: none;
    }}
    .topbar-right .top-jump-pill {{
      display: none;
    }}
  }}

  /* =========================================================
     3. LEFT SIDEBAR (Curriculum & Guide Section Tree)
     ========================================================= */
  .docs-left-sidebar {{
    position: sticky;
    top: calc(var(--topbar-height) + 2px);
    height: calc(100vh - var(--topbar-height) - 2px);
    overflow-y: auto;
    border-right: 1px solid var(--border-subtle);
    background: var(--bg-sidebar);
    padding: 22px 16px 40px 20px;
    font-size: 13.5px;
  }}
  .nav-group {{
    margin-bottom: 22px;
  }}
  .nav-group-title {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6B7280;
    margin: 0 0 8px 8px;
  }}
  .nav-list {{
    list-style: none;
    margin: 0;
    padding: 0;
  }}
  .nav-item {{
    margin-bottom: 2px;
  }}
  .nav-link {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 6px;
    padding: 6px 10px;
    border-radius: 6px;
    color: #374151;
    text-decoration: none;
    font-size: 13px;
    line-height: 1.35;
    cursor: pointer;
    transition: all 0.12s ease;
  }}
  .nav-link:hover {{
    background: #F3F4F6;
    color: #111827;
    text-decoration: none;
  }}
  .nav-link.active {{
    background: var(--accent-primary-bg);
    color: var(--accent-primary);
    font-weight: 600;
  }}
  .nav-link.sub-link {{
    padding-left: 20px;
    font-size: 12.5px;
    color: #4B5563;
  }}
  .nav-link.sub-link.active {{
    color: var(--accent-primary);
    font-weight: 600;
  }}
  .interactive-tag {{
    font-size: 10px;
    font-weight: 700;
    background: #DBEAFE;
    color: #1E40AF;
    padding: 1px 6px;
    border-radius: 999px;
    flex-shrink: 0;
  }}

  /* =========================================================
     4. CENTER CONTENT PANE (Clean Claude Docs Reading Flow)
     ========================================================= */
  .docs-main-pane {{
    padding: 36px 56px 80px;
    max-width: 1080px;
    width: 100%;
    margin: 0 auto;
  }}

  @media (max-width: 760px) {{
    .docs-main-pane {{ padding: 24px 18px 60px; }}
  }}

  .breadcrumbs {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12.5px;
    font-weight: 500;
    color: var(--text-muted);
    margin-bottom: 14px;
  }}
  .breadcrumbs span.crumb-active {{
    color: var(--accent-primary);
    font-weight: 600;
  }}

  .view-section {{ display: none; }}
  .view-section.active {{ display: block; }}

  .whitepaper-header {{
    border-bottom: 1px solid var(--border-subtle);
    padding-bottom: 22px;
    margin-bottom: 26px;
  }}
  .whitepaper-title {{
    font-size: 30px;
    font-weight: 700;
    color: #111827;
    margin: 0 0 12px 0;
    line-height: 1.22;
    letter-spacing: -0.02em;
  }}
  .whitepaper-sub {{
    font-size: 13.5px;
    color: var(--text-muted);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
  }}

  /* In-paper Section & Interactive Calculator Strip */
  .quick-jump-strip {{
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
    font-size: 12.5px;
  }}
  .quick-jump-links {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }}
  .jump-pill {{
    background: #FFFFFF;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
    padding: 5px 11px;
    border-radius: 6px;
    text-decoration: none;
    font-weight: 600;
    font-size: 12px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
  }}
  .jump-pill:hover {{
    background: #EFF6FF;
    text-decoration: none;
  }}

  .single-col-body {{
    max-width: 100%;
  }}
  details.refs-accordion {{
    margin-top: 36px;
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    background: #F9FAFB;
    padding: 12px 18px;
  }}
  details.refs-accordion summary {{
    font-weight: 600;
    font-size: 14px;
    color: var(--text-primary);
    cursor: pointer;
    user-select: none;
  }}
  details.refs-accordion .refs-body {{
    margin-top: 14px;
    font-size: 13px;
  }}

  h2 {{
    font-size: 22px;
    font-weight: 700;
    color: var(--heading-h2);
    margin: 40px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-subtle);
    letter-spacing: -0.01em;
    break-after: avoid;
    column-span: all;
  }}
  h3 {{
    font-size: 17px;
    font-weight: 600;
    color: var(--heading-h3);
    margin: 28px 0 10px 0;
    break-after: avoid;
  }}
  p {{ margin: 0 0 14px 0; color: var(--text-secondary); }}
  ul, ol {{ margin: 0 0 16px 0; padding-left: 22px; color: var(--text-secondary); }}
  li {{ margin-bottom: 7px; }}
  strong {{ color: var(--text-primary); }}
  a {{ color: var(--accent-primary); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  code {{
    font-family: 'JetBrains Mono', 'Roboto Mono', monospace;
    font-size: 12.5px;
    background: #F3F4F6;
    color: #111827;
    padding: 2px 5px;
    border-radius: 4px;
    border: 1px solid #E5E7EB;
  }}

  /* =========================================================
     5. RIGHT SIDEBAR ("On this page" Scroll-Spy TOC)
     ========================================================= */
  .docs-right-toc {{
    position: sticky;
    top: calc(var(--topbar-height) + 2px);
    height: calc(100vh - var(--topbar-height) - 2px);
    overflow-y: auto;
    padding: 28px 20px 40px 16px;
    font-size: 12.5px;
  }}
  .toc-header {{
    font-size: 11.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #111827;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .toc-list {{
    list-style: none;
    margin: 0;
    padding: 0;
    border-left: 1px solid #E5E7EB;
  }}
  .toc-item {{
    margin: 0;
  }}
  .toc-link {{
    display: block;
    padding: 5px 0 5px 12px;
    margin-left: -1px;
    border-left: 2px solid transparent;
    color: #6B7280;
    text-decoration: none;
    line-height: 1.35;
    transition: all 0.12s ease;
  }}
  .toc-link:hover {{
    color: #111827;
    text-decoration: none;
  }}
  .toc-link.toc-h3 {{
    padding-left: 22px;
    font-size: 12px;
  }}
  .toc-link.toc-widget {{
    padding-left: 22px;
    font-size: 12px;
    color: #1D4ED8;
    font-weight: 600;
  }}
  .toc-link.active {{
    color: var(--accent-primary);
    border-left-color: var(--accent-primary);
    font-weight: 600;
  }}

  .toc-toolkit-card {{
    margin-top: 22px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 12px;
  }}
  .toc-toolkit-title {{
    font-size: 11.5px;
    font-weight: 700;
    color: #1E3A8A;
    margin-bottom: 8px;
  }}
  .toc-toolkit-btn {{
    display: block;
    width: 100%;
    text-align: left;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 6px 9px;
    font-size: 11.5px;
    font-weight: 600;
    color: #1E40AF;
    margin-bottom: 6px;
    cursor: pointer;
    transition: all 0.12s ease;
  }}
  .toc-toolkit-btn:hover {{
    background: #EFF6FF;
    border-color: #93C5FD;
  }}

  /* =========================================================
     6. TABLES, FIGURES & CALLOUTS
     ========================================================= */
  .table-wrap {{
    margin: 18px 0 24px;
    overflow-x: auto;
    break-inside: avoid;
    column-span: all;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
  }}
  table.whitepaper-table {{
    width: 100%;
    border-collapse: collapse;
    background-color: #FFFFFF;
    font-size: 13px;
    line-height: 1.48;
  }}
  table.whitepaper-table th {{
    background-color: #F9FAFB;
    color: #111827;
    font-weight: 600;
    text-align: left;
    padding: 10px 14px;
    border-bottom: 1px solid #E5E7EB;
  }}
  table.whitepaper-table td {{
    padding: 10px 14px;
    border-bottom: 1px solid #F3F4F6;
    vertical-align: top;
    color: #374151;
  }}
  table.whitepaper-table tr:last-child td {{
    border-bottom: none;
  }}
  .arxiv-figure {{
    margin: 22px 0 26px;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 14px;
    break-inside: avoid;
    column-span: all;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  }}
  .arxiv-figure img {{
    width: 100%;
    height: auto;
    display: block;
    border-radius: 6px;
  }}
  .arxiv-figure figcaption {{
    margin-top: 10px;
    font-size: 12.5px;
    color: var(--text-muted);
    text-align: center;
    font-weight: 500;
  }}
  .callout-box {{
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #1A73E8;
    padding: 16px 20px;
    margin: 18px 0 24px;
    border-radius: 8px;
    font-size: 14px;
    column-span: all;
  }}

  /* =========================================================
     7. IN-PAPER INTERACTIVE TOOLKIT WIDGETS
     ========================================================= */
  .interactive-widget {{
    background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%);
    border: 1.5px solid #93C5FD;
    border-radius: 12px;
    padding: 22px 24px;
    margin: 24px 0 30px;
    column-span: all;
    box-shadow: 0 4px 16px rgba(26, 115, 232, 0.07);
  }}
  .widget-header {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 8px;
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 12px;
    margin-bottom: 16px;
  }}
  .widget-badge {{
    display: inline-block;
    background: #DBEAFE;
    color: #1E40AF;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 0.4px;
  }}
  .widget-header h4 {{
    margin: 5px 0 0 0;
    font-size: 17px;
    color: #0F172A;
  }}
  .widget-hint {{
    font-size: 12px;
    color: #64748B;
  }}
  .filter-controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 16px;
  }}
  .filter-chip {{
    display: flex;
    align-items: center;
    gap: 7px;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    padding: 7px 12px;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 500;
    cursor: pointer;
    user-select: none;
  }}
  .filter-chip:hover {{
    border-color: #3B82F6;
    background: #F8FAFC;
  }}
  .license-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 12px;
  }}
  .lic-card {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 12px 14px;
    font-size: 12.5px;
  }}
  .lic-card.status-green {{ border-left: 4px solid #16A34A; }}
  .lic-card.status-amber {{ border-left: 4px solid #D97706; background: #FFFBEB; }}
  .lic-card.status-red {{ border-left: 4px solid #DC2626; background: #FEF2F2; opacity: 0.88; }}
  .lic-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
    font-weight: 700;
    color: #0F172A;
  }}
  .lic-badge {{
    font-size: 11px;
    padding: 2px 7px;
    border-radius: 999px;
    font-weight: 700;
  }}
  .badge-green {{ background: #DCFCE7; color: #166534; }}
  .badge-amber {{ background: #FEF3C7; color: #92400E; }}
  .badge-red {{ background: #FEE2E2; color: #991B1B; }}

  /* TCO Sliders */
  .tco-sliders {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-bottom: 18px;
  }}
  @media (max-width: 760px) {{ .tco-sliders {{ grid-template-columns: 1fr; }} }}
  .slider-group {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    padding: 12px 16px;
    border-radius: 8px;
  }}
  .slider-label {{
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    margin-bottom: 8px;
  }}
  .slider-group input[type=range] {{
    width: 100%;
    accent-color: #2563EB;
    cursor: pointer;
  }}
  .slider-ticks {{
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: #64748B;
    margin-top: 4px;
  }}
  .tco-bars {{
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 14px;
  }}
  .tco-row {{
    display: grid;
    grid-template-columns: 240px 1fr 120px;
    align-items: center;
    gap: 12px;
    font-size: 13px;
  }}
  @media (max-width: 760px) {{ .tco-row {{ grid-template-columns: 1fr; }} }}
  .tco-bar-track {{
    background: #F1F5F9;
    height: 22px;
    border-radius: 6px;
    overflow: hidden;
  }}
  .tco-bar-fill {{
    height: 100%;
    border-radius: 6px;
    transition: width 0.2s ease;
  }}
  .tco-verdict {{
    background: #ECFDF5;
    border: 1px solid #6EE7B7;
    color: #065F46;
    padding: 12px 16px;
    border-radius: 8px;
    font-size: 13.5px;
  }}

  /* Quadrant Selector */
  .quadrant-selector-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
  }}
  @media (max-width: 760px) {{ .quadrant-selector-grid {{ grid-template-columns: 1fr; }} }}
  .q-card {{
    text-align: left;
    padding: 14px 16px;
    border-radius: 10px;
    border: 2px solid #E2E8F0;
    background: #FFFFFF;
    cursor: pointer;
    transition: all 0.15s ease;
  }}
  .q-card.q-blue.active, .q-card.q-blue:hover {{ border-color: #2563EB; background: #EFF6FF; }}
  .q-card.q-green.active, .q-card.q-green:hover {{ border-color: #059669; background: #ECFDF5; }}
  .q-card.q-slate.active, .q-card.q-slate:hover {{ border-color: #475569; background: #F8FAFC; }}
  .q-card.q-amber.active, .q-card.q-amber:hover {{ border-color: #D97706; background: #FFFBEB; }}
  .q-tag {{ font-size: 11px; font-weight: 700; color: #475569; margin-bottom: 3px; }}
  .q-title {{ font-size: 15px; font-weight: 700; color: #0F172A; margin-bottom: 3px; }}
  .q-sub {{ font-size: 12px; color: #475569; }}
  .quadrant-detail {{
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 16px 20px;
    font-size: 13.5px;
  }}

  /* Series Cards Grid */
  .series-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 18px;
    margin-top: 20px;
  }}
  .series-card {{
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 18px 20px;
    background: #FFFFFF;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .series-date {{
    font-size: 11.5px;
    font-weight: 700;
    color: #1A73E8;
    text-transform: uppercase;
  }}
  .series-title {{
    font-size: 16px;
    font-weight: 700;
    color: #0F172A;
    margin: 6px 0 8px;
  }}
  .series-surface {{
    font-size: 12px;
    background: #F1F5F9;
    padding: 5px 9px;
    border-radius: 6px;
    margin-bottom: 10px;
    color: #334155;
  }}

  /* Docs Footer Pagination (Claude Docs style Next/Prev cards) */
  .docs-footer-nav {{
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid var(--border-subtle);
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }}
  .footer-nav-card {{
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 14px 18px;
    text-decoration: none;
    color: inherit;
    transition: all 0.15s ease;
    cursor: pointer;
    background: #FFFFFF;
  }}
  .footer-nav-card:hover {{
    border-color: var(--accent-primary);
    background: #F8FAFC;
    text-decoration: none;
  }}
  .footer-nav-label {{
    font-size: 11.5px;
    color: var(--text-muted);
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}
  .footer-nav-title {{
    font-size: 14.5px;
    font-weight: 600;
    color: var(--accent-primary);
  }}

  @media print {{
    .docs-topbar, .google-accent-line, .docs-left-sidebar, .docs-right-toc, .quick-jump-strip, .docs-footer-nav {{
      display: none !important;
    }}
    .docs-shell {{ display: block; }}
    .docs-main-pane {{ max-width: 100%; padding: 0; }}
  }}
</style>
</head>
<body>

<!-- =========================================================
     TOP NAVIGATION BAR
     ========================================================= -->
<header class="docs-topbar">
  <a href="#top" class="topbar-left" onclick="goHomeTop(); return false;" style="text-decoration:none; cursor:pointer;" title="Back to top of page">
    <span class="brand-mark">OW</span>
    <span class="brand-title">open-weights-playbook</span>
    <span class="gc-unofficial-badge" style="font-size:10.5px;padding:2px 8px;" title="Independent community guide — not an officially supported Google product">Unofficial Guide</span>
  </a>

  <nav class="topbar-center" aria-label="Main">
    <button id="top-tab-enterprise" class="slash-nav-link active" onclick="goHomeTop()">
      <span class="slug">/</span>playbook
    </button>
    <a class="slash-nav-link" href="#architect-questions" onclick="navToSection('view-enterprise', 'architect-questions'); return false;">
      <span class="slug">/</span>questions
    </a>
    <a class="slash-nav-link" href="#models-directory-sec" onclick="navToSection('view-enterprise', 'models-directory-sec'); return false;">
      <span class="slug">/</span>models
    </a>
    <a class="slash-nav-link" href="#1-open-weights-vs-open-source-the-4-release-tiers" onclick="navToSection('view-enterprise', '1-open-weights-vs-open-source-the-4-release-tiers'); return false;">
      <span class="slug">/</span>tiers
    </a>
    <a class="slash-nav-link" href="#widget-license-inline" onclick="navToSection('view-enterprise', 'widget-license-inline'); return false;">
      <span class="slug">/</span>licensing
    </a>
    <a class="slash-nav-link" href="#3-2-the-three-layer-open-production-stack" onclick="navToSection('view-enterprise', '3-2-the-three-layer-open-production-stack'); return false;">
      <span class="slug">/</span>stack
    </a>
    <a class="slash-nav-link" href="#4-enterprise-drivers-strategic-value-runtime-levers-watch-outs" onclick="navToSection('view-enterprise', '4-enterprise-drivers-strategic-value-runtime-levers-watch-outs'); return false;">
      <span class="slug">/</span>drivers
    </a>
    <a class="slash-nav-link" href="#5-industry-patterns-real-world-production-deployments" onclick="navToSection('view-enterprise', '5-industry-patterns-real-world-production-deployments'); return false;">
      <span class="slug">/</span>patterns
    </a>
    <a class="slash-nav-link" href="#widget-tco-inline" onclick="navToSection('view-enterprise', 'widget-tco-inline'); return false;">
      <span class="slug">/</span>economics
    </a>
    <button id="top-tab-series" class="slash-nav-link" onclick="switchView('view-series')">
      <span class="slug">/</span>series
    </button>
  </nav>

  <div class="topbar-right">
    <a class="top-jump-pill" href="#widget-license-inline" onclick="navToSection('view-enterprise', 'widget-license-inline'); return false;">⚡ License Filter</a>
    <a class="top-jump-pill" href="#widget-tco-inline" onclick="navToSection('view-enterprise', 'widget-tco-inline'); return false;">⚡ FinOps TCO</a>
    <a class="top-jump-pill" href="#widget-quadrant-inline" onclick="navToSection('view-enterprise', 'widget-quadrant-inline'); return false;">⚡ Workload Router</a>
    <a class="util-btn" href="https://github.com/kanchpat/open-weight-models" target="_blank" rel="noopener" style="text-decoration:none;">GitHub Repo ↗</a>
  </div>
</header>

<!-- PERSISTENT UNOFFICIAL GUIDE + AUTHORSHIP TOP RIBBON -->
<div class="unofficial-top-ribbon" role="note" aria-label="Unofficial Guide Notice and Credits">
  <strong>⚠️ Unofficial Google Cloud Practitioner Guide:</strong> Authored &amp; built by <strong>Kanchana Patlolla</strong> &amp; <strong>Anusha Sabbineni</strong>, with guidance from <strong>Alan Blount</strong>. Not an official Google or Google Cloud product, documentation site, or endorsement — views are the authors' own.
</div>

<!-- =========================================================
     VARIANT FIRST PAGE: GOOGLE CLOUD × OPEN-WEIGHT AI HERO
     + 5 KEY ARCHITECT QUESTIONS + ALL OPEN-WEIGHT MODELS
     ========================================================= -->
<section class="gc-hero-wrap" id="top-hero">
  <div class="gc-hero-inner">
    <div class="gc-split-grid">
      <div>
        <div class="gc-eyebrow-row">
          <span class="gc-unofficial-badge">⚠️ UNOFFICIAL GOOGLE CLOUD GUIDE</span>
          <span class="gc-live-badge">● Living Playbook · Updated Nov 2026</span>
        </div>
        <h1 class="gc-hero-title">
          Enterprise Architect's Guide to <span class="hl">Open-Weight AI Models</span> on Google&nbsp;Cloud
        </h1>
        <p class="gc-hero-sub">
          Open-weight models now power <strong>56% of enterprise gateway token volume at 14% of total spend</strong>. Before downloading a checkpoint or reserving GPUs, use this unofficial practitioner playbook to answer the five questions every enterprise architect faces—with examples across Google Cloud.
        </p>
        <div class="author-credit-panel">
          <div class="author-credit-chips">
            <span style="font-size:12px;font-weight:700;color:#0F172A;text-transform:uppercase;letter-spacing:0.04em;">Created by</span>
            <span class="author-chip"><span class="author-initials">KP</span> Kanchana Patlolla</span>
            <span class="author-chip"><span class="author-initials">AS</span> Anusha Sabbineni</span>
            <span class="author-chip guidance"><span class="author-initials">AB</span> Guidance: Alan Blount</span>
          </div>
          <div class="author-disclaimer-line">
            <strong>Unofficial Guide Disclaimer:</strong> Independent community &amp; practitioner resource — <strong>not</strong> an officially supported Google product, official Google Cloud documentation, or legal advice. All opinions and FinOps estimates are the authors' own.
          </div>
        </div>
        <div class="gc-cta-row">
          <button type="button" class="btn-pill-video" onclick="playExplainerAt(0, true, null)">
            <span aria-hidden="true">▶</span> Watch 5-Min Overview <span class="vid-dur-tag">5:01</span>
          </button>
          <a class="btn-pill-dark" href="#playbook-start" onclick="navToSection('view-enterprise', 'playbook-start'); return false;">
            Read Full Playbook <span aria-hidden="true">↓</span>
          </a>
          <a class="btn-pill-ghost" href="#architect-questions" onclick="navToSection('view-enterprise', 'architect-questions'); return false;">
            5 Key Questions <span aria-hidden="true">↓</span>
          </a>
          <a class="btn-pill-ghost" href="#models-directory-sec" onclick="navToSection('view-enterprise', 'models-directory-sec'); return false;">
            All 11 Models Covered <span aria-hidden="true">↓</span>
          </a>
          <button type="button" class="btn-pill-ghost" onclick="switchView('view-series')">
            7-Part Code &amp; Video Series <span aria-hidden="true">→</span>
          </button>
        </div>
      </div>

      <div class="gc-visual-card">
        <img src="{HERO_IMG_B64}" alt="Google Cloud x Open-Weight AI Models Architecture" />
        <div class="gc-surface-strip">
          <a class="gc-surf-chip" href="#6-1-the-73-duty-cycle-rule-serverless-openmaas-vs-dedicated-gpus" onclick="navToSection('view-enterprise', '6-1-the-73-duty-cycle-rule-serverless-openmaas-vs-dedicated-gpus'); return false;">
            <strong>Vertex AI OpenMaaS</strong>
            <span>Serverless · $0 Idle</span>
          </a>
          <a class="gc-surf-chip" href="#3-2-the-three-layer-open-production-stack" onclick="navToSection('view-enterprise', '3-2-the-three-layer-open-production-stack'); return false;">
            <strong>Cloud Run GPUs</strong>
            <span>Scale-to-Zero vLLM</span>
          </a>
          <a class="gc-surf-chip" href="#4-2-high-roi-runtime-drivers-evolving-the-harness-system-1-models" onclick="navToSection('view-enterprise', '4-2-high-roi-runtime-drivers-evolving-the-harness-system-1-models'); return false;">
            <strong>Google ADK Router</strong>
            <span>Harness + System 1</span>
          </a>
          <a class="gc-surf-chip" href="#7-ready-to-start-on-google-cloud-watch-this-space" onclick="navToSection('view-enterprise', '7-ready-to-start-on-google-cloud-watch-this-space'); return false;">
            <strong>Agent Runtime</strong>
            <span>In-VPC · LoRA/GRPO</span>
          </a>
        </div>
      </div>
    </div>

    <!-- 5-MINUTE NARRATED ARCHITECT'S VIDEO OVERVIEW (ENTRY RAMP ABOVE DEEP SCROLL) -->
    <div class="gc-video-spotlight" id="video-briefing">
      <div class="yt-player-stage" id="yt-player-stage">
        <button type="button" class="yt-poster-btn" onclick="playExplainerAt(0, false, null)" aria-label="Play 5-Minute Open-Weight AI Playbook Overview Video">
          <img src="{YT_THUMB_B64}" alt="Open-Weight AI Playbook 5-Minute Explainer Thumbnail" />
          <span class="yt-play-ring" aria-hidden="true">
            <svg viewBox="0 0 24 24"><polygon points="6,4 20,12 6,20"></polygon></svg>
          </span>
          <span class="yt-dur-badge">▶ 05:01</span>
        </button>
      </div>
      <div class="yt-spot-meta">
        <div class="yt-spot-top">
          <span class="yt-eyebrow">🎬 5-Minute Executive Overview · Start Here</span>
          <a class="yt-ext-link" href="https://youtu.be/jxbvqmRBcAo" target="_blank" rel="noopener noreferrer">Watch on YouTube ↗</a>
        </div>
        <h2 class="yt-spot-title">Prefer to watch first? Get the strategy, trade-offs &amp; 3-calculator tour in 5 minutes</h2>
        <p class="yt-spot-sub">Narrated by <strong>Kanchana Patlolla</strong> — why open weights run 56% of tokens at 14% of spend, hidden valuation &amp; MAU license traps, the <strong>73% GPU utilization rule</strong>, and how to use all three live calculators below. Click any chapter to jump right in:</p>
        <div class="yt-chap-grid" role="group" aria-label="Video chapters">
          <button type="button" class="yt-chap-btn" onclick="playExplainerAt(0, false, this)">
            <span class="yt-chap-time">0:00</span>
            <span class="yt-chap-lbl">56% / 14% Shift</span>
          </button>
          <button type="button" class="yt-chap-btn" onclick="playExplainerAt(40, false, this)">
            <span class="yt-chap-time">0:40</span>
            <span class="yt-chap-lbl">Why Enterprises Care</span>
          </button>
          <button type="button" class="yt-chap-btn" onclick="playExplainerAt(71, false, this)">
            <span class="yt-chap-time">1:11</span>
            <span class="yt-chap-lbl">License &amp; Data Traps</span>
          </button>
          <button type="button" class="yt-chap-btn" onclick="playExplainerAt(116, false, this)">
            <span class="yt-chap-time">1:56</span>
            <span class="yt-chap-lbl">ADK &amp; System 1 Heads</span>
          </button>
          <button type="button" class="yt-chap-btn" onclick="playExplainerAt(151, false, this)">
            <span class="yt-chap-time">2:31</span>
            <span class="yt-chap-lbl">The 73% GPU Rule</span>
          </button>
          <button type="button" class="yt-chap-btn" onclick="playExplainerAt(192, false, this)">
            <span class="yt-chap-time">3:12</span>
            <span class="yt-chap-lbl">3 Live Calculators</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 5 KEY ARCHITECT QUESTIONS (VISUAL METRIC BENTO) -->
    <div class="gc-questions-box" id="architect-questions">
      <div class="gc-sec-hdr">
        <h2>5 Key Questions for Enterprise Architects</h2>
        <span>Click any card to launch its calculator or blueprint ↓</span>
      </div>
      <div class="gc-q-grid">
        <!-- Q1 -->
        <div class="gc-q-card" style="--q-accent:#0B57D0; --q-bg:#EFF6FF;" onclick="navToSection('view-enterprise', 'widget-license-inline')">
          <div>
            <div class="gc-q-top">
              <div class="gc-q-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>
              </div>
              <span class="gc-q-num">01 · LICENSE</span>
            </div>
            <div class="gc-q-title">Which open-weight license is safe?</div>
            <div class="gc-q-stat">
              <strong>Tier 1–4</strong>
              <span>Valuation &amp; MAU Caps</span>
            </div>
            <div class="gc-q-pills">
              <span class="gc-q-pill">Apache 2.0</span>
              <span class="gc-q-pill">$10B Gate</span>
              <span class="gc-q-pill">Olmo 3</span>
            </div>
          </div>
          <div class="gc-q-foot"><span>⚡ Try License Filter</span><span>→</span></div>
        </div>

        <!-- Q2 -->
        <div class="gc-q-card" style="--q-accent:#15803D; --q-bg:#ECFDF5;" onclick="navToSection('view-enterprise', '4-2-high-roi-runtime-drivers-evolving-the-harness-system-1-models')">
          <div>
            <div class="gc-q-top">
              <div class="gc-q-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
              </div>
              <span class="gc-q-num">02 · HARNESS</span>
            </div>
            <div class="gc-q-title">Train weights or evolve the harness?</div>
            <div class="gc-q-stat">
              <strong>+16.7pp</strong>
              <span>35× Faster System 1</span>
            </div>
            <div class="gc-q-pills">
              <span class="gc-q-pill">Google ADK</span>
              <span class="gc-q-pill">output_tokens: 0</span>
            </div>
          </div>
          <div class="gc-q-foot"><span>Explore Harnesses</span><span>→</span></div>
        </div>

        <!-- Q3 -->
        <div class="gc-q-card" style="--q-accent:#B45309; --q-bg:#FEF3C7;" onclick="navToSection('view-enterprise', '4-3-seven-enterprise-watch-outs-how-to-mitigate-them')">
          <div>
            <div class="gc-q-top">
              <div class="gc-q-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              </div>
              <span class="gc-q-num">03 · SECURITY</span>
            </div>
            <div class="gc-q-title">How do we lock down VPC &amp; weights?</div>
            <div class="gc-q-stat">
              <strong>SHA-256</strong>
              <span>In-VPC Isolation</span>
            </div>
            <div class="gc-q-pills">
              <span class="gc-q-pill">Artifact Registry</span>
              <span class="gc-q-pill">Model Armor</span>
            </div>
          </div>
          <div class="gc-q-foot"><span>7 Risk Watch-Outs</span><span>→</span></div>
        </div>

        <!-- Q4 -->
        <div class="gc-q-card" style="--q-accent:#DC2626; --q-bg:#FEE2E2;" onclick="navToSection('view-enterprise', '5-industry-patterns-real-world-production-deployments')">
          <div>
            <div class="gc-q-top">
              <div class="gc-q-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
              </div>
              <span class="gc-q-num">04 · PATTERNS</span>
            </div>
            <div class="gc-q-title">Who is running this in production?</div>
            <div class="gc-q-stat">
              <strong>5 Patterns</strong>
              <span>Up to 90% Cost Cut</span>
            </div>
            <div class="gc-q-pills">
              <span class="gc-q-pill">Netflix</span>
              <span class="gc-q-pill">Pinterest</span>
              <span class="gc-q-pill">Harvey</span>
              <span class="gc-q-pill">DoorDash</span>
            </div>
          </div>
          <div class="gc-q-foot"><span>Industry Patterns</span><span>→</span></div>
        </div>

        <!-- Q5 -->
        <div class="gc-q-card" style="--q-accent:#6D28D9; --q-bg:#F3E8FF;" onclick="navToSection('view-enterprise', 'widget-tco-inline')">
          <div>
            <div class="gc-q-top">
              <div class="gc-q-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>
              </div>
              <span class="gc-q-num">05 · FINOPS</span>
            </div>
            <div class="gc-q-title">Serverless OpenMaaS or dedicated GPUs?</div>
            <div class="gc-q-stat">
              <strong>73% Rule</strong>
              <span>$0 Idle GPU Burn</span>
            </div>
            <div class="gc-q-pills">
              <span class="gc-q-pill">OpenMaaS ($0.907)</span>
              <span class="gc-q-pill">Cloud Run vLLM</span>
            </div>
          </div>
          <div class="gc-q-foot"><span>⚡ FinOps Calculator</span><span>→</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- =========================================================
     ALL OPEN-WEIGHT MODELS SHOWCASE DIRECTORY (First Page)
     ========================================================= -->
<section class="models-dir-sec" id="models-directory-sec">
  <div class="gc-sec-hdr">
    <h2>🧩 Open-Weight Models Covered in This Unofficial Guide &amp; Series</h2>
    <span>Filter by license, provenance tier, or Google Cloud deployment surface</span>
  </div>
  <div class="models-filter-bar">
    <button type="button" class="m-filter-btn active" onclick="filterModelShowcase('all', this)">All Models (11)</button>
    <button type="button" class="m-filter-btn" onclick="filterModelShowcase('permissive', this)">🟢 Unrestricted Apache 2.0 / MIT</button>
    <button type="button" class="m-filter-btn" onclick="filterModelShowcase('gcloud', this)">☁️ Vertex AI OpenMaaS &amp; Cloud Run</button>
    <button type="button" class="m-filter-btn" onclick="filterModelShowcase('tier4', this)">🔍 Tier 4 Full Pre-Training Provenance</button>
    <button type="button" class="m-filter-btn" onclick="filterModelShowcase('system1', this)">⚡ System 1 &amp; Specialized</button>
    <button type="button" class="m-filter-btn" onclick="filterModelShowcase('gated', this)">⚠️ Commercial / Valuation Caps</button>
  </div>
  <div id="models-showcase-container" class="models-showcase-grid"></div>
</section>

<!-- =========================================================
     TWO-PANE DOCS LAYOUT (Left Sidebar + Center Playbook)
     ========================================================= -->
<div class="docs-shell" id="playbook-start">

  <!-- SINGLE LEFT SIDEBAR: Complete Section, Calculator & Series Navigation -->
  <aside class="docs-left-sidebar" aria-label="Documentation Navigation">
    <div class="nav-group">
      <div class="nav-group-title">1. Strategy &amp; Licensing Triage</div>
      <ul class="nav-list">
        <li class="nav-item">
          <a class="nav-link" data-target="video-briefing" onclick="playExplainerAt(0, true, null); return false;">
            <span>▶ 5-Min Video Overview</span>
            <span class="interactive-tag">5:01</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link active" data-target="1-open-weights-vs-open-source-the-4-release-tiers" onclick="navToSection('view-enterprise', '1-open-weights-vs-open-source-the-4-release-tiers'); return false;">1. The 4 Openness Release Tiers</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-target="2-procurement-licensing-triage" onclick="navToSection('view-enterprise', '2-procurement-licensing-triage'); return false;">2. Procurement &amp; Licensing Triage</a>
        </li>
        <li class="nav-item">
          <a class="nav-link sub-link" data-target="widget-license-inline" onclick="navToSection('view-enterprise', 'widget-license-inline'); return false;">
            <span>2.1 License &amp; Audit Filter</span>
            <span class="interactive-tag">⚡ Tool</span>
          </a>
        </li>
      </ul>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">2. Stack, Drivers &amp; Industry Patterns</div>
      <ul class="nav-list">
        <li class="nav-item">
          <a class="nav-link" data-target="3-the-2026-model-landscape-3-layer-production-stack" onclick="navToSection('view-enterprise', '3-the-2026-model-landscape-3-layer-production-stack'); return false;">3. 2026 Model Landscape &amp; Stack</a>
        </li>
        <li class="nav-item">
          <a class="nav-link sub-link" data-target="3-1-picking-the-right-open-weight-model-family" onclick="navToSection('view-enterprise', '3-1-picking-the-right-open-weight-model-family'); return false;">3.1 Picking a Model Family</a>
        </li>
        <li class="nav-item">
          <a class="nav-link sub-link" data-target="3-2-the-three-layer-open-production-stack" onclick="navToSection('view-enterprise', '3-2-the-three-layer-open-production-stack'); return false;">3.2 3-Layer Production Stack</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-target="4-enterprise-drivers-strategic-value-runtime-levers-watch-outs" onclick="navToSection('view-enterprise', '4-enterprise-drivers-strategic-value-runtime-levers-watch-outs'); return false;">4. Enterprise Drivers &amp; Watch-Outs</a>
        </li>
        <li class="nav-item">
          <a class="nav-link sub-link" data-target="4-1-four-strategic-value-drivers" onclick="navToSection('view-enterprise', '4-1-four-strategic-value-drivers'); return false;">4.1 Four Strategic Value Drivers</a>
        </li>
        <li class="nav-item">
          <a class="nav-link sub-link" data-target="4-2-high-roi-runtime-drivers-evolving-the-harness-system-1-models" onclick="navToSection('view-enterprise', '4-2-high-roi-runtime-drivers-evolving-the-harness-system-1-models'); return false;">4.2 Harnesses &amp; System 1 Drivers</a>
        </li>
        <li class="nav-item">
          <a class="nav-link sub-link" data-target="4-3-seven-enterprise-watch-outs-how-to-mitigate-them" onclick="navToSection('view-enterprise', '4-3-seven-enterprise-watch-outs-how-to-mitigate-them'); return false;">4.3 Seven Risk Watch-Outs</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-target="5-industry-patterns-real-world-production-deployments" onclick="navToSection('view-enterprise', '5-industry-patterns-real-world-production-deployments'); return false;">5. Industry Patterns (1–5)</a>
        </li>
      </ul>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">3. Economics &amp; Workload Router</div>
      <ul class="nav-list">
        <li class="nav-item">
          <a class="nav-link" data-target="6-unit-economics-workload-routing-toolkit" onclick="navToSection('view-enterprise', '6-unit-economics-workload-routing-toolkit'); return false;">6. Economics &amp; Workload Toolkit</a>
        </li>
        <li class="nav-item">
          <a class="nav-link sub-link" data-target="widget-tco-inline" onclick="navToSection('view-enterprise', 'widget-tco-inline'); return false;">
            <span>6.1 FinOps TCO Calculator</span>
            <span class="interactive-tag">⚡ Tool</span>
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link sub-link" data-target="widget-quadrant-inline" onclick="navToSection('view-enterprise', 'widget-quadrant-inline'); return false;">
            <span>6.2 Workload Router</span>
            <span class="interactive-tag">⚡ Tool</span>
          </a>
        </li>
      </ul>
    </div>

    <div class="nav-group">
      <div class="nav-group-title">4. Google Cloud &amp; Code Series</div>
      <ul class="nav-list">
        <li class="nav-item">
          <a class="nav-link" data-target="7-ready-to-start-on-google-cloud-watch-this-space" onclick="navToSection('view-enterprise', '7-ready-to-start-on-google-cloud-watch-this-space'); return false;">7. Ready to Start on Google Cloud</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-target="8-reference-appendices-primary-source-bibliography" onclick="navToSection('view-enterprise', '8-reference-appendices-primary-source-bibliography'); return false;">8. References ([1]–[20])</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" onclick="switchView('view-series'); return false;">💻 All 7 Weekly Code Modules →</a>
        </li>
      </ul>
    </div>
  </aside>

  <!-- CENTER MAIN PANE: Paper + Embedded Interactive Toolkit -->
  <main class="docs-main-pane">

    <!-- VIEW 1: ENTERPRISE WHITEPAPER + INLINE INTERACTIVE TOOLKIT (DEFAULT) -->
    <div id="view-enterprise" class="view-section active">
      <div class="breadcrumbs">
        <span>Unofficial Practitioner Guides</span>
        <span>›</span>
        <span>Open-Weight AI Models</span>
        <span>›</span>
        <span class="crumb-active">Architect's Playbook &amp; Interactive FinOps Toolkit</span>
      </div>

      <header class="whitepaper-header">
        <div style="margin-bottom:10px;">
          <span class="gc-unofficial-badge">⚠️ UNOFFICIAL GOOGLE CLOUD PRACTITIONER GUIDE · NOT AN OFFICIAL GOOGLE PRODUCT</span>
        </div>
        <h1 class="whitepaper-title">Open-Weight AI Models for the Enterprise: An Architect's Guide to Strategy, Economics &amp; Production Patterns</h1>
        <div class="whitepaper-sub" style="display:flex;flex-direction:column;gap:6px;margin-top:10px;">
          <div class="author-credit-chips" style="margin-bottom:2px;">
            <span class="author-chip"><span class="author-initials">KP</span> Kanchana Patlolla</span>
            <span class="author-chip"><span class="author-initials">AS</span> Anusha Sabbineni</span>
            <span class="author-chip guidance"><span class="author-initials">AB</span> Guidance: Alan Blount</span>
          </div>
          <span>Part 1 of 7 · Unofficial Companion Playbook to the Community Code &amp; Video Series (Views expressed are the authors' own)</span>
        </div>
      </header>

      <div class="single-col-body">
        {ent_body_html}
      </div>

      <div class="docs-footer-nav" style="grid-template-columns: 1fr;">
        <div class="footer-nav-card" style="text-align:right;" onclick="switchView('view-series')">
          <div class="footer-nav-label">Next in Series (Parts 2–7)</div>
          <div class="footer-nav-title">Explore the 7-Part Weekly Code &amp; Video Series →</div>
        </div>
      </div>
    </div>

    <!-- VIEW 3: 7-PART CODE & VIDEO SERIES -->
    <div id="view-series" class="view-section">
      <div class="breadcrumbs">
        <span>Unofficial Practitioner Guides</span>
        <span>›</span>
        <span>Open-Weight AI Models</span>
        <span>›</span>
        <span class="crumb-active">7-Part Weekly Code &amp; Video Series (Nov 6 – Dec 18, 2026)</span>
      </div>

      <header class="whitepaper-header">
        <div style="margin-bottom:10px;">
          <span class="gc-unofficial-badge">⚠️ UNOFFICIAL GOOGLE CLOUD PRACTITIONER SERIES · NOT AN OFFICIAL GOOGLE PRODUCT</span>
        </div>
        <h1 class="whitepaper-title">7-Part Open-Weight Models Community Blog, Video &amp; Code Series (with Google Cloud Examples)</h1>
        <div class="whitepaper-sub" style="display:flex;flex-direction:column;gap:6px;margin-top:10px;">
          <div class="author-credit-chips" style="margin-bottom:2px;">
            <span class="author-chip"><span class="author-initials">KP</span> Kanchana Patlolla</span>
            <span class="author-chip"><span class="author-initials">AS</span> Anusha Sabbineni</span>
            <span class="author-chip guidance"><span class="author-initials">AB</span> Guidance: Alan Blount</span>
          </div>
          <span>Unofficial community resource (views are the authors' own) · Repo: <code>whitepaper/</code> · <code>docs/</code> · <code>series/part-02..07/</code></span>
        </div>
      </header>

      <div class="callout-box">
        <strong>How the GitHub Repo &amp; GitHub Pages Work Together:</strong> The <strong>Enterprise Playbook + Interactive Guide</strong> lives both on this documentation site and as native Markdown in <code>/whitepaper/enterprise-playbook.md</code>. Each Friday release below unlocks a hands-on code directory under <code>/series/</code> with runnable Vertex AI notebooks, <code>vLLM</code> Cloud Run Dockerfiles, ADK harnesses, and short video demos.
      </div>

      <div class="series-grid">
        <div class="series-card" id="series-part-1">
          <div>
            <div class="series-date">Part 1 · Nov 6, 2026 (Live Now)</div>
            <div class="series-title">Open-Weight AI for the Enterprise: Strategy, Economics &amp; the 2×2 Portfolio Matrix</div>
            <div class="series-surface"><strong>Surface:</strong> Vertex AI Model Garden (<code>Gemma 4</code>, <code>Qwen 3.8</code>, <code>DeepSeek-V4.1-Flash</code>, <code>Olmo 3</code>)</div>
            <p>The anchor executive whitepaper: 4-tier openness spectrum, <code>Green/Amber/Red</code> licensing triage, 5 Patterns from the Field, 7 downsides (<code>73%</code> duty cycle &amp; <code>$1,200</code> abliteration), and the Gartner 2×2 Matrix.</p>
          </div>
          <div style="display:flex;flex-direction:column;gap:8px;margin-top:10px;">
            <div style="display:flex;gap:8px;">
              <button type="button" class="util-btn" style="flex:1;justify-content:center;background:#0F172A;color:#FFFFFF;border-color:#0F172A;font-weight:600;" onclick="playExplainerAt(0, true, null)">▶ Watch Part 1 Video (5:01)</button>
              <a class="util-btn" style="text-decoration:none;font-weight:600;" href="https://youtu.be/jxbvqmRBcAo" target="_blank" rel="noopener noreferrer">YouTube ↗</a>
            </div>
            <button type="button" class="util-btn" style="width:100%;justify-content:center;background:#EFF6FF;color:#1D4ED8;border-color:#BFDBFE;font-weight:600;" onclick="switchView('view-enterprise')">📖 Read Part 1 Whitepaper &amp; Interactive Tools →</button>
          </div>
        </div>

        <div class="series-card" id="series-part-2">
          <div>
            <div class="series-date">Part 2 · Nov 13, 2026</div>
            <div class="series-title">Start Serverless: Building Zero-Ops Open-Weight Agents on Vertex AI OpenMaaS</div>
            <div class="series-surface"><strong>Repo Path:</strong> <code>series/part-02-openmaas-serverless/</code></div>
            <p>Why OpenMaaS PayGo (<code>$0.907/1M</code>) beats dedicated self-deploy (<code>$1.29/1M</code>) by <strong>1.42×</strong> below <code>73%</code> utilization + building a tool-calling <code>Gemma 4</code> / <code>Qwen</code> agent with contractual IP indemnification and <code>$0</code> idle burn.</p>
          </div>
          <span class="brand-badge">Unlocks Nov 13 · cURL + Vertex Python SDK</span>
        </div>

        <div class="series-card" id="series-part-3">
          <div>
            <div class="series-date">Part 3 · Nov 13, 2026</div>
            <div class="series-title">"Don't Train the Model, Evolve the Harness": Multi-Model Routing &amp; Verification with ADK</div>
            <div class="series-surface"><strong>Repo Path:</strong> <code>series/part-03-adk-harness-system1/</code></div>
            <p>Combining <code>Gemini 3.1 Pro</code> + <code>Gemma 4</code> / <code>DeepSeek</code> in Google's <strong>Agent Development Kit (ADK)</strong> (<code>64%</code> lower thread cost) with <strong><code>System 1</code> single-pass rubric verification gates</strong> (<code>+16.7pp</code> accuracy, <code>35×</code> faster).</p>
          </div>
          <span class="brand-badge">Unlocks Nov 13 · ADK + System 1 Pattern 3</span>
        </div>

        <div class="series-card" id="series-part-4">
          <div>
            <div class="series-date">Part 4 · Nov 20, 2026</div>
            <div class="series-title">When &amp; How to Self-Host: Scale-to-Zero vLLM &amp; QAT Open Models on Cloud Run</div>
            <div class="series-surface"><strong>Repo Path:</strong> <code>series/part-04-cloudrun-vllm-qat/</code></div>
            <p>Avoiding idle GPU burn on bursty custom containers using <strong>Cloud Run scale-to-zero GPUs</strong>, custom <code>vLLM</code> prefix caching / prefill heads (<em>Pattern 1</em>), and <strong><code>Gemma 4</code> QAT</strong> (<code>FP4</code>/<code>INT4</code> with zero tool-calling drift).</p>
          </div>
          <span class="brand-badge">Unlocks Nov 20 · Cloud Run L4/H100 + vLLM</span>
        </div>

        <div class="series-card" id="series-part-5">
          <div>
            <div class="series-date">Part 5 · Nov 20, 2026</div>
            <div class="series-title">Sovereign &amp; Matter-Isolated Agents: In-VPC Open Weights + System 1 Guardrails on Agent Runtime</div>
            <div class="series-surface"><strong>Repo Path:</strong> <code>series/part-05-agent-runtime-vpc/</code></div>
            <p>Deploying <code>SHA-256</code>-pinned open weights inside private VPC perimeters on <strong>Vertex AI Agent Runtime</strong>, wrapped in <strong><code>System 1</code> guardrails</strong>, <strong>Model Armor</strong>, and bidirectional PII redaction (<em>Pattern 5</em>).</p>
          </div>
          <span class="brand-badge">Unlocks Nov 20 · Sovereign VPC + Guardrails</span>
        </div>

        <div class="series-card" id="series-part-6">
          <div>
            <div class="series-date">Part 6 · Dec 4, 2026</div>
            <div class="series-title">Beyond the Prompt Tax: LoRA, &lt;$100 Verifiable RL (GRPO), and Multi-LoRA on Vertex AI</div>
            <div class="series-surface"><strong>Repo Path:</strong> <code>series/part-06-lora-grpo-verifiable-rl/</code></div>
            <p>Eliminating the 10,000-token "Prompt Context Tax" via Parameter-Efficient <code>LoRA</code>/<code>QLoRA</code>, <strong>single-GPU Verifiable RL (<code>GRPO</code>)</strong> (<em>Pattern 5</em>: <code>&lt;$100</code>, <code>+9.6%</code> F1 fraud-agent blueprint), and dynamic Multi-LoRA serving on Vertex AI.</p>
          </div>
          <span class="brand-badge">Unlocks Dec 4 · Vertex AI Training + SkyRL GRPO</span>
        </div>

        <div class="series-card" id="series-part-7">
          <div>
            <div class="series-date">Part 7 · Dec 11, 2026 (Wrap-Up Dec 18)</div>
            <div class="series-title">The "Frontier-to-Open" Distillation Playbook: 10× Cost Cut &amp; &lt;150 ms TTFT</div>
            <div class="series-surface"><strong>Repo Path:</strong> <code>series/part-07-frontier-distillation/</code></div>
            <p>Using <strong><code>Gemini 3.1 Pro</code></strong> as a teacher to synthesize verified domain pairs and distilling into compact <strong><code>Gemma 4</code> (<code>26B-A4B</code> / <code>E4B</code>)</strong> student models for <code>&lt;150 ms</code> TTFT at <strong>10% of frontier serving cost</strong> (<em>Patterns 2 &amp; 4</em>).</p>
          </div>
          <span class="brand-badge">Unlocks Dec 11 · Teacher-Student Distillation</span>
        </div>
      </div>
    </div>

  </main>

</div>

<footer class="site-global-footer">
  <div class="site-global-footer-inner">
    <div style="font-weight:600;color:#0F172A;">
      ✍️ Authored &amp; Built by <strong>Kanchana Patlolla</strong> &amp; <strong>Anusha Sabbineni</strong> &nbsp;·&nbsp; With guidance from <strong>Alan Blount</strong> &nbsp;·&nbsp;
      <a href="https://github.com/kanchpat/open-weight-models" target="_blank" rel="noopener">GitHub Repository (Apache 2.0) ↗</a>
    </div>
    <div>
      <strong>⚠️ Unofficial Google / Google Cloud Guide Disclaimer:</strong> This website (<code>openweights.cloudrace.info</code>) and companion repository are an independent, <strong>unofficial practitioner &amp; community guide</strong>. This is <strong>not</strong> an officially supported Google product, official Google Cloud documentation, or an official statement on behalf of Google LLC. All opinions, architectural recommendations, FinOps cost estimates, and model license summaries (provided for informational planning only and not legal advice) are strictly the authors' own.
    </div>
  </div>
</footer>

<script>
const LICENSE_MODELS = [
  {{ name: "Google Gemma 4 (31B / 26B-A4B / E4B / MedGemma)", license: "Apache 2.0", origin: "US", auditLevel: 2, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "Unrestricted commercial + patent grant; open QAT recipe; Vertex AI OpenMaaS." }},
  {{ name: "Ai2 Olmo 3 (32B Think) & Tülu 3", license: "Apache 2.0 / OpenMDW", origin: "US", auditLevel: 3, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "100% auditable pre-training data + filtering code + weights (Tier 4)." }},
  {{ name: "Reflection AI Beam-1.0-501B-A23B", license: "Apache 2.0", origin: "US", auditLevel: 2, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "US-origin frontier Sparse MoE (501B total / 23B active)." }},
  {{ name: "Aleph Alpha Kolibri (78B / 3.5B MoE)", license: "Apache 2.0", origin: "EU", auditLevel: 3, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "Sovereign European MoE with Merlin-Arthur verified grounding (44% abstention)." }},
  {{ name: "Alibaba Qwen 3.8 (27B / Flash-Next)", license: "Apache 2.0", origin: "CN", auditLevel: 2, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "Permissive Apache 2.0 workhorse; watch US Defense/FedRAMP origin rules." }},
  {{ name: "DeepSeek-V4.1-Flash (763B / 8B-16B Act)", license: "MIT", origin: "CN", auditLevel: 2, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "MIT license; 437x KV-cache compression (76x cheaper coding sessions)." }},
  {{ name: "Mistral Large 4 (1T/52B) & Timestral", license: "Apache 2.0 / Mod-MIT", origin: "EU", auditLevel: 1, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "Large 4 is Apache 2.0 (93.3% Lakera B3 safety); Timestral weights use Mod-MIT." }},
  {{ name: "Meta Llama 4 (Maverick / Scout)", license: "Llama 4 Community (700M MAU Cap)", origin: "US", auditLevel: 1, cap10b: false, cap100m: false, cap700m: true, ncAdapter: false, note: "Triggers commercial license above 700M MAU + requires 'Llama' naming prefix." }},
  {{ name: "Moonshot Kimi K3 / Meta Muse Spark Open", license: "Custom Commercial Cap (100M MAU)", origin: "CN/US", auditLevel: 1, cap10b: false, cap100m: true, cap700m: true, ncAdapter: false, note: "Requires commercial license above 100M MAU or $20M/mo inference revenue." }},
  {{ name: "Zhipu GLM-5.3 (320B / 18B Act)", license: "Custom $10B Valuation Cap", origin: "CN", auditLevel: 1, cap10b: true, cap100m: true, cap700m: true, ncAdapter: false, note: "Triggers mandatory commercial/security gate if company valuation/revenue >= $10B." }},
  {{ name: "firelex/jeff (sanctions & soc LoRA adapters)", license: "CC BY-NC 4.0 (Adapters)", origin: "US/EU", auditLevel: 2, cap10b: false, cap100m: false, cap700m: false, ncAdapter: true, note: "Base model is Apache 2.0, but sanctions/soc LoRAs prohibit commercial use." }}
];

const VAL_LABELS = {{
  1: "$50M (Startup)",
  2: "$500M (Growth)",
  3: "$2B (Mid-Market)",
  4: "$10B (Enterprise Gate)",
  5: "$50B+ (Global Fortune 500)"
}};

const MAU_LABELS = {{
  1: "<1M MAU",
  2: "10M MAU",
  3: "50M MAU",
  4: "100M+ MAU (Commercial Cap)",
  5: "700M+ MAU (Hyperscale Cap)"
}};

const REG_LABELS = {{
  1: "Global (Any Origin)",
  2: "US / EU Regulated Origin Only",
  3: "Strict EU Sovereign Origin Only"
}};

const AUD_LABELS = {{
  1: "Level 1: Weights Only",
  2: "Level 2: Weights + Open Recipe",
  3: "Level 3: Full Pre-Training Data (Tier 4)"
}};

function renderLicenseGrid(targetId, valStep, mauStep, regStep, audStep) {{
  const el = document.getElementById(targetId);
  if (!el) return;
  let htmlStr = "";
  LICENSE_MODELS.forEach(m => {{
    let status = "green";
    let badgeText = "🟢 Approved";
    let reasons = [];
    if (m.ncAdapter) {{
      status = "red";
      badgeText = "🔴 Non-Commercial Adapter";
      reasons.push("CC BY-NC 4.0 adapter bars commercial use");
    }}
    if (valStep >= 4 && m.cap10b) {{
      status = "red";
      badgeText = "🔴 Hits $10B Valuation Cap";
      reasons.push("Exceeds $10B corporate valuation/revenue gate");
    }}
    if (mauStep >= 4 && m.cap100m && status !== "red") {{
      status = "amber";
      badgeText = "🟡 Hits 100M MAU / $20M Cap";
      reasons.push("Requires custom commercial license above 100M MAU");
    }}
    if (mauStep >= 5 && m.cap700m && !m.cap100m && status !== "red") {{
      status = "amber";
      badgeText = "🟡 Hits 700M MAU Cap";
      reasons.push("Requires custom commercial license above 700M MAU");
    }}
    if (regStep === 2 && (m.origin !== "US" && m.origin !== "EU")) {{
      status = "red";
      badgeText = "🔴 Origin Restriction";
      reasons.push("Non-US/EU origin (" + m.origin + ")");
    }}
    if (regStep === 3 && m.origin !== "EU") {{
      status = status === "red" ? "red" : (m.origin === "US" ? "amber" : "red");
      badgeText = m.origin === "US" ? "🟡 US Origin (Host in EU VPC)" : "🔴 Non-EU Origin";
      reasons.push("Strict EU origin policy selected (" + m.origin + ")");
    }}
    if (audStep > m.auditLevel) {{
      status = status === "red" ? "red" : "amber";
      if (status === "amber") {{
        badgeText = audStep === 3 ? "🟡 Weights Only (Not Tier 4)" : "🟡 Recipe Not Fully Disclosed";
      }}
      reasons.push(audStep === 3 ? "Pre-training data corpus not publicly auditable" : "Post-training recipe not fully open");
    }}
    const badgeCls = status === "green" ? "badge-green" : (status === "amber" ? "badge-amber" : "badge-red");
    const reasonLine = reasons.length ? `<div style="margin-top:6px;font-weight:600;color:#B45309;">⚠️ ${{reasons.join(" · ")}}</div>` : "";
    htmlStr += `
      <div class="lic-card status-${{status}}">
        <div class="lic-top">
          <span>${{m.name}}</span>
          <span class="lic-badge ${{badgeCls}}">${{badgeText}}</span>
        </div>
        <div style="color:#475569;margin-bottom:4px;"><strong>License:</strong> <code>${{m.license}}</code> · <strong>Origin:</strong> ${{m.origin}}</div>
        <div>${{m.note}}</div>
        ${{reasonLine}}
      </div>`;
  }});
  el.innerHTML = htmlStr;
}}

function updateLicenseFilter() {{
  const valStep = parseInt(document.getElementById("sld-lic-val")?.value || "4", 10);
  const mauStep = parseInt(document.getElementById("sld-lic-mau")?.value || "3", 10);
  const regStep = parseInt(document.getElementById("sld-lic-reg")?.value || "1", 10);
  const audStep = parseInt(document.getElementById("sld-lic-aud")?.value || "1", 10);

  const lblVal = document.getElementById("lbl-lic-val");
  const lblMau = document.getElementById("lbl-lic-mau");
  const lblReg = document.getElementById("lbl-lic-reg");
  const lblAud = document.getElementById("lbl-lic-aud");

  if (lblVal) lblVal.textContent = VAL_LABELS[valStep] || "$10B";
  if (lblMau) lblMau.textContent = MAU_LABELS[mauStep] || "50M MAU";
  if (lblReg) lblReg.textContent = REG_LABELS[regStep] || "Global";
  if (lblAud) lblAud.textContent = AUD_LABELS[audStep] || "Weights Only";

  renderLicenseGrid("license-results-grid", valStep, mauStep, regStep, audStep);
}}

function updateTcoCalc() {{
  const tokMPerDay = parseInt(document.getElementById("sld-tok-vol")?.value || "25", 10);
  const dutyPct = parseInt(document.getElementById("sld-duty")?.value || "35", 10);
  const monthlyM = tokMPerDay * 30;

  document.getElementById("lbl-tok-vol").textContent = `${{tokMPerDay}}M tokens/day (${{monthlyM.toLocaleString()}}M/mo)`;
  let dutyDesc = dutyPct < 30 ? "Spiky Traffic" : (dutyPct < 73 ? "Below 73% Break-Even" : "High Sustained Utilization");
  document.getElementById("lbl-duty").textContent = `${{dutyPct}}% Duty Cycle (${{dutyDesc}})`;

  const costClosed = Math.round(monthlyM * 10.0);
  const costMaaS = Math.round(monthlyM * 0.907);
  const effectiveDedicatedRate = 0.907 * (73.0 / Math.max(dutyPct, 10));
  const costDedicated = Math.round(monthlyM * effectiveDedicatedRate);
  const costSystem1 = Math.max(45, Math.round(monthlyM * 0.05));

  const maxCost = Math.max(costClosed, costDedicated, costMaaS, 1);
  const rows = [
    {{ label: "Closed Frontier API ($10.00/1M)", cost: costClosed, color: "#64748B", rate: "$10.00/1M" }},
    {{ label: "Vertex AI OpenMaaS PayGo ($0.907/1M)", cost: costMaaS, color: "#1A73E8", rate: "$0.907/1M ($0 idle)" }},
    {{ label: `Dedicated Self-Deploy (@ ${{dutyPct}}% Duty Cycle)`, cost: costDedicated, color: dutyPct >= 73 ? "#059669" : "#D97706", rate: `$${{effectiveDedicatedRate.toFixed(2)}}/1M eff.` }},
    {{ label: "System 1 Single-Pass (Clef / Decision-1)", cost: costSystem1, color: "#0D9488", rate: "output_tokens: 0" }}
  ];

  let barsHtml = "";
  rows.forEach(r => {{
    const wPct = Math.max(3, Math.min(100, (r.cost / maxCost) * 100));
    barsHtml += `
      <div class="tco-row">
        <div><strong>${{r.label}}</strong><div style="font-size:11.5px;color:#64748B;">${{r.rate}}</div></div>
        <div class="tco-bar-track"><div class="tco-bar-fill" style="width:${{wPct}}%;background:${{r.color}};"></div></div>
        <div style="text-align:right;font-weight:700;">$${{r.cost.toLocaleString()}}/mo</div>
      </div>`;
  }});
  document.getElementById("tco-bars-container").innerHTML = barsHtml;

  const savingsVsClosed = Math.round((1 - (Math.min(costMaaS, costDedicated) / costClosed)) * 100);
  let verdictHtml = "";
  if (tokMPerDay < 8) {{
    verdictHtml = `<strong>📌 FinOps Verdict (Pilot Scale &lt; 8M tok/day):</strong> Stay on <strong>Vertex AI OpenMaaS PayGo (<code>$${{costMaaS.toLocaleString()}}/mo</code>)</strong> or Closed Frontier APIs. Spinning up dedicated GPUs at <code>${{dutyPct}}%</code> utilization costs <strong>${{(effectiveDedicatedRate / 0.907).toFixed(2)}}× more</strong> than serverless OpenMaaS.`;
  }} else if (dutyPct < 73) {{
    verdictHtml = `<strong>📌 FinOps Verdict (Below 73% Duty Cycle):</strong> Choose <strong>Vertex AI OpenMaaS PayGo (<code>$${{costMaaS.toLocaleString()}}/mo</code>, saving ${{savingsVsClosed}}% vs. closed APIs)</strong> or <strong>Cloud Run Scale-to-Zero GPUs</strong> (if custom <code>vLLM</code> flags are required). Dedicated 24/7 self-hosting burns idle GPU budget (<code>$${{costDedicated.toLocaleString()}}/mo</code>) until duty cycle exceeds <strong>73%</strong>. See <strong>Series Parts 2 &amp; 4</strong>.`;
  }} else {{
    verdictHtml = `<strong>📌 FinOps Verdict (Sustained Scale &gt; 73% Duty Cycle):</strong> You have cleared the <strong>73% duty-cycle barrier</strong>! A 3-year reserved self-deployment or custom <code>vLLM</code> cluster (<code>$${{costDedicated.toLocaleString()}}/mo</code>) now beats PayGo while cutting costs <strong>${{savingsVsClosed}}% vs. closed APIs</strong>. Offload classification/guardrails to <strong>System 1 (<code>Clef</code> / <code>Decision-1</code>)</strong> to save even more. See <strong>Series Parts 4 &amp; 5</strong>.`;
  }}
  document.getElementById("tco-verdict-box").innerHTML = verdictHtml;
}}

const QUADRANT_DATA = {{
  Q2: {{
    title: "Quadrant II — Govern & Audit: Sovereign & Reproducible Open Weights (In-VPC)",
    patterns: "Pattern 3: Harvey (Matter-Isolated Rubric & Harness Gates) · Sovereign EU Banking (Kolibri) · Clinical HIPAA/FDA Pinning (MedGemma) · Full Provenance (Olmo 3)",
    stack: "Vertex AI Agent Runtime (In-VPC) + SHA-256 Checkpoint Pinning + System 1 Guardrails + Google Cloud Model Armor",
    module: "Part 5 (Nov 20, 2026): Sovereign & Matter-Isolated Agents on Vertex AI Agent Runtime"
  }},
  Q1: {{
    title: "Quadrant I — Own the Moat (Strategic Leaders): Post-Trained & Surgically Customized Open Weights",
    patterns: "Pattern 1: Netflix GenRec (vLLM Prefill Catalog Ranker, +10% traffic) · Pattern 2: Pinterest (Surgical Vision Encoder Graft, -90% cost) · Pattern 4: DoorDash (Teacher-Student SKU Distillation, 10x cut) · Pattern 5: Coinbase & Uber (<$100 Single-GPU GRPO Fraud Agent & PII Gateway, +9.6% F1)",
    stack: "Vertex AI Training + SkyRL GRPO + OpenMaaS Dynamic Multi-LoRA + Gemini 3.1 Pro → Gemma 4 Distillation",
    module: "Part 6 (Dec 4: LoRA & <$100 GRPO RL) & Part 7 (Dec 11: Frontier-to-Open Distillation)"
  }},
  Q3: {{
    title: "Quadrant III — Rent for Agility & Frontier R&D: Closed Frontier APIs & Serverless OpenMaaS",
    patterns: "Zero-Ops Prototyping (<73% GPU duty cycle, $0 idle burn) · Contractual IP Indemnification · Hard PhD Science (CritPt v2)",
    stack: "Gemini 3.1 Pro + Vertex AI Model Garden Managed OpenMaaS (Gemma 4, Qwen 3.8, DeepSeek-V4.1-Flash at $0.907/1M)",
    module: "Part 2 (Nov 13, 2026): Start Serverless — Building Zero-Ops Open-Weight Agents on Vertex AI OpenMaaS"
  }},
  Q4: {{
    title: "Quadrant IV — Scale & Optimize FinOps: Sparse Open Weights, Evolved Harnesses & System 1",
    patterns: "76x Lower Coding Cost (DeepSeek-V4.1-Flash 437x KV-Cache Cut) · +16.7pp Meta-Harness Evolution · System 1 Zero-Token Triage (Clef / Clairic / Decision-1, 35x faster & 200x cheaper)",
    stack: "Google ADK Multi-Model In-Harness Router + System 1 Verification Gate + Cloud Run Scale-to-Zero vLLM GPUs",
    module: "Part 3 (Nov 13: ADK Harness & System 1 Routing) & Part 4 (Nov 20: Scale-to-Zero vLLM & QAT on Cloud Run)"
  }}
}};

function selectQuadrant(qKey, btnEl) {{
  if (btnEl) {{
    document.querySelectorAll(".q-card").forEach(b => b.classList.remove("active"));
    btnEl.classList.add("active");
  }}
  const d = QUADRANT_DATA[qKey];
  const panel = document.getElementById("quadrant-detail-panel");
  if (!panel || !d) return;
  panel.innerHTML = `
    <div style="font-weight:700;font-size:15.5px;color:#0F172A;margin-bottom:8px;">${{d.title}}</div>
    <div style="margin-bottom:6px;"><strong>Industry Patterns &amp; Customers:</strong> ${{d.patterns}}</div>
    <div style="margin-bottom:10px;"><strong>Recommended Google Cloud Stack:</strong> <code>${{d.stack}}</code></div>
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;background:#F8FAFC;padding:10px 14px;border-radius:6px;border:1px solid #E2E8F0;">
      <span><strong>Matching Hands-On Series Module:</strong> ${{d.module}}</span>
      <button class="util-btn" style="background:#EFF6FF;color:#1D4ED8;border-color:#BFDBFE;font-weight:600;" onclick="switchView('view-series')">View in 7-Part Code Series →</button>
    </div>`;
}}

/* =========================================================
   NAVIGATION & RIGHT "ON THIS PAGE" SCROLL-SPY ENGINE
   ========================================================= */
let currentActiveView = "view-enterprise";

function buildRightToc(viewId) {{
  const container = document.getElementById(viewId);
  const tocUl = document.getElementById("dynamic-right-toc");
  if (!container || !tocUl) return;

  const nodes = container.querySelectorAll("h2[id], h3[id], .interactive-widget[id]");
  let htmlItems = "";
  nodes.forEach(node => {{
    const id = node.id;
    if (!id) return;
    let label = "";
    let cls = "toc-link";
    if (node.classList.contains("interactive-widget")) {{
      label = node.getAttribute("data-toc-label") || "⚡ Interactive Tool";
      cls += " toc-widget";
    }} else {{
      label = node.textContent.replace(/\\s+/g, " ").trim();
      if (label.length > 54) label = label.slice(0, 52) + "…";
      if (node.tagName === "H3") cls += " toc-h3";
    }}
    htmlItems += `<li class="toc-item"><a class="${{cls}}" href="#${{id}}" data-toc-id="${{id}}" onclick="navToSection('${{viewId}}', '${{id}}'); return false;">${{label}}</a></li>`;
  }});
  tocUl.innerHTML = htmlItems;
}}

const SHOWCASE_MODELS = [
  {{
    name: "Google Gemma 4 (31B / 26B-A4B / E4B / MedGemma)",
    tier: "Tier III (Open Recipe + QAT)",
    license: "Apache 2.0",
    status: "green",
    cats: ["all", "permissive", "gcloud"],
    arch: "Dense 31B · MoE 26B-A4B · Edge E4B · FP4/INT4 QAT",
    strength: "Zero tool-calling drift under FP4/INT4 QAT; teacher-student distillation target (<150 ms TTFT).",
    cloud: "Vertex AI OpenMaaS · Cloud Run vLLM · ADK",
    jump: "3-1-picking-the-right-open-weight-model-family"
  }},
  {{
    name: "Ai2 Olmo 3 (32B Think) & Tülu 3",
    tier: "Tier IV (100% Open Source)",
    license: "Apache 2.0 / OpenMDW",
    status: "green",
    cats: ["all", "permissive", "tier4", "gcloud"],
    arch: "32B Dense · Full Dolma 3 Corpus + RLVR Code",
    strength: "Gold-standard EU AI Act & copyright auditability with line-by-line pre-training data lineage.",
    cloud: "Vertex AI Model Garden · Agent Runtime VPC",
    jump: "1-open-weights-vs-open-source-the-4-release-tiers"
  }},
  {{
    name: "DeepSeek-V4.1-Flash (1017)",
    tier: "Tier III (Open Weights)",
    license: "MIT",
    status: "green",
    cats: ["all", "permissive", "gcloud"],
    arch: "763B Total / 8B–16B Active MoE · CSA2 Attention",
    strength: "437× KV-cache reduction (10 MB @ 128K context); 76× lower coding & math agent token cost.",
    cloud: "Vertex AI OpenMaaS · ADK Tiered Router",
    jump: "3-1-picking-the-right-open-weight-model-family"
  }},
  {{
    name: "Alibaba Qwen 3.8 (27B & Flash-Next 180B-A6B)",
    tier: "Tier III (Open Weights)",
    license: "Apache 2.0",
    status: "green",
    cats: ["all", "permissive", "gcloud"],
    arch: "27B Dense & 180B Total / 6B Active Hybrid MoE",
    strength: "High-throughput multilingual & coding workhorse; vision encoder graft base (Pattern 2).",
    cloud: "Vertex AI OpenMaaS · Cloud Run GPUs",
    jump: "3-1-picking-the-right-open-weight-model-family"
  }},
  {{
    name: "Mistral Large 4 (1T/52B) & Timestral",
    tier: "Tier III (Open Weights)",
    license: "Apache 2.0 / Mod-MIT",
    status: "green",
    cats: ["all", "permissive", "gcloud"],
    arch: "1T Total / 52B Active MoE · 380M Time-Series",
    strength: "93.3% Lakera B3 adversarial safety defense; Timestral zero-shot forecasting at 5,000 series/s.",
    cloud: "Vertex AI Model Garden · Cloud Run vLLM",
    jump: "4-3-seven-enterprise-watch-outs-how-to-mitigate-them"
  }},
  {{
    name: "Reflection AI Beam 1.0 (501B-A23B)",
    tier: "Tier III (Open Weights)",
    license: "Apache 2.0",
    status: "green",
    cats: ["all", "permissive", "gcloud"],
    arch: "501B Total / 23B Active Sparse MoE",
    strength: "US-origin frontier open-weight MoE engineered for multi-step enterprise agentic reasoning.",
    cloud: "Vertex AI Model Garden · Agent Runtime",
    jump: "3-1-picking-the-right-open-weight-model-family"
  }},
  {{
    name: "Aleph Alpha Kolibri (78B-A3.5B MoE)",
    tier: "Tier IV (Sovereign Verified)",
    license: "Apache 2.0",
    status: "green",
    cats: ["all", "permissive", "tier4", "gcloud"],
    arch: "78B Total / 3.5B Active MoE · Merlin-Arthur",
    strength: "European sovereign MoE with cryptographic citation verification (44% ungrounded abstention).",
    cloud: "Vertex AI Agent Runtime (EU Sovereign VPC)",
    jump: "3-1-picking-the-right-open-weight-model-family"
  }},
  {{
    name: "System 1 Decision Models (dgem / Clef / Clairic / Decision-1)",
    tier: "Tier III (Single-Pass Heads)",
    license: "Apache 2.0",
    status: "green",
    cats: ["all", "permissive", "system1", "gcloud"],
    arch: "0.6B–4B Single Forward Pass (output_tokens: 0)",
    strength: "35× faster (5.8–84 ms p50) & 200× cheaper rubric verification, guardrails & structured extraction.",
    cloud: "Google ADK Gate · Cloud Run · Agent Runtime",
    jump: "4-2-high-roi-runtime-drivers-evolving-the-harness-system-1-models"
  }},
  {{
    name: "Meta Llama 4 (Maverick / Scout)",
    tier: "Tier III (Threshold License)",
    license: "Llama 4 Community (700M MAU Cap)",
    status: "amber",
    cats: ["all", "gated", "gcloud"],
    arch: "Multimodal Native MoE (17B Active)",
    strength: "Broad ecosystem compatibility; requires 'Llama' naming prefix & commercial deal above 700M MAU.",
    cloud: "Vertex AI Model Garden",
    jump: "2-procurement-licensing-triage"
  }},
  {{
    name: "Moonshot Kimi K3.1 Pro & K3",
    tier: "Tier III (Threshold License)",
    license: "Custom Cap (100M MAU / $20M Rev)",
    status: "amber",
    cats: ["all", "gated"],
    arch: "1T+ Sparse MoE · Long-Horizon Agent",
    strength: "Strong deep-research & tool-use benchmarks; triggers commercial license above 100M MAU.",
    cloud: "Self-Hosted vLLM on GKE / Cloud Run",
    jump: "2-procurement-licensing-triage"
  }},
  {{
    name: "Zhipu GLM-5.3-Flash (320B-A18B)",
    tier: "Tier III (Valuation Gate)",
    license: "Custom $10B Valuation Cap",
    status: "red",
    cats: ["all", "gated"],
    arch: "320B Total / 18B Active MoE",
    strength: "Fast agentic coding, but triggers mandatory commercial & security gate if valuation >= $10B.",
    cloud: "Requires Commercial Gate Clearance",
    jump: "2-procurement-licensing-triage"
  }}
];

function filterModelShowcase(cat, btnEl) {{
  if (btnEl) {{
    document.querySelectorAll(".m-filter-btn").forEach(b => b.classList.remove("active"));
    btnEl.classList.add("active");
  }}
  const container = document.getElementById("models-showcase-container");
  if (!container) return;
  const filtered = SHOWCASE_MODELS.filter(m => m.cats.includes(cat));
  let html = "";
  filtered.forEach(m => {{
    const badgeCls = m.status === "green" ? "badge-green" : (m.status === "amber" ? "badge-amber" : "badge-red");
    html += `
      <div class="m-show-card">
        <div>
          <div class="m-show-top">
            <div class="m-show-name">${{m.name}}</div>
            <span class="lic-badge ${{badgeCls}}">${{m.license}}</span>
          </div>
          <div class="m-show-meta">
            <span class="m-tag-chip">${{m.tier}}</span>
            <span class="m-tag-chip">${{m.arch}}</span>
          </div>
          <div style="color:#475569;line-height:1.42;">${{m.strength}}</div>
        </div>
        <div class="m-cloud-bar">
          <span>☁️ ${{m.cloud}}</span>
          <a href="#${{m.jump}}" onclick="navToSection('view-enterprise', '${{m.jump}}'); return false;">Details →</a>
        </div>
      </div>`;
  }});
  container.innerHTML = html;
}}

function playExplainerAt(startSec, shouldScroll, btnEl) {{
  const safeStart = Math.max(0, Math.min(300, Math.floor(Number(startSec) || 0)));
  if (currentActiveView !== "view-enterprise") {{
    switchView("view-enterprise", true);
  }}
  const spot = document.getElementById("video-briefing");
  if (shouldScroll && spot) {{
    spot.scrollIntoView({{ behavior: "smooth", block: "center" }});
  }}
  document.querySelectorAll(".yt-chap-btn").forEach(b => b.classList.remove("active"));
  if (btnEl) {{
    btnEl.classList.add("active");
  }} else {{
    const firstBtn = document.querySelector(".yt-chap-btn");
    if (firstBtn && safeStart === 0) firstBtn.classList.add("active");
  }}

  // On file:// or opaque sandboxed origins (where YouTube blocks embeds without an HTTPS/HTTP referrer), open YouTube cleanly at the timestamp.
  let originStr = "";
  try {{ originStr = String(window.location.origin || ""); }} catch (e) {{ originStr = ""; }}
  const proto = String(window.location.protocol || "");
  if ((proto !== "https:" && proto !== "http:") || !originStr || originStr === "null") {{
    const extUrl = safeStart > 0
      ? "https://youtu.be/jxbvqmRBcAo?t=" + String(safeStart)
      : "https://youtu.be/jxbvqmRBcAo";
    window.open(extUrl, "_blank", "noopener,noreferrer");
    return;
  }}

  const stage = document.getElementById("yt-player-stage");
  if (!stage) return;
  if (spot) spot.classList.add("is-playing");

  const iframe = document.createElement("iframe");
  iframe.setAttribute(
    "src",
    "https://www.youtube-nocookie.com/embed/jxbvqmRBcAo?autoplay=1&rel=0&modestbranding=1&playsinline=1&start=" + String(safeStart)
  );
  iframe.setAttribute("title", "Open-Weight AI Models for Enterprise Architects — 5-Minute Explainer");
  iframe.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
  iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
  iframe.setAttribute("allowfullscreen", "");
  stage.replaceChildren(iframe);
}}

function goHomeTop() {{
  if (currentActiveView !== "view-enterprise") {{
    switchView("view-enterprise", true);
  }}
  document.querySelectorAll(".slash-nav-link").forEach(b => b.classList.remove("active"));
  document.getElementById("top-tab-enterprise")?.classList.add("active");
  window.scrollTo({{ top: 0, behavior: "smooth" }});
}}

function switchView(viewId, skipScrollTop) {{
  currentActiveView = viewId;
  document.querySelectorAll(".view-section").forEach(s => s.classList.remove("active"));
  const target = document.getElementById(viewId);
  if (target) target.classList.add("active");

  document.querySelectorAll(".slash-nav-link").forEach(b => b.classList.remove("active"));
  if (viewId === "view-enterprise") document.getElementById("top-tab-enterprise")?.classList.add("active");
  if (viewId === "view-series") document.getElementById("top-tab-series")?.classList.add("active");

  const heroEl = document.getElementById("top-hero");
  const modelsEl = document.getElementById("models-directory-sec");
  if (heroEl) heroEl.style.display = viewId === "view-enterprise" ? "block" : "none";
  if (modelsEl) modelsEl.style.display = viewId === "view-enterprise" ? "block" : "none";

  buildRightToc(viewId);
  if (!skipScrollTop) {{
    window.scrollTo({{ top: 0, behavior: "smooth" }});
  }}
  setTimeout(onScrollSpy, 60);
}}

function navToSection(viewId, elementId) {{
  if (currentActiveView !== viewId) {{
    switchView(viewId, true);
  }}
  const el = document.getElementById(elementId);
  if (el) {{
    el.scrollIntoView({{ behavior: "smooth", block: "start" }});
  }}
  // Highlight immediately
  highlightNavTarget(elementId);
}}

function highlightNavTarget(activeId) {{
  if (!activeId) return;
  document.querySelectorAll("#dynamic-right-toc .toc-link").forEach(a => {{
    a.classList.toggle("active", a.getAttribute("data-toc-id") === activeId);
  }});
  document.querySelectorAll(".docs-left-sidebar .nav-link[data-target]").forEach(a => {{
    a.classList.toggle("active", a.getAttribute("data-target") === activeId);
  }});
}}

function onScrollSpy() {{
  if (currentActiveView !== "view-enterprise") return;
  const links = Array.from(document.querySelectorAll(".docs-left-sidebar .nav-link[data-target]"));
  const targets = links.map(a => document.getElementById(a.getAttribute("data-target"))).filter(Boolean);
  if (!targets.length) return;

  let currentId = targets[0].id;
  const threshold = 140;
  for (const el of targets) {{
    const rect = el.getBoundingClientRect();
    if (rect.top <= threshold) {{
      currentId = el.id;
    }}
  }}
  highlightNavTarget(currentId);
}}

window.addEventListener("scroll", onScrollSpy, {{ passive: true }});

// Initialize on load
filterModelShowcase("all", null);
updateLicenseFilter();
updateTcoCalc();
selectQuadrant("Q2", null);
buildRightToc("view-enterprise");
onScrollSpy();
</script>
</body>
</html>
"""

out_html_path = os.path.join(DOCS_DIR, "index.html")
with open(out_html_path, "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)

with open(os.path.join(DOCS_DIR, "CNAME"), "w", encoding="utf-8") as f:
    f.write("openweights.cloudrace.info\n")

with open(os.path.join(DOCS_DIR, ".nojekyll"), "w", encoding="utf-8") as f:
    f.write("")

print("Built 3-pane Claude-Docs-style GitHub Pages prototype at:", out_html_path, "Size:", os.path.getsize(out_html_path))
