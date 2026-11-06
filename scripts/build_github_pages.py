import base64
import html
import os
import re

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
    md_text = re.sub(
        r"https://docs\.google\.com/document/d/[a-zA-Z0-9_-]+(?:/edit[^\)\s]*)?",
        "#full-playbook",
        md_text,
    )
    md_text = re.sub(
        r"https://notebooklm\.google\.com/notebook/[a-zA-Z0-9_-]+",
        "#8-reference-appendices-primary-source-bibliography",
        md_text,
    )
    return md_text


with open(os.path.join(WP_DIR, "enterprise-playbook.md"), "r", encoding="utf-8") as f:
    ent_md_raw = f.read()

ent_md_clean = sanitize_external(ent_md_raw)

# Strip duplicate lead header/disclaimer callout lines that are already surfaced in the Warm Editorial header & hero
ent_md_lines = []
skip_why_blockquote = False
for ln in ent_md_clean.splitlines():
    if ln.startswith("**Authored & Built by:**") or ln.startswith("*Unofficial Google Cloud Practitioner Guide"):
        continue
    if ln.startswith("> **⚠️ Unofficial Guide Disclaimer:**"):
        continue
    if ln.startswith("> **Why Read This Guide?"):
        skip_why_blockquote = True
        continue
    if skip_why_blockquote:
        if ln.startswith(">"):
            continue
        skip_why_blockquote = False
    ent_md_lines.append(ln)

ent_md_html_src = "\n".join(ent_md_lines)

MODULES = [
    (
        "part-02-openmaas-serverless",
        "Part 2 (Nov 13, 2026): Start Serverless — Building Zero-Ops Open-Weight Agents on Vertex AI OpenMaaS",
        "Vertex AI OpenMaaS (`Gemma 4 31B/26B`, `Qwen 3.8`, `DeepSeek-V4.1-Flash`)",
        "Demonstrates why OpenMaaS PayGo (`$0.907/1M` output tokens) beats dedicated self-deploy (`$1.29/1M`, `1.42x` penalty) below `73%` GPU utilization, with cURL and Python SDK tool-calling agent templates.",
    ),
    (
        "part-03-adk-harness-system1",
        "Part 3 (Nov 13, 2026): 'Don't Train the Model, Evolve the Harness' — Multi-Model Routing & Verification with ADK",
        "Google ADK + OpenMaaS + `System 1` Single-Pass Verification",
        "Implements tiered in-harness routing (`64%` lower thread cost) and single-pass `System 1` (`output_tokens: 0`, `35x` faster) pre-submission rubric verification gates (`+16.7pp` accuracy).",
    ),
    (
        "part-04-cloudrun-vllm-qat",
        "Part 4 (Nov 20, 2026): When & How to Self-Host — Scale-to-Zero vLLM & QAT Open Models on Cloud Run",
        "Google Cloud Run GPUs (`vLLM` + `Gemma 4` QAT `E4B`/`26B-A4B`)",
        "Avoids idle GPU burn on bursty custom containers using Cloud Run scale-to-zero GPUs, `vLLM` prefix caching, and `Gemma 4` Quantization-Aware Training (`FP4`/`INT4` with zero tool-call drift).",
    ),
    (
        "part-05-agent-runtime-vpc",
        "Part 5 (Nov 20, 2026): Sovereign & Matter-Isolated Agents — In-VPC Open Weights + System 1 Guardrails on Agent Runtime",
        "Vertex AI Agent Runtime + `System 1` Guardrails & Google Cloud Model Armor",
        "Deploys `SHA-256`-pinned open weights inside air-gapped VPCs with custom `vLLM` prefill heads, `System 1` guardrails, and bidirectional PII redaction (*Pattern 5*).",
    ),
    (
        "part-06-lora-grpo-verifiable-rl",
        "Part 6 (Dec 4, 2026): Beyond the Prompt Tax — LoRA, <$100 Verifiable RL (GRPO), and Multi-LoRA on Vertex AI",
        "Vertex AI Training + OpenMaaS Multi-LoRA + `SkyRL` GRPO",
        "Replaces 10,000-token few-shot prompt bloat with Weight Transfer (`LoRA`/`QLoRA`), single-GPU Verifiable RL (`GRPO`, *Pattern 5*: `<$100`, `+9.6%` F1), and dynamic Multi-LoRA serving.",
    ),
    (
        "part-07-frontier-distillation",
        "Part 7 (Dec 11, 2026): The 'Frontier-to-Open' Distillation Playbook — 10x Cost Cut & <150 ms TTFT",
        "Vertex AI Distillation (`Gemini 3.1 Pro` Teacher -> `Gemma 4` Student)",
        "Uses `Gemini 3.1 Pro` to synthesize rubric-verified domain pairs and distills into compact `Gemma 4` (`26B-A4B` / `E4B`) students for `<150 ms` TTFT at 10% of frontier serving cost (*Patterns 2 & 4*).",
    ),
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

print("Scaffolded series module READMEs.")


def md_inline(text):
    def repl_link(m):
        lbl, url = m.group(1), m.group(2)
        safe_url = html.escape(url, quote=True)
        target = ' target="_blank" rel="noopener noreferrer"' if url.startswith("http") else ""
        return f'<a href="{safe_url}"{target}>{lbl}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl_link, text)
    text = re.sub(r"`([^`]+)`", lambda m: f"<code>{html.escape(m.group(1))}</code>", text)
    text = re.sub(r"\*\*\*([^*]+)\*\*\*", r"<strong><em>\1</em></strong>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = text.replace(r"\$", "$")
    text = text.replace(r"$\rightarrow$", "→")
    return text


ANCHOR_ALIASES = {
    "4-2-high-roi-runtime-drivers-evolving-the-harness-system-1-models": "harness-strategy",
    "4-3-seven-enterprise-watch-outs-how-to-mitigate-them": "security-mitigations",
    "7-ready-to-start-on-google-cloud-watch-this-space": "google-cloud-stack",
}


def md_to_html(md_text):
    lines = md_text.splitlines()
    out = []
    in_ul = False
    in_ol = False
    in_bq = False
    in_table = False
    table_rows = []
    last_heading = ""

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
        nonlocal in_table, table_rows, last_heading
        if not in_table:
            return
        in_table = False
        if len(table_rows) >= 2:
            headers = [c.strip() for c in table_rows[0].strip("|").split("|")]
            body_rows = table_rows[2:]
            out.append('<div class="wp-table-wrap"><table class="wp-table"><thead><tr>')
            for h in headers:
                out.append(f"<th>{md_inline(h)}</th>")
            out.append("</tr></thead><tbody>")
            for r in body_rows:
                cols = [c.strip() for c in r.strip("|").split("|")]
                out.append("<tr>")
                for c in cols:
                    out.append(f"<td>{md_inline(c)}</td>")
                out.append("</tr>")
            out.append("</tbody></table></div>")
        table_rows = []
        if "2.1 Navigating the Three Broad Licensing" in last_heading:
            out.append(
                '<div class="wp-tool-jump">'
                '<span>⚡ <strong>Interactive Tool:</strong> Test all 11 checkpoints &amp; adapters against your valuation, MAU, sovereignty, and auditability gates.</span>'
                '<a href="#license-filter" class="wp-jump-btn">Launch License Triage ↑</a>'
                "</div>"
            )

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
            src = B64_IMGS.get(bname, html.escape(path, quote=True))
            out.append(
                f'<figure class="wp-figure"><img src="{src}" alt="{html.escape(alt, quote=True)}" loading="lazy">'
                f"<figcaption>{html.escape(alt)}</figcaption></figure>"
            )
            continue

        if line.startswith("# "):
            close_lists()
            continue

        if line.startswith("## "):
            close_lists()
            h_txt = line[3:].strip()
            slug = re.sub(r"[^a-z0-9]+", "-", h_txt.lower()).strip("-")
            alias = ANCHOR_ALIASES.get(slug)
            alias_span = f'<span id="{alias}" class="anchor-alias"></span>' if alias else ""
            if h_txt.startswith("8. Reference"):
                out.append(
                    f'<details class="wp-refs" id="{slug}" open>'
                    f"<summary>8. Reference Appendices &amp; Primary Source Bibliography ([1]–[20])</summary>"
                    f'<div class="wp-refs-body">'
                )
            else:
                out.append(f'{alias_span}<h3 class="wp-h2" id="{slug}">{md_inline(h_txt)}</h3>')
                if slug == "7-ready-to-start-on-google-cloud-watch-this-space":
                    out.append(
                        f'<figure class="wp-figure"><img src="{HERO_IMG_B64}" alt="Google Cloud Open-Weight AI Production Reference Stack" loading="lazy">'
                        f"<figcaption>Google Cloud Open-Weight Production Architecture: Vertex AI OpenMaaS, Google ADK + System 1 Gates, Cloud Run Scale-to-Zero vLLM GPUs, and In-VPC Agent Runtime.</figcaption></figure>"
                    )
            last_heading = h_txt
            continue

        if line.startswith("### "):
            close_lists()
            h_txt = line[4:].strip()
            slug = re.sub(r"[^a-z0-9]+", "-", h_txt.lower()).strip("-")
            alias = ANCHOR_ALIASES.get(slug)
            alias_span = f'<span id="{alias}" class="anchor-alias"></span>' if alias else ""
            out.append(f'{alias_span}<h4 class="wp-h3" id="{slug}">{md_inline(h_txt)}</h4>')
            last_heading = h_txt
            continue

        if line.startswith(">"):
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_bq:
                out.append('<div class="wp-callout">')
                in_bq = True
            bq_content = line.lstrip("> ").strip()
            if bq_content.startswith("- "):
                out.append(f'<div class="wp-callout-bullet">• {md_inline(bq_content[2:])}</div>')
            elif bq_content:
                out.append(f"<p>{md_inline(bq_content)}</p>")
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
                out.append('<ul class="wp-list">')
                in_ul = True
            item_txt = m_ul.group(2)
            out.append(f"<li>{md_inline(item_txt)}</li>")
            if "6.1 The 73% Duty-Cycle Rule" in last_heading and "Enterprise Mitigation:" in item_txt:
                close_lists()
                out.append(
                    '<div class="wp-tool-jump">'
                    '<span>⚡ <strong>Interactive Tool:</strong> Model your daily output tokens &amp; GPU duty cycle against the 73% break-even rule.</span>'
                    '<a href="#quick-calculators" class="wp-jump-btn">Open FinOps Calculator ↑</a>'
                    "</div>"
                )
                last_heading = ""
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
                out.append('<ol class="wp-list wp-ol">')
                in_ol = True
            out.append(f"<li>{md_inline(m_ol.group(2))}</li>")
            continue

        close_lists()
        out.append(f'<p class="wp-p">{md_inline(line)}</p>')
        if "6.2 Interactive Workload & Architecture Router" in last_heading:
            out.append(
                '<div class="wp-tool-jump">'
                '<span>⚡ <strong>Interactive Tool:</strong> Click any quadrant of the 2×2 matrix to map your workload to Google Cloud reference stacks.</span>'
                '<a href="#workload-router" class="wp-jump-btn">Open 2×2 Workload Router ↑</a>'
                "</div>"
            )
            last_heading = ""

    close_lists()
    flush_table()
    joined = "\n".join(out)
    if '<details class="wp-refs"' in joined:
        joined += "</div></details>"
    return joined


ent_body_html = md_to_html(ent_md_html_src)

# Inline crisp SVGs (replacing external Material Symbols font ligatures for zero-FOUT & offline reliability)
SVG_CALC = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="11" x2="10" y2="11"/><line x1="14" y1="11" x2="16" y2="11"/><line x1="8" y1="15" x2="10" y2="15"/><line x1="14" y1="15" x2="16" y2="15"/><line x1="8" y1="19" x2="16" y2="19"/></svg>'
SVG_SHIELD = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>'
SVG_CUBE = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m21 16-9 5-9-5V8l9-5 9 5z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>'
SVG_ROUTE = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="19" r="3"/><path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15"/><circle cx="18" cy="5" r="3"/></svg>'
SVG_BOOK = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>'
SVG_EXT = '<svg class="ico-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
SVG_ARROW = '<svg class="ico-sm arrow-shift" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>'
SVG_SPARKLE = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/></svg>'
SVG_TUNE = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="2" y1="14" x2="6" y2="14"/><line x1="10" y1="8" x2="14" y2="8"/><line x1="18" y1="16" x2="22" y2="16"/></svg>'
SVG_PLAY = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polygon points="10 8 16 12 10 16 10 8" fill="currentColor"/></svg>'
SVG_INFO = '<svg class="ico-lg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>'
SVG_CHECK = '<svg class="ico-lg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
SVG_MEDAL = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>'
SVG_CLOUD = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>'
SVG_SPEED = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/></svg>'
SVG_GITHUB = '<svg class="ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>'

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="referrer" content="strict-origin-when-cross-origin">
<!-- TODO(security): Static GitHub Pages hosting cannot emit per-request script nonces or HTTP X-Frame-Options/CSP response headers; enforce strict nonce-based CSP and frame-ancestors at reverse-proxy/CDN layer if migrated off static Pages. -->
<title>Enterprise Architect&#39;s Guide to Open-Weight AI Models — OpenWeights Playbook</title>
<meta name="description" content="Interactive enterprise architecture playbook, FinOps 73% duty-cycle calculator, license-triage filter, 5-minute explainer video, and 7-part Google Cloud code series for open-weight AI models.">
<link rel="canonical" href="https://openweights.cloudrace.info/">
<meta property="og:title" content="Open-Weight AI Models — Enterprise Architect&#39;s Playbook &amp; Toolkit">
<meta property="og:description" content="56% of gateway tokens at 14% of spend: interactive license filter, 73% GPU duty-cycle FinOps calculator, 5-min video walkthrough, and 7-part Google Cloud code series.">
<meta property="og:url" content="https://openweights.cloudrace.info/">
<meta property="og:type" content="website">
<meta property="og:image" content="https://openweights.cloudrace.info/assets/youtube_explainer_thumbnail.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Open-Weight AI Models — Enterprise Architect&#39;s Playbook &amp; Toolkit">
<meta name="twitter:description" content="Interactive license filter, 73% GPU duty-cycle FinOps calculator, 5-min explainer video, and 7-part Google Cloud code series.">
<meta name="twitter:image" content="https://openweights.cloudrace.info/assets/youtube_explainer_thumbnail.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&amp;family=Raleway:wght@400;500;600;700&amp;family=Red+Hat+Mono:wght@400;500;600&amp;display=swap" rel="stylesheet">
<style>
  :root {{
    --coral: #C85028;
    --coral-bright: #E06338;
    --amber: #D9822B;
    --amber-deep: #9E5A14;
    --plum: #4A235A;
    --forest: #1E2E28;
    --forest-deep: #16221D;
    --success: #2D6A4F;
    --danger: #C53030;
    --surface: #FAF8F5;
    --surface-container: #FFFFFF;
    --surface-high: #F2ECE4;
    --surface-highlight: #FFF5ED;
    --on-surface: #1A1816;
    --on-surface-variant: #5C564E;
    --outline: #DDD5CA;
    --outline-variant: #ECE6DC;
    --font-headline: "Playfair Display", Georgia, "Times New Roman", serif;
    --font-body: "Raleway", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    --font-code: "Red Hat Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
    --shadow-xs: 0 2px 8px -2px rgba(40, 30, 20, 0.05);
    --shadow-sm: 0 2px 8px -2px rgba(40, 30, 20, 0.05), 0 12px 28px -6px rgba(40, 30, 20, 0.05);
    --shadow-md: 0 6px 18px -4px rgba(40, 30, 20, 0.08), 0 18px 36px -10px rgba(40, 30, 20, 0.07);
    --radius-sm: 4px;
    --radius: 8px;
    --radius-md: 10px;
    --radius-lg: 12px;
    --radius-xl: 18px;
  }}

  *, *::before, *::after {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; scroll-padding-top: 92px; }}
  body {{
    margin: 0;
    min-height: 100vh;
    background-color: var(--surface);
    color: var(--on-surface);
    font-family: var(--font-body);
    font-size: 15px;
    line-height: 1.56;
    -webkit-font-smoothing: antialiased;
  }}
  ::selection {{
    background: rgba(217, 130, 43, 0.22);
    color: var(--forest);
  }}
  a {{ color: var(--coral); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  button, select, input {{ font-family: inherit; }}
  .tabular {{ font-variant-numeric: tabular-nums; }}
  .anchor-alias {{ display: block; position: relative; top: -92px; visibility: hidden; height: 0; }}

  .ico {{ width: 16px; height: 16px; flex-shrink: 0; vertical-align: middle; }}
  .ico-sm {{ width: 14px; height: 14px; flex-shrink: 0; vertical-align: middle; }}
  .ico-lg {{ width: 22px; height: 22px; flex-shrink: 0; }}

  /* =========================================================
     1. STICKY TOP HEADER & UNOFFICIAL BANNER (Warm Editorial)
     ========================================================= */
  .site-header {{
    position: sticky;
    top: 0;
    z-index: 200;
    background: linear-gradient(90deg, rgba(250, 248, 245, 0.95) 0%, rgba(255, 255, 255, 0.96) 50%, rgba(250, 245, 238, 0.95) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--outline-variant);
    box-shadow: var(--shadow-xs);
  }}
  .top-gradient-bar {{
    height: 4px;
    width: 100%;
    background: linear-gradient(90deg, var(--coral) 0%, var(--amber) 34%, var(--forest) 68%, var(--plum) 100%);
  }}
  .header-inner {{
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 24px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
  }}
  .brand-link {{
    display: flex;
    align-items: center;
    gap: 13px;
    color: inherit;
    text-decoration: none;
  }}
  .brand-link:hover {{ text-decoration: none; }}
  .brand-monogram {{
    width: 36px;
    height: 36px;
    border-radius: var(--radius-md);
    background: linear-gradient(135deg, var(--forest) 0%, #121A15 100%);
    color: var(--amber);
    border: 1px solid rgba(217, 130, 43, 0.36);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-headline);
    font-weight: 700;
    font-size: 17px;
    box-shadow: var(--shadow-xs);
    flex-shrink: 0;
  }}
  .brand-title-row {{
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }}
  .brand-name {{
    font-family: var(--font-headline);
    font-size: 18px;
    font-weight: 700;
    letter-spacing: -0.01em;
    color: var(--on-surface);
  }}
  .edition-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 11.5px;
    font-weight: 600;
    background: linear-gradient(90deg, rgba(217, 130, 43, 0.20), rgba(200, 80, 40, 0.12));
    color: var(--forest);
    border: 1px solid rgba(217, 130, 43, 0.34);
  }}
  .pulse-dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--coral);
    animation: pulseGlow 2.2s ease-in-out infinite;
  }}
  @keyframes pulseGlow {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.45; transform: scale(0.85); }}
  }}
  .brand-sub {{
    margin: 1px 0 0 0;
    font-size: 12.5px;
    color: var(--on-surface-variant);
  }}

  .toolkit-dock {{
    display: flex;
    align-items: center;
    gap: 3px;
    padding: 4px;
    border-radius: var(--radius-md);
    background: linear-gradient(90deg, var(--surface-high), #FFFFFF, var(--surface-high));
    border: 1px solid var(--outline-variant);
    box-shadow: var(--shadow-xs);
  }}
  .dock-tab {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 11px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    color: var(--on-surface);
    text-decoration: none;
    transition: all 0.14s ease-out;
    white-space: nowrap;
  }}
  .dock-tab:hover {{
    color: var(--coral);
    background: var(--surface-highlight);
    text-decoration: none;
  }}
  .dock-tab .c-coral {{ color: var(--coral); }}
  .dock-tab .c-success {{ color: var(--success); }}
  .dock-tab .c-plum {{ color: var(--plum); }}
  .dock-tab .c-amber {{ color: var(--amber); }}
  .dock-tab .c-forest {{ color: var(--forest); }}

  .header-actions {{
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;
  }}
  .btn-gh {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    border-radius: var(--radius-md);
    border: 1px solid var(--outline-variant);
    background: linear-gradient(180deg, #FFFFFF 0%, #F9F5EF 100%);
    color: var(--on-surface);
    font-size: 12px;
    font-weight: 600;
    box-shadow: var(--shadow-xs);
    transition: background 0.14s ease;
    text-decoration: none;
  }}
  .btn-gh:hover {{
    background: var(--surface-high);
    text-decoration: none;
  }}
  .btn-dispatch {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 7px 14px;
    border-radius: var(--radius-md);
    background: linear-gradient(90deg, var(--forest) 0%, #2D453C 100%);
    color: var(--amber);
    font-size: 12px;
    font-weight: 700;
    box-shadow: var(--shadow-xs);
    transition: filter 0.15s ease, transform 0.15s ease;
    text-decoration: none;
    white-space: nowrap;
  }}
  .btn-dispatch:hover {{
    filter: brightness(1.08);
    transform: translateY(-1px);
    text-decoration: none;
  }}

  .unofficial-banner {{
    background: linear-gradient(90deg, #FFF8E7 0%, #FFF3D6 50%, #FFEED0 100%);
    border-bottom: 1px solid #F0E2C0;
    color: #4A3B18;
    padding: 9px 16px;
    font-size: 13px;
    text-align: center;
  }}
  .unofficial-inner {{
    max-width: 1280px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 6px;
  }}
  .unofficial-strong {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-weight: 700;
    color: var(--forest);
  }}
  .unofficial-strong svg {{ color: var(--amber); }}

  /* Mobile Quick Jump Bar */
  .mobile-jump-bar {{
    display: none;
    overflow-x: auto;
    gap: 8px;
    padding: 10px 16px;
    background: #FFFFFF;
    border-bottom: 1px solid var(--outline-variant);
  }}
  .mobile-jump-bar a {{
    flex-shrink: 0;
    padding: 5px 11px;
    border-radius: 999px;
    border: 1px solid var(--outline-variant);
    background: var(--surface);
    color: var(--forest);
    font-size: 12px;
    font-weight: 600;
    text-decoration: none;
  }}

  @media (max-width: 1120px) {{
    .toolkit-dock {{ display: none; }}
    .mobile-jump-bar {{ display: flex; }}
  }}
  @media (max-width: 640px) {{
    .brand-sub, .edition-pill, .btn-gh .gh-lbl {{ display: none; }}
    .header-inner {{ padding: 0 14px; }}
  }}

  /* =========================================================
     2. 12-COLUMN APP GRID & LEFT STICKY SIDEBAR
     ========================================================= */
  .page-shell {{
    max-width: 1280px;
    margin: 0 auto;
    padding: 32px 24px 56px;
    display: grid;
    grid-template-columns: 280px minmax(0, 1fr);
    gap: 32px;
    align-items: start;
  }}
  @media (max-width: 1024px) {{
    .page-shell {{
      grid-template-columns: 1fr;
      padding: 20px 16px 44px;
    }}
    .left-rail {{ display: none; }}
  }}

  .left-rail {{
    position: sticky;
    top: 86px;
    max-height: calc(100vh - 102px);
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 18px;
    padding-right: 2px;
  }}
  .rail-card {{
    background: var(--surface-container);
    border: 1px solid var(--outline-variant);
    border-radius: var(--radius-lg);
    padding: 18px;
    box-shadow: var(--shadow-xs);
  }}
  .rail-head {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: 1px solid var(--outline-variant);
  }}
  .rail-eyebrow {{
    font-size: 11.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--on-surface-variant);
  }}
  .rail-ver {{
    font-family: var(--font-code);
    font-size: 11px;
    font-weight: 600;
    color: var(--coral);
  }}
  .toc-nav {{
    display: flex;
    flex-direction: column;
    gap: 3px;
  }}
  .toc-item {{
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 6px 10px;
    border-radius: var(--radius);
    font-size: 13px;
    font-weight: 500;
    color: var(--on-surface-variant);
    text-decoration: none;
    transition: all 0.14s ease;
  }}
  .toc-item:hover {{
    background: var(--surface);
    color: var(--on-surface);
    text-decoration: none;
  }}
  .toc-dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--outline);
    flex-shrink: 0;
  }}
  .toc-item.active {{
    background: var(--surface-highlight);
    color: var(--coral);
    font-weight: 700;
  }}
  .toc-item.active .toc-dot {{
    background: var(--coral);
  }}

  .dispatch-title-row {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
    color: var(--coral);
  }}
  .dispatch-title-row span {{
    font-family: var(--font-headline);
    font-size: 15px;
    font-weight: 700;
    color: var(--on-surface);
  }}
  .dispatch-sub {{
    margin: 0 0 10px 0;
    font-size: 12.5px;
    color: var(--on-surface-variant);
  }}
  .dispatch-list {{
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}
  .dispatch-link {{
    display: flex;
    align-items: flex-start;
    gap: 9px;
    padding: 8px 10px;
    border-radius: var(--radius);
    background: var(--surface);
    border: 1px solid transparent;
    text-decoration: none;
    transition: all 0.14s ease;
  }}
  .dispatch-link:hover {{
    background: var(--surface-high);
    border-color: var(--outline);
    text-decoration: none;
  }}
  .dispatch-link.live {{
    background: var(--surface-highlight);
    border-color: #F5D5C5;
  }}
  .dispatch-num {{
    font-family: var(--font-code);
    font-size: 12px;
    font-weight: 700;
    color: #9E9589;
    margin-top: 1px;
  }}
  .dispatch-link.live .dispatch-num {{ color: var(--coral); }}
  .dispatch-name {{
    display: block;
    font-size: 12.5px;
    font-weight: 600;
    color: var(--on-surface);
    line-height: 1.3;
  }}
  .dispatch-link.live .dispatch-name {{ color: var(--coral); font-weight: 700; }}
  .dispatch-date {{
    display: block;
    font-size: 11.5px;
    color: var(--on-surface-variant);
    margin-top: 1px;
  }}

  .author-list {{
    display: flex;
    flex-direction: column;
    gap: 9px;
    margin-top: 10px;
  }}
  .author-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    font-weight: 600;
    color: var(--on-surface);
  }}
  .author-row.guidance {{
    padding-top: 9px;
    border-top: 1px solid var(--outline-variant);
    color: var(--on-surface-variant);
    font-weight: 500;
  }}
  .avatar-badge {{
    width: 25px;
    height: 25px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
    flex-shrink: 0;
  }}
  .av-kp {{ background: var(--coral); color: #FFFFFF; }}
  .av-as {{ background: var(--forest); color: var(--amber); }}
  .av-ab {{ background: var(--plum); color: #FFFFFF; }}

  /* =========================================================
     3. MAIN WORKBENCH & HERO SECTION
     ========================================================= */
  .main-col {{
    display: flex;
    flex-direction: column;
    gap: 44px;
    min-width: 0;
  }}

  .hero-card {{
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #FFFFFF 0%, #FFFBF7 52%, #FFF3E8 100%);
    border: 1px solid #EFE3D3;
    border-radius: var(--radius-xl);
    padding: clamp(24px, 3.6vw, 40px);
    box-shadow: var(--shadow-sm);
  }}
  .hero-orb-tr {{
    position: absolute;
    top: -96px;
    right: -96px;
    width: 360px;
    height: 360px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(217, 130, 43, 0.22) 0%, rgba(200, 80, 40, 0.12) 45%, transparent 72%);
    pointer-events: none;
  }}
  .hero-orb-bl {{
    position: absolute;
    bottom: -80px;
    left: -80px;
    width: 300px;
    height: 300px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(200, 80, 40, 0.10) 0%, rgba(74, 35, 90, 0.08) 50%, transparent 72%);
    pointer-events: none;
  }}
  .hero-content {{
    position: relative;
    z-index: 1;
    max-width: 820px;
  }}
  .hero-eyebrow {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 4px 13px;
    border-radius: 999px;
    background: linear-gradient(90deg, rgba(217, 130, 43, 0.20), rgba(217, 130, 43, 0.10), rgba(200, 80, 40, 0.14));
    border: 1px solid rgba(217, 130, 43, 0.34);
    color: var(--forest);
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 16px;
  }}
  .hero-eyebrow svg {{ color: var(--amber); }}
  .hero-h1 {{
    font-family: var(--font-headline);
    font-size: clamp(30px, 3.6vw, 44px);
    line-height: 1.17;
    letter-spacing: -0.015em;
    font-weight: 700;
    color: var(--forest);
    margin: 0 0 16px 0;
  }}
  .hero-lead {{
    font-size: 17px;
    line-height: 1.56;
    color: var(--on-surface-variant);
    margin: 0 0 24px 0;
  }}
  .hero-lead .hl-forest {{ color: var(--forest); font-weight: 700; }}
  .hero-lead .hl-coral {{ color: var(--coral); font-weight: 700; }}

  .stat-strip {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    padding: 18px 20px;
    border-radius: var(--radius-lg);
    background: linear-gradient(180deg, #FFFFFF 0%, #FAF6F0 100%);
    border: 1px solid var(--outline-variant);
    margin-bottom: 26px;
    box-shadow: var(--shadow-xs);
  }}
  @media (max-width: 680px) {{
    .stat-strip {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  }}
  .stat-cell {{
    padding: 8px 10px;
    border-radius: var(--radius);
  }}
  .stat-cell.s-coral {{ background: linear-gradient(135deg, rgba(200, 80, 40, 0.06), transparent); }}
  .stat-cell.s-success {{ background: linear-gradient(135deg, rgba(45, 106, 79, 0.06), transparent); }}
  .stat-cell.s-amber {{ background: linear-gradient(135deg, rgba(217, 130, 43, 0.07), transparent); }}
  .stat-cell.s-plum {{ background: linear-gradient(135deg, rgba(74, 35, 90, 0.06), transparent); }}
  .stat-num {{
    display: block;
    font-family: var(--font-headline);
    font-size: 28px;
    line-height: 1.18;
    font-weight: 700;
    margin-bottom: 2px;
  }}
  .s-coral .stat-num {{ color: var(--coral); }}
  .s-success .stat-num {{ color: var(--success); }}
  .s-amber .stat-num {{ color: var(--amber); }}
  .s-plum .stat-num {{ color: var(--plum); }}
  .stat-lbl {{
    font-size: 12.5px;
    font-weight: 600;
    color: var(--on-surface-variant);
  }}

  .hero-ctas {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 12px;
  }}
  .btn-primary-coral {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: var(--radius);
    background: linear-gradient(90deg, var(--coral) 0%, var(--coral-bright) 100%);
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    box-shadow: var(--shadow-xs);
    transition: all 0.15s ease;
    text-decoration: none;
  }}
  .btn-primary-coral:hover {{
    background: var(--forest);
    color: #FFFFFF;
    text-decoration: none;
    transform: translateY(-1px);
  }}
  .btn-secondary-warm {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 18px;
    border-radius: var(--radius);
    background: linear-gradient(180deg, #FFFFFF 0%, #F9F5EF 100%);
    border: 1px solid var(--outline);
    color: var(--on-surface);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    box-shadow: var(--shadow-xs);
    transition: all 0.15s ease;
    text-decoration: none;
  }}
  .btn-secondary-warm:hover {{
    background: var(--surface-high);
    border-color: #C7BBAE;
    color: var(--forest);
    text-decoration: none;
  }}
  .btn-video-ghost {{
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 10px 14px;
    border-radius: var(--radius);
    background: transparent;
    border: 1px solid transparent;
    color: var(--on-surface-variant);
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
  }}
  .btn-video-ghost svg {{ color: var(--coral); width: 20px; height: 20px; }}
  .btn-video-ghost:hover {{
    color: var(--coral);
    background: var(--surface-highlight);
    border-color: #F5D5C5;
  }}

  /* =========================================================
     4. 5-MINUTE VIDEO TOUR SPOTLIGHT (Warm Editorial)
     ========================================================= */
  .video-card {{
    background: linear-gradient(135deg, #FFFFFF 0%, #FFFBF7 55%, #FFF5ED 100%);
    border: 1px solid #EFE2D2;
    border-radius: var(--radius-xl);
    padding: 14px;
    box-shadow: var(--shadow-xs);
  }}
  .yt-stage {{
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 9;
    border-radius: var(--radius-lg);
    overflow: hidden;
    background: var(--forest-deep);
    border: 1px solid var(--outline);
    box-shadow: var(--shadow-md);
  }}
  .yt-stage iframe {{
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
    background: var(--forest-deep);
    cursor: pointer;
    display: block;
  }}
  .yt-poster-btn img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.24s ease, filter 0.24s ease;
  }}
  .yt-poster-btn:hover img {{
    transform: scale(1.018);
    filter: brightness(1.04);
  }}
  .yt-play-circle {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 68px;
    height: 68px;
    border-radius: 50%;
    background: rgba(200, 80, 40, 0.94);
    border: 2.5px solid #FFF8E7;
    box-shadow: 0 12px 28px rgba(22, 34, 29, 0.55);
    display: grid;
    place-items: center;
    transition: transform 0.18s ease, background 0.18s ease;
  }}
  .yt-poster-btn:hover .yt-play-circle {{
    transform: translate(-50%, -50%) scale(1.08);
    background: var(--coral-bright);
  }}
  .yt-play-circle svg {{ width: 26px; height: 26px; fill: #FFFFFF; margin-left: 3px; }}
  .yt-dur-pill {{
    position: absolute;
    right: 12px;
    bottom: 12px;
    background: rgba(22, 34, 29, 0.90);
    color: #FAF8F5;
    border: 1px solid rgba(217, 130, 43, 0.45);
    font-family: var(--font-code);
    font-size: 11.5px;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 6px;
  }}

  /* =========================================================
     5. SECTION HEADERS & 5 ARCHITECT QUESTIONS BENTO
     ========================================================= */
  .sec-header {{
    display: flex;
    flex-wrap: wrap;
    align-items: flex-end;
    justify-content: space-between;
    gap: 12px;
    padding-bottom: 14px;
    margin-bottom: 22px;
    border-bottom: 1px solid var(--outline-variant);
  }}
  .sec-eyebrow {{
    display: block;
    font-family: var(--font-code);
    font-size: 12.5px;
    font-weight: 600;
    color: var(--coral);
    letter-spacing: 0.03em;
    margin-bottom: 3px;
  }}
  .sec-h2 {{
    font-family: var(--font-headline);
    font-size: clamp(24px, 2.5vw, 28px);
    line-height: 1.25;
    font-weight: 700;
    color: var(--forest);
    margin: 0;
    letter-spacing: -0.01em;
  }}
  .sec-sub {{
    font-size: 13.5px;
    color: var(--on-surface-variant);
    margin: 4px 0 0 0;
    max-width: 540px;
  }}

  .q-bento-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
  }}
  .q-card-span2 {{ grid-column: span 2; }}
  @media (max-width: 820px) {{
    .q-bento-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    .q-card-span2 {{ grid-column: span 2; }}
  }}
  @media (max-width: 560px) {{
    .q-bento-grid {{ grid-template-columns: 1fr; }}
    .q-card-span2 {{ grid-column: span 1; }}
  }}
  .q-bento-card {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 20px;
    border-radius: var(--radius-lg);
    border: 1px solid var(--outline-variant);
    box-shadow: var(--shadow-xs);
    text-decoration: none;
    color: inherit;
    transition: all 0.16s ease;
  }}
  .q-bento-card:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
    text-decoration: none;
  }}
  .q-bento-card:hover .arrow-shift {{ transform: translateX(4px); }}
  .arrow-shift {{ transition: transform 0.16s ease; }}

  .qc-coral {{ background: linear-gradient(135deg, #FFFFFF 0%, #FFFFFF 55%, #FFF9F5 100%); }}
  .qc-coral:hover {{ border-color: var(--coral); }}
  .qc-forest {{ background: linear-gradient(135deg, #FFFFFF 0%, #FFFFFF 55%, #F5F8F6 100%); }}
  .qc-forest:hover {{ border-color: var(--forest); }}
  .qc-amber {{ background: linear-gradient(135deg, #FFFFFF 0%, #FFFFFF 55%, #FFFDF5 100%); }}
  .qc-amber:hover {{ border-color: var(--amber); }}
  .qc-plum {{ background: linear-gradient(135deg, #FFFFFF 0%, #FFFFFF 55%, #FAF6FB 100%); }}
  .qc-plum:hover {{ border-color: var(--plum); }}
  .qc-finops {{ background: linear-gradient(135deg, #FFFFFF 0%, #FFFFFF 55%, #F4F9F6 100%); }}
  .qc-finops:hover {{ border-color: var(--forest); }}

  .q-top-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 11px;
  }}
  .q-code {{
    font-family: var(--font-code);
    font-size: 12.5px;
    font-weight: 700;
  }}
  .q-pill {{
    font-size: 11.5px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: var(--radius-sm);
  }}
  .pill-green {{ background: linear-gradient(90deg, #E8F5E9, #DDF0DE); color: var(--success); border: 1px solid #C8E6C9; }}
  .pill-amber {{ background: linear-gradient(90deg, #FFF8E7, #FFF1D0); color: var(--amber-deep); border: 1px solid #F0E2C0; }}
  .pill-plum {{ background: linear-gradient(90deg, #F4ECF7, #FCEEF9); color: var(--plum); border: 1px solid #E8DAEF; }}
  .pill-coral {{ background: linear-gradient(90deg, #FFF5ED, #FFEFE0); color: var(--coral); border: 1px solid #F5D5C5; }}
  .pill-red {{ background: linear-gradient(90deg, #FFEBEE, #FFDADA); color: var(--danger); border: 1px solid #FFCDD2; }}

  .q-title {{
    font-family: var(--font-headline);
    font-size: 18.5px;
    line-height: 1.3;
    font-weight: 700;
    color: var(--forest);
    margin: 0 0 8px 0;
  }}
  .q-desc {{
    font-size: 13.5px;
    color: var(--on-surface-variant);
    margin: 0 0 14px 0;
  }}
  .q-foot {{
    padding-top: 11px;
    border-top: 1px solid var(--outline-variant);
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 12.5px;
    font-weight: 700;
  }}

  /* =========================================================
     6. INTERACTIVE TOOLKIT WORKBENCHES (FinOps, License, Router)
     ========================================================= */
  .workbench-card {{
    background: linear-gradient(135deg, #FFFFFF 0%, #FCFAF7 100%);
    border: 1px solid var(--outline-variant);
    border-radius: var(--radius-xl);
    padding: clamp(20px, 3vw, 32px);
    box-shadow: var(--shadow-sm);
  }}
  .wb-head {{
    padding-bottom: 16px;
    margin-bottom: 22px;
    border-bottom: 1px solid var(--outline-variant);
  }}
  .wb-top-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 6px;
  }}
  .wb-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: var(--radius-sm);
    background: linear-gradient(90deg, rgba(217, 130, 43, 0.20), rgba(217, 130, 43, 0.08));
    border: 1px solid rgba(217, 130, 43, 0.34);
    color: var(--forest);
    font-size: 12px;
    font-weight: 700;
  }}
  .wb-meta {{
    font-family: var(--font-code);
    font-size: 12.5px;
    color: var(--on-surface-variant);
  }}
  .wb-desc {{
    margin: 6px 0 0 0;
    font-size: 14.5px;
    color: var(--on-surface-variant);
  }}

  /* FinOps Sliders */
  .sliders-panel {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 22px;
    padding: 20px;
    border-radius: var(--radius-lg);
    background: linear-gradient(180deg, #FFFFFF 0%, #FAF6F0 100%);
    border: 1px solid var(--outline-variant);
    margin-bottom: 20px;
  }}
  @media (max-width: 720px) {{
    .sliders-panel {{ grid-template-columns: 1fr; }}
  }}
  .slider-head {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 12.5px;
  }}
  .slider-head label {{ font-weight: 700; color: var(--on-surface); }}
  .slider-val-coral {{ font-family: var(--font-code); font-size: 14px; font-weight: 700; color: var(--coral); }}
  .slider-val-amber {{ font-family: var(--font-code); font-size: 14px; font-weight: 700; color: var(--amber-deep); }}
  .range-coral, .range-amber {{
    width: 100%;
    height: 8px;
    border-radius: 999px;
    cursor: pointer;
  }}
  .range-coral {{ accent-color: var(--coral); }}
  .range-amber {{ accent-color: var(--amber); }}
  .slider-ticks {{
    display: flex;
    justify-content: space-between;
    margin-top: 6px;
    font-family: var(--font-code);
    font-size: 11.5px;
    color: var(--on-surface-variant);
  }}

  .finops-cards {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin-bottom: 18px;
  }}
  @media (max-width: 900px) {{
    .finops-cards {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  }}
  @media (max-width: 500px) {{
    .finops-cards {{ grid-template-columns: 1fr; }}
  }}
  .f-card {{
    padding: 16px;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-xs);
  }}
  .fc-closed {{ background: linear-gradient(180deg, #FFFFFF, #FBF9F6); border: 1px solid var(--outline-variant); }}
  .fc-maas {{ background: linear-gradient(135deg, #FFF5ED, #FFEFE0); border: 1px solid #F5D5C5; }}
  .fc-ded {{ background: linear-gradient(135deg, #FFF8E7, #FFF1D0); border: 1px solid #F0E2C0; }}
  .fc-sys1 {{ background: linear-gradient(135deg, #E8F5E9, #DDF0DE); border: 1px solid #C8E6C9; }}
  .f-lbl {{ display: block; font-size: 12px; font-weight: 700; margin-bottom: 3px; }}
  .f-rate {{ display: block; font-family: var(--font-code); font-size: 12px; }}
  .f-price {{
    font-family: var(--font-headline);
    font-size: 23px;
    font-weight: 700;
    margin: 8px 0 6px;
  }}
  .f-bar-track {{
    height: 5px;
    border-radius: 999px;
    background: rgba(26, 24, 22, 0.08);
    overflow: hidden;
    margin-bottom: 6px;
  }}
  .f-bar-fill {{
    height: 100%;
    border-radius: 999px;
    transition: width 0.18s ease;
  }}
  .f-note {{ display: block; font-size: 12px; font-weight: 600; }}

  .verdict-box {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 16px 18px;
    border-radius: var(--radius-lg);
  }}
  .verdict-coral {{
    background: linear-gradient(90deg, #FFF5ED 0%, #FFF9F2 50%, #FFF3E8 100%);
    border: 1px solid #F5D5C5;
    color: var(--coral);
  }}
  .verdict-green {{
    background: linear-gradient(90deg, #E8F5E9 0%, #F1F8E9 100%);
    border: 1px solid #C8E6C9;
    color: var(--success);
  }}
  .verdict-title {{
    display: block;
    font-family: var(--font-headline);
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 4px;
  }}
  .verdict-body {{
    margin: 0;
    font-size: 13.5px;
    line-height: 1.52;
    color: var(--on-surface-variant);
  }}

  /* =========================================================
     7. 11 OPEN-WEIGHT MODELS CATALOG & FILTER PILLS
     ========================================================= */
  .filter-bar {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 20px;
  }}
  .model-filter-btn {{
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 12.5px;
    font-weight: 600;
    background: var(--surface-container);
    border: 1px solid var(--outline-variant);
    color: var(--on-surface);
    cursor: pointer;
    transition: all 0.14s ease;
  }}
  .model-filter-btn:hover {{ border-color: var(--coral); color: var(--coral); }}
  .model-filter-btn.active {{
    background: var(--coral);
    border-color: var(--coral);
    color: #FFFFFF;
    box-shadow: var(--shadow-xs);
  }}

  .models-grid {{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
  }}
  @media (max-width: 900px) {{ .models-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
  @media (max-width: 580px) {{ .models-grid {{ grid-template-columns: 1fr; }} }}

  .model-card {{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 18px;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-xs);
    transition: all 0.16s ease;
  }}
  .model-card:hover {{ transform: translateY(-2px); box-shadow: var(--shadow-md); }}
  .mc-coral {{ background: linear-gradient(135deg, #FFFFFF 0%, #FCFAF7 55%, #FFF5ED 100%); border: 1px solid #EFE2D2; }}
  .mc-coral:hover {{ border-color: var(--coral); }}
  .mc-green {{ background: linear-gradient(135deg, #FFFFFF 0%, #FCFAF7 55%, #F2F8F4 100%); border: 1px solid #E0EFE5; }}
  .mc-green:hover {{ border-color: var(--success); }}
  .mc-amber {{ background: linear-gradient(135deg, #FFFFFF 0%, #FCFAF7 55%, #FFF8E7 100%); border: 1px solid #F0E6D0; }}
  .mc-amber:hover {{ border-color: var(--amber); }}
  .mc-plum {{ background: linear-gradient(135deg, #FFFFFF 0%, #FCFAF7 55%, #FBF5FD 100%); border: 1px solid #EADBF0; }}
  .mc-plum:hover {{ border-color: var(--plum); }}
  .mc-red {{ background: linear-gradient(135deg, #FFFFFF 0%, #FCFAF7 55%, #FFF0F0 100%); border: 1px solid #FADBD8; }}
  .mc-red:hover {{ border-color: var(--danger); }}

  .mc-top {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 6px;
  }}
  .mc-name {{
    font-family: var(--font-headline);
    font-size: 17.5px;
    line-height: 1.25;
    font-weight: 700;
    color: var(--forest);
    margin: 0;
  }}
  .mc-lic {{
    font-family: var(--font-code);
    font-size: 11px;
    font-weight: 600;
    padding: 2px 7px;
    border-radius: var(--radius-sm);
    white-space: nowrap;
    flex-shrink: 0;
  }}
  .mc-arch {{
    font-size: 12.5px;
    font-weight: 600;
    color: var(--on-surface-variant);
    margin-bottom: 8px;
  }}
  .mc-body {{
    font-size: 13px;
    color: var(--on-surface);
    line-height: 1.5;
    margin: 0 0 12px 0;
  }}
  .mc-foot {{
    padding-top: 10px;
    border-top: 1px solid var(--outline-variant);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 11.5px;
  }}
  .mc-cloud {{
    font-family: var(--font-code);
    color: var(--on-surface-variant);
    font-weight: 500;
  }}
  .mc-link {{
    font-weight: 700;
    white-space: nowrap;
  }}

  /* =========================================================
     8. LICENSE & AUDITABILITY TRIAGE (4 Dropdowns + All Models)
     ========================================================= */
  .triage-controls {{
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    padding: 18px;
    border-radius: var(--radius-lg);
    background: var(--surface);
    border: 1px solid var(--outline-variant);
    margin-bottom: 16px;
  }}
  @media (max-width: 820px) {{ .triage-controls {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
  @media (max-width: 500px) {{ .triage-controls {{ grid-template-columns: 1fr; }} }}
  .triage-field label {{
    display: block;
    font-size: 12px;
    font-weight: 700;
    color: var(--on-surface);
    margin-bottom: 6px;
  }}
  .triage-select {{
    width: 100%;
    padding: 8px 11px;
    border-radius: var(--radius);
    border: 1px solid var(--outline);
    background: #FFFFFF;
    color: var(--on-surface);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
  }}
  .triage-select:focus {{
    outline: 2px solid rgba(200, 80, 40, 0.25);
    border-color: var(--coral);
  }}
  .triage-summary-bar {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 12px;
    font-size: 12.5px;
    color: var(--on-surface-variant);
  }}
  .triage-tally {{
    font-family: var(--font-code);
    font-weight: 600;
    color: var(--forest);
  }}
  .triage-list {{
    display: flex;
    flex-direction: column;
    gap: 9px;
  }}
  .triage-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    padding: 13px 16px;
    border-radius: var(--radius-lg);
  }}
  @media (max-width: 640px) {{
    .triage-row {{ flex-direction: column; align-items: flex-start; }}
  }}
  .tr-green {{ background: var(--surface); border: 1px solid var(--outline-variant); }}
  .tr-amber {{ background: #FFFBEB; border: 1px solid #F0E2C0; }}
  .tr-red {{ background: #FFEBEE; border: 1px solid #FFCDD2; }}
  .tr-left {{
    display: flex;
    align-items: flex-start;
    gap: 11px;
    min-width: 0;
  }}
  .tr-dot {{
    width: 11px;
    height: 11px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
  }}
  .dot-green {{ background: var(--success); }}
  .dot-amber {{ background: var(--amber); }}
  .dot-red {{ background: var(--danger); }}
  .tr-name {{
    font-family: var(--font-headline);
    font-size: 16px;
    font-weight: 700;
    color: var(--forest);
    margin: 0 0 2px 0;
  }}
  .tr-note {{ font-size: 12.5px; color: var(--on-surface-variant); display: block; }}
  .tr-reason {{ font-size: 12.5px; font-weight: 600; margin-top: 3px; display: block; }}
  .tr-red .tr-reason {{ color: var(--danger); }}
  .tr-amber .tr-reason {{ color: var(--amber-deep); }}
  .tr-pill {{
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
    flex-shrink: 0;
  }}

  /* =========================================================
     9. 5 BATTLE-TESTED INDUSTRY PATTERNS
     ========================================================= */
  .patterns-stack {{
    display: flex;
    flex-direction: column;
    gap: 14px;
  }}
  .pat-card {{
    padding: 22px 24px;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-xs);
    transition: box-shadow 0.16s ease;
  }}
  .pat-card:hover {{ box-shadow: var(--shadow-md); }}
  .pat-head {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin-bottom: 10px;
  }}
  .pat-title-wrap {{
    display: flex;
    align-items: center;
    gap: 10px;
  }}
  .pat-num {{
    width: 28px;
    height: 28px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-headline);
    font-size: 12.5px;
    font-weight: 700;
    flex-shrink: 0;
  }}
  .pn-coral {{ background: linear-gradient(135deg, var(--coral), var(--coral-bright)); color: #FFFFFF; }}
  .pn-amber {{ background: linear-gradient(135deg, var(--amber), #F39C12); color: #FFFFFF; }}
  .pn-plum {{ background: linear-gradient(135deg, var(--plum), #6C3483); color: #FFFFFF; }}
  .pn-forest {{ background: linear-gradient(135deg, var(--forest), #2D453C); color: var(--amber); }}

  .pat-h3 {{
    font-family: var(--font-headline);
    font-size: 19px;
    font-weight: 700;
    color: var(--forest);
    margin: 0;
  }}
  .pat-links {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }}
  .pat-co-badge {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none;
  }}
  .pat-co-badge:hover {{ filter: brightness(0.97); text-decoration: underline; }}
  .pat-body {{
    font-size: 14px;
    color: var(--on-surface-variant);
    margin: 0 0 12px 0;
    line-height: 1.56;
  }}
  .pat-body code {{
    font-family: var(--font-code);
    font-size: 12.5px;
    color: var(--coral);
    background: var(--surface);
    border: 1px solid #F5D5C5;
    padding: 1px 6px;
    border-radius: 4px;
  }}
  .pat-roi-bar {{
    padding: 10px 14px;
    border-radius: var(--radius);
    background: linear-gradient(90deg, #FFFFFF, #FAF6F0);
    border: 1px solid var(--outline-variant);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 13px;
  }}
  .pat-surface {{
    font-family: var(--font-code);
    font-size: 12px;
    font-weight: 600;
  }}

  /* =========================================================
     10. 2x2 WORKLOAD ROUTER
     ========================================================= */
  .quad-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
    margin-bottom: 18px;
  }}
  @media (max-width: 680px) {{ .quad-grid {{ grid-template-columns: 1fr; }} }}
  .quad-btn {{
    padding: 18px 20px;
    border-radius: var(--radius-lg);
    border: 1px solid var(--outline-variant);
    background: linear-gradient(135deg, #FFFFFF, var(--surface));
    text-align: left;
    cursor: pointer;
    transition: all 0.15s ease;
  }}
  .quad-btn:hover {{ border-color: var(--outline); box-shadow: var(--shadow-xs); }}
  .quad-btn.active {{
    border: 2px solid var(--coral);
    background: linear-gradient(135deg, #FFF5ED 0%, #FFF8F2 55%, #FFECE0 100%);
    box-shadow: var(--shadow-xs);
  }}
  .quad-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
  }}
  .quad-tag {{ font-family: var(--font-code); font-size: 12px; font-weight: 700; }}
  .quad-title {{
    font-family: var(--font-headline);
    font-size: 18px;
    font-weight: 700;
    color: var(--forest);
    margin: 0 0 4px 0;
  }}
  .quad-sub {{ font-size: 13px; color: var(--on-surface-variant); margin: 0; }}

  .quad-detail {{
    padding: 20px 22px;
    border-radius: var(--radius-lg);
    background: linear-gradient(135deg, #FFFFFF 0%, #FCFAF8 55%, #FFF5ED 100%);
    border: 1px solid #F0E4D5;
    box-shadow: var(--shadow-xs);
  }}
  .qd-head {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 10px;
  }}
  .qd-title {{
    font-family: var(--font-headline);
    font-size: 18.5px;
    font-weight: 700;
    color: var(--coral);
    margin: 0;
  }}
  .qd-desc {{ font-size: 13.5px; color: var(--on-surface); margin: 0 0 12px 0; }}
  .qd-stack-box {{
    padding: 12px 14px;
    border-radius: var(--radius);
    background: #FFFFFF;
    border: 1px solid var(--outline-variant);
    margin-bottom: 12px;
  }}
  .qd-stack-lbl {{ display: block; font-size: 12px; font-weight: 700; color: var(--on-surface); margin-bottom: 3px; }}
  .qd-stack-code {{ font-family: var(--font-code); font-size: 12.5px; color: var(--coral); font-weight: 600; }}
  .qd-foot {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 12.5px;
    color: var(--on-surface-variant);
  }}
  .qd-cta {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 13.5px;
    font-weight: 700;
    color: var(--coral);
  }}

  /* =========================================================
     11. DEEP-DIVE WHITEPAPER CHAPTERS, TABLES & INFOGRAPHICS
     ========================================================= */
  .playbook-paper {{
    background: #FFFFFF;
    border: 1px solid var(--outline-variant);
    border-radius: var(--radius-xl);
    padding: clamp(22px, 3.4vw, 38px);
    box-shadow: var(--shadow-sm);
  }}
  .wp-h2 {{
    font-family: var(--font-headline);
    font-size: 24px;
    line-height: 1.28;
    font-weight: 700;
    color: var(--forest);
    margin: 34px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--outline-variant);
  }}
  .playbook-paper .wp-h2:first-of-type {{ margin-top: 6px; }}
  .wp-h3 {{
    font-family: var(--font-headline);
    font-size: 18.5px;
    font-weight: 700;
    color: var(--coral);
    margin: 24px 0 10px 0;
  }}
  .wp-p {{ margin: 0 0 14px 0; font-size: 15px; line-height: 1.66; color: #38332D; }}
  .wp-list {{ margin: 0 0 16px 0; padding-left: 22px; color: #38332D; line-height: 1.62; }}
  .wp-list li {{ margin-bottom: 8px; }}
  .playbook-paper code {{
    font-family: var(--font-code);
    font-size: 12.5px;
    background: var(--surface);
    color: var(--forest);
    border: 1px solid var(--outline-variant);
    padding: 1px 6px;
    border-radius: 4px;
  }}
  .wp-table-wrap {{
    margin: 16px 0 22px;
    overflow-x: auto;
    border: 1px solid var(--outline-variant);
    border-radius: var(--radius-md);
  }}
  .wp-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    line-height: 1.5;
    background: #FFFFFF;
  }}
  .wp-table th {{
    background: #FAF6F0;
    color: var(--forest);
    font-weight: 700;
    text-align: left;
    padding: 10px 14px;
    border-bottom: 1px solid var(--outline);
  }}
  .wp-table td {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--outline-variant);
    vertical-align: top;
    color: #38332D;
  }}
  .wp-table tr:last-child td {{ border-bottom: none; }}
  .wp-figure {{
    margin: 20px 0 24px;
    padding: 14px;
    border-radius: var(--radius-lg);
    background: var(--surface);
    border: 1px solid var(--outline-variant);
  }}
  .wp-figure img {{
    width: 100%;
    height: auto;
    display: block;
    border-radius: var(--radius);
    border: 1px solid var(--outline-variant);
  }}
  .wp-figure figcaption {{
    margin-top: 9px;
    text-align: center;
    font-size: 12.5px;
    font-weight: 600;
    color: var(--on-surface-variant);
  }}
  .wp-callout {{
    background: linear-gradient(90deg, #FFF8E7 0%, #FFFDF8 100%);
    border: 1px solid #F0E2C0;
    border-left: 4px solid var(--amber);
    border-radius: var(--radius);
    padding: 14px 18px;
    margin: 16px 0 20px;
    font-size: 14px;
  }}
  .wp-callout p {{ margin: 0 0 6px 0; }}
  .wp-callout p:last-child {{ margin-bottom: 0; }}
  .wp-tool-jump {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 12px 16px;
    margin: 14px 0 22px;
    border-radius: var(--radius-md);
    background: var(--surface-highlight);
    border: 1px solid #F5D5C5;
    font-size: 13px;
    color: var(--forest);
  }}
  .wp-jump-btn {{
    padding: 6px 12px;
    border-radius: 6px;
    background: var(--coral);
    color: #FFFFFF;
    font-size: 12px;
    font-weight: 700;
    text-decoration: none;
    white-space: nowrap;
  }}
  .wp-jump-btn:hover {{ background: var(--forest); color: #FFFFFF; text-decoration: none; }}

  .wp-refs {{
    margin-top: 30px;
    border: 1px solid var(--outline-variant);
    border-radius: var(--radius-lg);
    background: var(--surface);
    padding: 14px 18px;
  }}
  .wp-refs summary {{
    font-family: var(--font-headline);
    font-size: 17px;
    font-weight: 700;
    color: var(--forest);
    cursor: pointer;
  }}
  .wp-refs-body {{
    margin-top: 12px;
    font-size: 13px;
  }}
  .wp-refs-body .wp-h3 {{ font-size: 15px; margin-top: 8px; }}

  /* =========================================================
     12. 7-PART CODE & VIDEO SERIES BANNER + MODULE CARDS
     ========================================================= */
  .series-hero {{
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, #16221D 0%, #1E2E28 55%, #2B3D35 100%);
    color: #FFFFFF;
    border-radius: var(--radius-xl);
    padding: clamp(24px, 3.2vw, 36px);
    box-shadow: var(--shadow-md);
    margin-bottom: 20px;
  }}
  .series-orb {{
    position: absolute;
    top: -64px;
    right: -64px;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(217, 130, 43, 0.30) 0%, rgba(200, 80, 40, 0.18) 50%, transparent 72%);
    pointer-events: none;
  }}
  .series-hero-inner {{
    position: relative;
    z-index: 1;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
  }}
  .series-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 999px;
    background: rgba(217, 130, 43, 0.22);
    border: 1px solid rgba(217, 130, 43, 0.45);
    color: #F7B963;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 10px;
  }}
  .series-h2 {{
    font-family: var(--font-headline);
    font-size: clamp(24px, 2.6vw, 30px);
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 8px 0;
  }}
  .series-lead {{
    margin: 0;
    max-width: 620px;
    font-size: 14.5px;
    color: #DCE4DF;
    line-height: 1.56;
  }}
  .btn-amber-gold {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 11px 20px;
    border-radius: var(--radius);
    background: linear-gradient(90deg, var(--amber), #F39C12);
    color: var(--forest-deep);
    font-size: 14px;
    font-weight: 700;
    text-decoration: none;
    box-shadow: var(--shadow-xs);
    white-space: nowrap;
  }}
  .btn-amber-gold:hover {{ filter: brightness(1.06); text-decoration: none; }}

  .series-cards-grid {{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
  }}
  @media (max-width: 740px) {{ .series-cards-grid {{ grid-template-columns: 1fr; }} }}
  .sc-card {{
    background: #FFFFFF;
    border: 1px solid var(--outline-variant);
    border-radius: var(--radius-lg);
    padding: 18px 20px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: var(--shadow-xs);
  }}
  .sc-card.sc-live {{
    background: linear-gradient(135deg, #FFFFFF 0%, #FFF8F2 100%);
    border-color: #F5D5C5;
  }}
  .sc-date {{
    font-family: var(--font-code);
    font-size: 11.5px;
    font-weight: 700;
    text-transform: uppercase;
    color: var(--amber-deep);
  }}
  .sc-card.sc-live .sc-date {{ color: var(--coral); }}
  .sc-title {{
    font-family: var(--font-headline);
    font-size: 17.5px;
    line-height: 1.3;
    font-weight: 700;
    color: var(--forest);
    margin: 6px 0 8px 0;
  }}
  .sc-stack {{
    font-family: var(--font-code);
    font-size: 11.5px;
    background: var(--surface);
    border: 1px solid var(--outline-variant);
    padding: 5px 9px;
    border-radius: 6px;
    color: var(--forest);
    margin-bottom: 9px;
  }}
  .sc-desc {{ font-size: 13px; color: var(--on-surface-variant); margin: 0 0 12px 0; }}
  .sc-foot {{
    padding-top: 10px;
    border-top: 1px solid var(--outline-variant);
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    font-size: 12px;
  }}
  .sc-btn-play {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 11px;
    border-radius: 6px;
    background: var(--coral);
    color: #FFFFFF;
    border: none;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
  }}
  .sc-btn-play:hover {{ background: var(--forest); }}

  /* =========================================================
     13. FOOTER & PRINT
     ========================================================= */
  .site-footer {{
    padding-top: 28px;
    border-top: 1px solid var(--outline-variant);
    color: var(--on-surface-variant);
    font-size: 13px;
  }}
  .footer-top {{
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 12px;
  }}
  .footer-brand {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-headline);
    font-size: 15px;
    font-weight: 700;
    color: var(--forest);
  }}
  .footer-mini-ow {{
    width: 24px;
    height: 24px;
    border-radius: 5px;
    background: var(--forest);
    color: var(--amber);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: 700;
  }}
  .footer-links {{
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    font-size: 12.5px;
    font-weight: 600;
  }}
  .footer-disclaimer {{
    margin: 0;
    max-width: 900px;
    line-height: 1.55;
  }}

  @media print {{
    .site-header, .mobile-jump-bar, .left-rail, .video-card {{ display: none !important; }}
    .page-shell {{ display: block; padding: 0; }}
    body {{ background: #FFFFFF; }}
    .hero-card, .workbench-card, .playbook-paper {{ box-shadow: none; border-color: #CCC; }}
  }}
</style>
</head>
<body id="top">

<!-- STICKY TOP NAVIGATION BAR -->
<header class="site-header">
  <div class="top-gradient-bar"></div>
  <div class="header-inner">
    <a href="#top" class="brand-link" title="Scroll to top">
      <div class="brand-monogram">OW</div>
      <div>
        <div class="brand-title-row">
          <span class="brand-name">open-weights-playbook</span>
          <span class="edition-pill">
            <span class="pulse-dot"></span>
            Living Playbook · Nov 2026
          </span>
        </div>
        <p class="brand-sub">Enterprise Architect&#39;s Production &amp; FinOps Journal</p>
      </div>
    </a>

    <nav class="toolkit-dock" aria-label="Quick Jump Toolkit">
      <a href="#quick-calculators" class="dock-tab"><span class="c-coral">{SVG_CALC}</span><span>FinOps TCO</span></a>
      <a href="#license-filter" class="dock-tab"><span class="c-success">{SVG_SHIELD}</span><span>License Triage</span></a>
      <a href="#models-matrix" class="dock-tab"><span class="c-plum">{SVG_CUBE}</span><span>11 Models</span></a>
      <a href="#workload-router" class="dock-tab"><span class="c-amber">{SVG_ROUTE}</span><span>Workload Router</span></a>
      <a href="#full-playbook" class="dock-tab"><span class="c-forest">{SVG_BOOK}</span><span>Full Playbook</span></a>
    </nav>

    <div class="header-actions">
      <a href="https://github.com/kanchpat/open-weight-models" target="_blank" rel="noopener noreferrer" class="btn-gh">
        {SVG_GITHUB}
        <span class="gh-lbl">GitHub</span>
        {SVG_EXT}
      </a>
      <a href="#series-overview" class="btn-dispatch">
        <span>7-Part Dispatch</span>
        {SVG_ARROW}
      </a>
    </div>
  </div>
</header>

<!-- UNOFFICIAL PRACTITIONER BANNER (Warm Parchment Edition) -->
<aside class="unofficial-banner" role="note" aria-label="Unofficial Practitioner Guide Disclaimer">
  <div class="unofficial-inner">
    <span class="unofficial-strong">{SVG_SHIELD} Unofficial Google Cloud Practitioner Guide</span>
    <span>· Authored by <strong>Kanchana Patlolla</strong> &amp; <strong>Anusha Sabbineni</strong>, with guidance from <strong>Alan Blount</strong>. Views are independent practitioner research — not an official Google product.</span>
  </div>
</aside>

<!-- COMPACT MOBILE/TABLET JUMP STRIP -->
<nav class="mobile-jump-bar" aria-label="Mobile Quick Navigation">
  <a href="#video-briefing">▶ 5-Min Video</a>
  <a href="#quick-calculators">⚡ FinOps TCO</a>
  <a href="#models-matrix">11 Models</a>
  <a href="#license-filter">⚡ License Triage</a>
  <a href="#industry-patterns">5 Patterns</a>
  <a href="#workload-router">2×2 Router</a>
  <a href="#full-playbook">Full Playbook</a>
  <a href="#series-overview">7-Part Series</a>
</nav>

<!-- MAIN 12-COLUMN CONTAINER -->
<div class="page-shell">

  <!-- LEFT STICKY SIDEBAR: TOC, 7-PART ROADMAP & AUTHORS -->
  <aside class="left-rail" aria-label="Playbook Navigation">
    <div class="rail-card">
      <div class="rail-head">
        <span class="rail-eyebrow">Playbook Chapters</span>
        <span class="rail-ver">v2026.11</span>
      </div>
      <nav class="toc-nav" id="sidebar-toc">
        <a href="#hero-shift" class="toc-item active" data-spy="hero-shift"><span class="toc-dot"></span><span>The 56% / 14% Paradigm</span></a>
        <a href="#video-briefing" class="toc-item" data-spy="video-briefing"><span class="toc-dot"></span><span>5-Min Video Briefing</span></a>
        <a href="#five-questions" class="toc-item" data-spy="five-questions"><span class="toc-dot"></span><span>5 Architect Inquiries</span></a>
        <a href="#quick-calculators" class="toc-item" data-spy="quick-calculators"><span class="toc-dot"></span><span>FinOps 73% Duty Rule</span></a>
        <a href="#models-matrix" class="toc-item" data-spy="models-matrix"><span class="toc-dot"></span><span>11 Frontier Checkpoints</span></a>
        <a href="#license-filter" class="toc-item" data-spy="license-filter"><span class="toc-dot"></span><span>Interactive License Triage</span></a>
        <a href="#industry-patterns" class="toc-item" data-spy="industry-patterns"><span class="toc-dot"></span><span>5 Industry Patterns</span></a>
        <a href="#workload-router" class="toc-item" data-spy="workload-router"><span class="toc-dot"></span><span>2×2 Workload Router</span></a>
        <a href="#full-playbook" class="toc-item" data-spy="full-playbook"><span class="toc-dot"></span><span>Deep-Dive Playbook (§1–§8)</span></a>
        <a href="#series-overview" class="toc-item" data-spy="series-overview"><span class="toc-dot"></span><span>7-Part Code Dispatches</span></a>
      </nav>
    </div>

    <div class="rail-card">
      <div class="dispatch-title-row">
        {SVG_BOOK}
        <span>Architectural Dispatches</span>
      </div>
      <p class="dispatch-sub">Friday code blueprints, notebooks &amp; Dockerfiles on Vertex AI and Cloud Run.</p>
      <ul class="dispatch-list">
        <li><a href="#series-part-1" class="dispatch-link live"><span class="dispatch-num">01</span><span><span class="dispatch-name">Architect&#39;s Playbook &amp; Video</span><span class="dispatch-date">Nov 6 · Live Now</span></span></a></li>
        <li><a href="#series-part-2" class="dispatch-link"><span class="dispatch-num">02</span><span><span class="dispatch-name">Vertex AI OpenMaaS $0 Idle</span><span class="dispatch-date">Nov 13, 2026</span></span></a></li>
        <li><a href="#series-part-3" class="dispatch-link"><span class="dispatch-num">03</span><span><span class="dispatch-name">Google ADK &amp; System 1 Gates</span><span class="dispatch-date">Nov 13, 2026</span></span></a></li>
        <li><a href="#series-part-4" class="dispatch-link"><span class="dispatch-num">04</span><span><span class="dispatch-name">Cloud Run Scale-to-Zero vLLM</span><span class="dispatch-date">Nov 20, 2026</span></span></a></li>
        <li><a href="#series-part-5" class="dispatch-link"><span class="dispatch-num">05</span><span><span class="dispatch-name">Sovereign In-VPC Runtime</span><span class="dispatch-date">Nov 20, 2026</span></span></a></li>
        <li><a href="#series-part-6" class="dispatch-link"><span class="dispatch-num">06</span><span><span class="dispatch-name">LoRA &amp; &lt;$100 GRPO RL</span><span class="dispatch-date">Dec 4, 2026</span></span></a></li>
        <li><a href="#series-part-7" class="dispatch-link"><span class="dispatch-num">07</span><span><span class="dispatch-name">Frontier-to-Open Distillation</span><span class="dispatch-date">Dec 11 · Wrap Dec 18</span></span></a></li>
      </ul>
    </div>

    <div class="rail-card">
      <span class="rail-eyebrow">Editorial Contributors</span>
      <div class="author-list">
        <div class="author-row"><span class="avatar-badge av-kp">KP</span><span>Kanchana Patlolla</span></div>
        <div class="author-row"><span class="avatar-badge av-as">AS</span><span>Anusha Sabbineni</span></div>
        <div class="author-row guidance"><span class="avatar-badge av-ab">AB</span><span>Guidance: Alan Blount</span></div>
      </div>
    </div>
  </aside>

  <!-- RIGHT MAIN CONTENT WORKBENCH -->
  <main class="main-col">

    <!-- HERO SECTION: THE 56% / 14% PARADIGM -->
    <section id="hero-shift" class="hero-card">
      <div class="hero-orb-tr"></div>
      <div class="hero-orb-bl"></div>
      <div class="hero-content">
        <div class="hero-eyebrow">
          {SVG_SPARKLE}
          <span>Vercel AI Gateway Index &amp; Stanford HAI 2026</span>
        </div>
        <h1 class="hero-h1">Enterprise Architect&#39;s Guide to Open-Weight AI Models on Google Cloud</h1>
        <p class="hero-lead">
          Open-weight models now process <span class="hl-forest">56% of enterprise gateway token volume</span> at only <span class="hl-coral">14% of total spend</span>. Before provisioning dedicated GPU clusters or downloading weights, use this practitioner playbook to evaluate licenses, FinOps break-evens, and production deployment patterns.
        </p>

        <div class="stat-strip">
          <div class="stat-cell s-coral">
            <span class="stat-num tabular">56%</span>
            <span class="stat-lbl">Gateway Token Share</span>
          </div>
          <div class="stat-cell s-success">
            <span class="stat-num tabular">14%</span>
            <span class="stat-lbl">Inference Spend Share</span>
          </div>
          <div class="stat-cell s-amber">
            <span class="stat-num tabular">73%</span>
            <span class="stat-lbl">GPU Duty Break-Even</span>
          </div>
          <div class="stat-cell s-plum">
            <span class="stat-num tabular">35×</span>
            <span class="stat-lbl">System 1 Speedup</span>
          </div>
        </div>

        <div class="hero-ctas">
          <a href="#quick-calculators" class="btn-primary-coral">
            {SVG_CALC}
            <span>Open FinOps Calculator</span>
          </a>
          <a href="#models-matrix" class="btn-secondary-warm">
            {SVG_TUNE}
            <span>Filter 11 Models</span>
          </a>
          <button type="button" class="btn-video-ghost" id="hero-video-btn">
            {SVG_PLAY}
            <span>Watch 5-Min Video Tour (5:01)</span>
          </button>
        </div>
      </div>
    </section>

    <!-- 5-MINUTE NARRATED EXECUTIVE VIDEO TOUR -->
    <section id="video-briefing" class="video-card" aria-label="5-Minute Executive Explainer Video">
      <div class="yt-stage" id="yt-player-stage">
        <button type="button" class="yt-poster-btn" id="yt-poster-trigger" aria-label="Play 5-Minute Open-Weight AI Playbook Overview Video">
          <img src="{YT_THUMB_B64}" alt="Open-Weight AI Playbook 5-Minute Explainer Thumbnail">
          <span class="yt-play-circle" aria-hidden="true">
            <svg viewBox="0 0 24 24"><polygon points="6,4 20,12 6,20"></polygon></svg>
          </span>
          <span class="yt-dur-pill">▶ 05:01</span>
        </button>
      </div>
    </section>

    <!-- 01 · ARCHITECTURAL STRATEGY: 5 QUESTIONS -->
    <section id="five-questions">
      <div class="sec-header">
        <div>
          <span class="sec-eyebrow">01 · ARCHITECTURAL STRATEGY</span>
          <h2 class="sec-h2">5 Questions Every Architect Faces</h2>
        </div>
        <p class="sec-sub">Click any domain card to jump directly to its production blueprint or interactive calculator.</p>
      </div>

      <div class="q-bento-grid">
        <a href="#license-filter" class="q-bento-card qc-coral">
          <div>
            <div class="q-top-row">
              <span class="q-code" style="color:var(--coral);">01 · LICENSING</span>
              <span class="q-pill pill-green">Tier 1–4</span>
            </div>
            <h3 class="q-title">Which open-weight license is safe?</h3>
            <p class="q-desc">Distinguish true Apache 2.0/MIT from custom commercial cliffs ($10B valuation caps, 700M MAU rules, CC BY-NC LoRAs).</p>
          </div>
          <div class="q-foot" style="color:var(--coral);"><span>⚡ Try License Filter</span>{SVG_ARROW}</div>
        </a>

        <a href="#harness-strategy" class="q-bento-card qc-forest">
          <div>
            <div class="q-top-row">
              <span class="q-code" style="color:var(--forest);">02 · HARNESS</span>
              <span class="q-pill pill-amber">+16.7pp Lift</span>
            </div>
            <h3 class="q-title">Train weights or evolve the harness?</h3>
            <p class="q-desc">Harvey&#39;s legal benchmark showed evolving the surrounding harness beats weight retraining (+16.7pp accuracy, -64% cost).</p>
          </div>
          <div class="q-foot" style="color:var(--forest);"><span>Google ADK Blueprint</span>{SVG_ARROW}</div>
        </a>

        <a href="#security-mitigations" class="q-bento-card qc-amber">
          <div>
            <div class="q-top-row">
              <span class="q-code" style="color:var(--amber-deep);">03 · SECURITY</span>
              <span class="q-pill pill-amber">SHA-256 Pin</span>
            </div>
            <h3 class="q-title">How do we lock down VPC &amp; weights?</h3>
            <p class="q-desc">$1,200 weight abliteration attacks, assistant prefill bypasses, and in-VPC isolation with Google Cloud Model Armor.</p>
          </div>
          <div class="q-foot" style="color:var(--amber-deep);"><span>7 Risk Watch-Outs</span>{SVG_ARROW}</div>
        </a>

        <a href="#industry-patterns" class="q-bento-card qc-plum">
          <div>
            <div class="q-top-row">
              <span class="q-code" style="color:var(--plum);">04 · PATTERNS</span>
              <span class="q-pill pill-plum">5 Patterns</span>
            </div>
            <h3 class="q-title">Who is running this in production?</h3>
            <p class="q-desc">Netflix GenRec (prefill ranker), Pinterest (vision graft), Harvey, DoorDash (distillation), and Coinbase/Uber (&lt;$100 GRPO RL).</p>
          </div>
          <div class="q-foot" style="color:var(--plum);"><span>Explore Field Architectures</span>{SVG_ARROW}</div>
        </a>

        <a href="#quick-calculators" class="q-bento-card qc-finops q-card-span2">
          <div>
            <div class="q-top-row">
              <span class="q-code" style="color:var(--forest);">05 · FINOPS &amp; HARDWARE</span>
              <span class="q-pill pill-green">73% Duty Rule</span>
            </div>
            <h3 class="q-title">Serverless OpenMaaS or dedicated self-hosted GPUs?</h3>
            <p class="q-desc">Why dedicated 24/7 GPU endpoints cost 1.42× more than serverless PayGo below 73% hardware utilization — and how to stay at $0 idle GPU burn with Vertex AI OpenMaaS and Cloud Run scale-to-zero GPUs.</p>
          </div>
          <div class="q-foot" style="color:var(--forest);"><span>⚡ Run Break-Even FinOps Calculator</span>{SVG_ARROW}</div>
        </a>
      </div>
    </section>

    <!-- INTERACTIVE FINOPS TCO CALCULATOR (§6.1) -->
    <section id="quick-calculators" class="workbench-card">
      <div class="wb-head">
        <div class="wb-top-row">
          <span class="wb-badge">⚡ Interactive FinOps Tool · Section 6.1</span>
          <span class="wb-meta">Benchmark: Gemma 4 26B-A4B · 8M–30M/day &amp; 73% Duty Thresholds</span>
        </div>
        <h2 class="sec-h2">OpenMaaS vs. Dedicated GPU Break-Even Calculator</h2>
        <p class="wb-desc">Adjust daily output token volume and dedicated GPU cluster duty cycle to model monthly spend and locate your hardware break-even point.</p>
      </div>

      <div class="sliders-panel">
        <div>
          <div class="slider-head">
            <label for="token-slider">Daily Output Token Volume</label>
            <span id="token-val-display" class="slider-val-coral tabular">25M tokens/day (750M/mo)</span>
          </div>
          <input id="token-slider" type="range" min="1" max="150" value="25" class="range-coral">
          <div class="slider-ticks">
            <span>1M/day (Pilot)</span>
            <span style="color:var(--coral);font-weight:700;">8M–30M (Break-Even)</span>
            <span>150M/day (Fleet)</span>
          </div>
        </div>

        <div>
          <div class="slider-head">
            <label for="duty-slider">Dedicated GPU Duty-Cycle Utilization</label>
            <span id="duty-val-display" class="slider-val-amber tabular">35% Duty Cycle</span>
          </div>
          <input id="duty-slider" type="range" min="10" max="95" value="35" class="range-amber">
          <div class="slider-ticks">
            <span>15% (Spiky)</span>
            <span>50% (Business)</span>
            <span style="color:var(--success);font-weight:700;">73% (Break-Even)</span>
            <span>95% (Batch)</span>
          </div>
        </div>
      </div>

      <div class="finops-cards">
        <div class="f-card fc-closed">
          <span class="f-lbl" style="color:var(--on-surface-variant);">Closed Frontier API</span>
          <span class="f-rate" style="color:var(--on-surface-variant);">$10.00 / 1M tokens</span>
          <div id="cost-closed" class="f-price tabular" style="color:var(--on-surface);">$7,500/mo</div>
          <div class="f-bar-track"><div id="bar-closed" class="f-bar-fill" style="width:100%;background:#7C746A;"></div></div>
          <span class="f-note" style="color:var(--on-surface-variant);">Baseline Proprietary API</span>
        </div>

        <div class="f-card fc-maas">
          <span class="f-lbl" style="color:var(--coral);">Vertex AI OpenMaaS PayGo</span>
          <span class="f-rate" style="color:var(--coral);">$0.907 / 1M tokens ($0 idle)</span>
          <div id="cost-openmaas" class="f-price tabular" style="color:var(--coral);">$680/mo</div>
          <div class="f-bar-track"><div id="bar-maas" class="f-bar-fill" style="width:9%;background:var(--coral);"></div></div>
          <span id="note-openmaas" class="f-note" style="color:var(--success);">91% savings vs closed</span>
        </div>

        <div class="f-card fc-ded">
          <span class="f-lbl" style="color:var(--amber-deep);">Dedicated 24/7 Self-Host</span>
          <span id="cost-dedicated-rate" class="f-rate" style="color:var(--amber-deep);">$1.89 / 1M effective</span>
          <div id="cost-dedicated" class="f-price tabular" style="color:#4A3B18;">$1,419/mo</div>
          <div class="f-bar-track"><div id="bar-ded" class="f-bar-fill" style="width:19%;background:var(--amber);"></div></div>
          <span id="cost-dedicated-note" class="f-note" style="color:var(--danger);">2.08× pricier than OpenMaaS</span>
        </div>

        <div class="f-card fc-sys1">
          <span class="f-lbl" style="color:var(--success);">System 1 Single-Pass</span>
          <span class="f-rate" style="color:var(--success);">output_tokens: 0</span>
          <div id="cost-system1" class="f-price tabular" style="color:var(--success);">$45/mo</div>
          <div class="f-bar-track"><div id="bar-sys1" class="f-bar-fill" style="width:3%;background:var(--success);"></div></div>
          <span class="f-note" style="color:var(--success);">35× faster triage &amp; gates</span>
        </div>
      </div>

      <div id="verdict-banner" class="verdict-box verdict-coral">
        <span id="verdict-icon-info">{SVG_INFO}</span>
        <span id="verdict-icon-check" style="display:none;">{SVG_CHECK}</span>
        <div>
          <span id="verdict-title" class="verdict-title">FinOps Verdict: Below 73% Duty Cycle — Start Serverless</span>
          <p id="verdict-text" class="verdict-body"></p>
        </div>
      </div>
    </section>

    <!-- 02 · MODEL CATALOG: 11 OPEN-WEIGHT MODELS -->
    <section id="models-matrix">
      <div class="sec-header">
        <div>
          <span class="sec-eyebrow">02 · MODEL CATALOG</span>
          <h2 class="sec-h2">11 Open-Weight Models Covered</h2>
          <p class="sec-sub">Filter by commercial license posture, pre-training provenance tier, or Google Cloud runtime surface.</p>
        </div>
      </div>

      <div class="filter-bar" id="model-filter-bar">
        <button type="button" class="model-filter-btn active" data-filter="all">All Models (11)</button>
        <button type="button" class="model-filter-btn" data-filter="permissive">🟢 Unrestricted Apache 2.0 / MIT</button>
        <button type="button" class="model-filter-btn" data-filter="gcp">☁️ Vertex AI &amp; Cloud Run</button>
        <button type="button" class="model-filter-btn" data-filter="tier4">🔍 Tier 4 Auditable Data Lineage</button>
        <button type="button" class="model-filter-btn" data-filter="system1">⚡ System 1 Single-Pass (tokens: 0)</button>
        <button type="button" class="model-filter-btn" data-filter="capped">⚠️ Commercial / Valuation Caps</button>
      </div>

      <div class="models-grid" id="models-container">
        <article class="model-card mc-coral" data-category="permissive gcp">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">Google Gemma 4</h3>
              <span class="mc-lic pill-green">Apache 2.0</span>
            </div>
            <div class="mc-arch">31B Dense · MoE 26B-A4B · Edge E4B · MedGemma QAT</div>
            <p class="mc-body">Zero tool-calling drift under FP4/INT4 Quantization-Aware Training. Prime teacher-student distillation target (&lt;150 ms TTFT).</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ Vertex OpenMaaS · Cloud Run</span>
            <a href="https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/open-models/use-gemma" target="_blank" rel="noopener noreferrer" class="mc-link" style="color:var(--coral);">Docs ↗</a>
          </div>
        </article>

        <article class="model-card mc-green" data-category="permissive gcp tier4">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">Ai2 Olmo 3 &amp; Tülu 3</h3>
              <span class="mc-lic pill-green">OpenMDW</span>
            </div>
            <div class="mc-arch">32B Dense · Full Dolma 3 Corpus + RLVR Code</div>
            <p class="mc-body">Gold-standard EU AI Act &amp; copyright auditability with line-by-line pre-training data lineage and open filtering recipes.</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ Model Garden · Agent VPC</span>
            <a href="https://arxiv.org/abs/2512.13961" target="_blank" rel="noopener noreferrer" class="mc-link" style="color:var(--success);">arXiv ↗</a>
          </div>
        </article>

        <article class="model-card mc-amber" data-category="permissive gcp">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">DeepSeek-V4.1-Flash</h3>
              <span class="mc-lic pill-green">MIT</span>
            </div>
            <div class="mc-arch">763B Total / 8B–16B Active MoE · CSA2</div>
            <p class="mc-body">437× KV-cache compression (10 MB @ 128K context); 76× lower coding &amp; math agent token cost ($0.72 vs $55.00).</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ Vertex OpenMaaS · ADK Router</span>
            <a href="https://arxiv.org/pdf/2609.19969" target="_blank" rel="noopener noreferrer" class="mc-link" style="color:var(--amber-deep);">Paper ↗</a>
          </div>
        </article>

        <article class="model-card mc-coral" data-category="permissive gcp">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">Alibaba Qwen 3.8</h3>
              <span class="mc-lic pill-green">Apache 2.0</span>
            </div>
            <div class="mc-arch">27B Dense &amp; Flash-Next 180B-A6B MoE</div>
            <p class="mc-body">High-throughput multilingual &amp; coding workhorse. Preferred base for Pinterest-style surgical vision encoder grafting.</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ Vertex OpenMaaS · Cloud Run</span>
            <a href="https://qwen.ai/blog?id=qwen3.8-flash-next" target="_blank" rel="noopener noreferrer" class="mc-link" style="color:var(--coral);">Report ↗</a>
          </div>
        </article>

        <article class="model-card mc-plum" data-category="permissive gcp">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">Mistral Large 4 &amp; Timestral</h3>
              <span class="mc-lic pill-green">Apache 2.0</span>
            </div>
            <div class="mc-arch">1T Total / 52B Active MoE · 380M Series</div>
            <p class="mc-body">93.3% Lakera B3 adversarial safety defense score; Timestral runs zero-shot forecasting at 5,000 series/s (Mod-MIT weights).</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ Model Garden · Cloud Run</span>
            <a href="https://mistral.ai/news/mistral-large-4" target="_blank" rel="noopener noreferrer" class="mc-link" style="color:var(--plum);">Blog ↗</a>
          </div>
        </article>

        <article class="model-card mc-coral" data-category="permissive gcp">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">Reflection AI Beam 1.0</h3>
              <span class="mc-lic pill-green">Apache 2.0</span>
            </div>
            <div class="mc-arch">501B Total / 23B Active Sparse MoE</div>
            <p class="mc-body">US-origin frontier open-weight MoE engineered for multi-step enterprise agentic reasoning and self-reflection.</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ Model Garden · Agent Runtime</span>
            <a href="https://reflection.ai/blog/introducing-beam" target="_blank" rel="noopener noreferrer" class="mc-link" style="color:var(--coral);">Blog ↗</a>
          </div>
        </article>

        <article class="model-card mc-green" data-category="permissive gcp tier4">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">Aleph Alpha Kolibri</h3>
              <span class="mc-lic pill-green">Tier IV Sovereign</span>
            </div>
            <div class="mc-arch">78B Total / 3.5B Active MoE · Merlin-Arthur</div>
            <p class="mc-body">European sovereign Apache 2.0 MoE with cryptographic citation verification and 44% ungrounded abstention.</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ EU Sovereign In-VPC Runtime</span>
            <a href="https://aleph-alpha.com/en/blog/kolibri-has-landed-a-sovereign-open-weight-model/" target="_blank" rel="noopener noreferrer" class="mc-link" style="color:var(--forest);">Blog ↗</a>
          </div>
        </article>

        <article class="model-card mc-plum" data-category="permissive gcp system1">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">System 1 Decision Models</h3>
              <span class="mc-lic pill-green">Apache 2.0</span>
            </div>
            <div class="mc-arch">0.6B–4B Single Forward Pass (tokens: 0)</div>
            <p class="mc-body">dgem, Clef, Clairic &amp; Decision-1: 35× faster (5.8–84 ms p50) and 200× cheaper rubric verification, routing, and triage.</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ ADK Gate · Cloud Run</span>
            <a href="https://blog.cloudflare.com/clef-decision-models/" target="_blank" rel="noopener noreferrer" class="mc-link" style="color:var(--plum);">Blog ↗</a>
          </div>
        </article>

        <article class="model-card mc-amber" data-category="gcp capped">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">Meta Llama 4 (Maverick)</h3>
              <span class="mc-lic pill-amber">700M MAU Cap</span>
            </div>
            <div class="mc-arch">Multimodal Native MoE (17B Active)</div>
            <p class="mc-body">Broad ecosystem compatibility; triggers mandatory commercial license deal above 700M MAU and requires &#39;Llama&#39; naming prefix.</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ Vertex AI Model Garden</span>
            <a href="#2-procurement-licensing-triage" class="mc-link" style="color:var(--amber-deep);">License ↓</a>
          </div>
        </article>

        <article class="model-card mc-amber" data-category="capped">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">Moonshot Kimi K3.1 Pro</h3>
              <span class="mc-lic pill-amber">100M MAU Cap</span>
            </div>
            <div class="mc-arch">1T+ Sparse MoE · Long-Horizon Agent</div>
            <p class="mc-body">Leading deep-research and tool-use benchmarks; commercial deal required above 100M MAU or $20M/mo inference revenue.</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ Self-Hosted vLLM on GKE</span>
            <a href="https://www.kimi.ai/blog/kimi-k3-1-pro" target="_blank" rel="noopener noreferrer" class="mc-link" style="color:var(--amber-deep);">Blog ↗</a>
          </div>
        </article>

        <article class="model-card mc-red" data-category="capped">
          <div>
            <div class="mc-top">
              <h3 class="mc-name">Zhipu GLM-5.3-Flash</h3>
              <span class="mc-lic pill-red">$10B Val Gate</span>
            </div>
            <div class="mc-arch">320B Total / 18B Active MoE</div>
            <p class="mc-body">Fast agentic coding execution, but triggers mandatory commercial &amp; security agreement if corporate valuation &gt;= $10B.</p>
          </div>
          <div class="mc-foot">
            <span class="mc-cloud">☁️ Commercial Gate Required</span>
            <a href="https://huggingface.co/zai-org/GLM-5.3/blob/main/LICENSE" target="_blank" rel="noopener noreferrer" class="mc-link" style="color:var(--danger);">License ↗</a>
          </div>
        </article>
      </div>
    </section>

    <!-- INTERACTIVE LICENSE & DATA AUDITABILITY TRIAGE (§2.1) -->
    <section id="license-filter" class="workbench-card">
      <div class="wb-head">
        <div class="wb-top-row">
          <span class="wb-badge">⚡ Interactive Legal Toolkit · Section 2.1</span>
          <span class="wb-meta">Evaluates 11 Model Cohorts &amp; LoRA Adapters</span>
        </div>
        <h2 class="sec-h2">Open-Weight License &amp; Data Auditability Triage</h2>
        <p class="wb-desc">Simulate enterprise valuation cliffs, MAU product limits, geopolitical origin rules, and training-data auditability requirements.</p>
      </div>

      <div class="triage-controls">
        <div class="triage-field">
          <label for="val-select">Company Valuation</label>
          <select id="val-select" class="triage-select">
            <option value="1">$50M Growth</option>
            <option value="2">$500M Mid-Market</option>
            <option value="3">$2B Late Stage</option>
            <option value="4" selected>$10B Enterprise Gate</option>
            <option value="5">$50B+ Global Fortune 500</option>
          </select>
        </div>

        <div class="triage-field">
          <label for="mau-select">Monthly Active Users</label>
          <select id="mau-select" class="triage-select">
            <option value="1">&lt;1M Users</option>
            <option value="2">10M Users</option>
            <option value="3" selected>50M Users</option>
            <option value="4">100M+ Cap (Kimi / $20M Rev)</option>
            <option value="5">700M+ Cap (Llama 4)</option>
          </select>
        </div>

        <div class="triage-field">
          <label for="region-select">Sovereignty Policy</label>
          <select id="region-select" class="triage-select">
            <option value="1" selected>Global (Any Origin)</option>
            <option value="2">US / EU Regulated Only</option>
            <option value="3">Strict EU Sovereign Air-Gap</option>
          </select>
        </div>

        <div class="triage-field">
          <label for="audit-select">Data Auditability</label>
          <select id="audit-select" class="triage-select">
            <option value="1" selected>Level 1: Weights Only</option>
            <option value="2">Level 2: Weights + Open Recipe</option>
            <option value="3">Level 3: Full Pre-Training Data (Tier 4)</option>
          </select>
        </div>
      </div>

      <div class="triage-summary-bar">
        <span>Informational procurement planning only (not legal advice).</span>
        <span id="triage-tally" class="triage-tally"></span>
      </div>

      <div class="triage-list" id="license-results-list"></div>
    </section>

    <!-- 03 · PRODUCTION PATTERNS: 5 INDUSTRY ARCHITECTURES -->
    <section id="industry-patterns">
      <div class="sec-header">
        <div>
          <span class="sec-eyebrow">03 · PRODUCTION PATTERNS</span>
          <h2 class="sec-h2">5 Battle-Tested Industry Architectures</h2>
          <p class="sec-sub">Production deployments linking directly to engineering blogs from Netflix, Pinterest, Harvey, DoorDash, Coinbase, and Uber.</p>
        </div>
      </div>

      <div class="patterns-stack">
        <article class="pat-card mc-coral">
          <div class="pat-head">
            <div class="pat-title-wrap">
              <span class="pat-num pn-coral">01</span>
              <h3 class="pat-h3">Prefill-Only Catalog Ranker</h3>
            </div>
            <div class="pat-links">
              <a href="https://netflixtechblog.com/genrec-towards-llm-native-recommendation-at-netflix-f20be6f643e3" target="_blank" rel="noopener noreferrer" class="pat-co-badge pill-coral">Netflix (GenRec) ↗</a>
            </div>
          </div>
          <p class="pat-body">
            Autoregressive token decoding is too slow for real-time catalog recommendation across millions of concurrent streams. Verbalize user watch history into prompt text, freeze base weights, and attach a linear catalog scoring head served on vLLM with <code>output_tokens: 0</code>.
          </p>
          <div class="pat-roi-bar">
            <span><strong>Production ROI:</strong> Statistically significant engagement lift across ~10% of global Netflix traffic at sub-second latency.</span>
            <span class="pat-surface" style="color:var(--coral);">☁️ Cloud Run GPUs (vLLM prefill)</span>
          </div>
        </article>

        <article class="pat-card mc-amber">
          <div class="pat-head">
            <div class="pat-title-wrap">
              <span class="pat-num pn-amber">02</span>
              <h3 class="pat-h3">Surgical Vision Encoder Graft</h3>
            </div>
            <div class="pat-links">
              <a href="https://www.youtube.com/watch?v=1C3HLLWtOx0" target="_blank" rel="noopener noreferrer" class="pat-co-badge pill-amber">Pinterest (Visual Commerce) ↗</a>
            </div>
          </div>
          <p class="pat-body">
            Closed multimodal APIs charge high per-image token fees and lack proprietary catalog embeddings. Post-train an open VLM (Qwen3-VL or Gemma 4) by slicing off its generic ViT tower and grafting Pinterest&#39;s pre-computed catalog visual vectors.
          </p>
          <div class="pat-roi-bar">
            <span><strong>Production ROI:</strong> 90% lower inference cost than closed proprietary APIs with higher visual search relevance.</span>
            <span class="pat-surface" style="color:var(--forest);">☁️ Vertex AI Model Garden &amp; GKE</span>
          </div>
        </article>

        <article class="pat-card mc-plum">
          <div class="pat-head">
            <div class="pat-title-wrap">
              <span class="pat-num pn-plum">03</span>
              <h3 class="pat-h3">Matter-Isolated Rubric &amp; Harness Gates</h3>
            </div>
            <div class="pat-links">
              <a href="https://www.harvey.ai/blog/introducing-harveys-legal-agent-benchmark" target="_blank" rel="noopener noreferrer" class="pat-co-badge pill-plum">Harvey (Legal Tech) ↗</a>
            </div>
          </div>
          <p class="pat-body">
            Global law firms demand strict client-matter air-gapping and zero vendor retraining on confidential briefs. Post-train open weights across 75,000+ legal rubric criteria and enforce pre-submission harness verification gates before returning drafts.
          </p>
          <div class="pat-roi-bar">
            <span><strong>Production ROI:</strong> Nearly 2× strict all-pass rate (+16.7pp accuracy from harness evolution alone).</span>
            <span class="pat-surface" style="color:var(--plum);">☁️ Vertex AI Agent Runtime In-VPC</span>
          </div>
        </article>

        <article class="pat-card mc-amber">
          <div class="pat-head">
            <div class="pat-title-wrap">
              <span class="pat-num pn-amber">04</span>
              <h3 class="pat-h3">Teacher-Student SKU Distillation</h3>
            </div>
            <div class="pat-links">
              <a href="https://careersatdoordash.com/blog/unleashing-the-power-of-large-language-models-at-doordash-for-a-seamless-shopping-adventure/" target="_blank" rel="noopener noreferrer" class="pat-co-badge pill-amber">DoorDash (Logistics) ↗</a>
            </div>
          </div>
          <p class="pat-body">
            Classifying millions of retail SKUs and defect photos on frontier APIs is slow and costly. Use Gemini 3.1 Pro as an offline teacher to synthesize verified pairs, then distill into INT4 quantized Gemma 4 LoRA/QLoRA student models on Ray.
          </p>
          <div class="pat-roi-bar">
            <span><strong>Production ROI:</strong> 10× lower serving cost at &lt;150 ms TTFT; training turnaround cut from weeks to days.</span>
            <span class="pat-surface" style="color:var(--amber-deep);">☁️ Vertex Distillation &amp; Cloud Run GPUs</span>
          </div>
        </article>

        <article class="pat-card mc-green">
          <div class="pat-head">
            <div class="pat-title-wrap">
              <span class="pat-num pn-forest">05</span>
              <h3 class="pat-h3">Sub-$100 Verifiable RL &amp; GenAI Gateway</h3>
            </div>
            <div class="pat-links">
              <a href="https://www.coinbase.com/blog/part-one-how-coinbase-built-evaluated-and-post-trained-a-fraud-agent" target="_blank" rel="noopener noreferrer" class="pat-co-badge pill-green">Coinbase ↗</a>
              <a href="https://www.uber.com/us/en/blog/genai-gateway/" target="_blank" rel="noopener noreferrer" class="pat-co-badge pill-green">Uber ↗</a>
            </div>
          </div>
          <p class="pat-body">
            Post-train a 9B open model using single-GPU GRPO (SkyRL) for under $100 against verifiable fraud rubrics (Coinbase), served behind an in-VPC PII-redacting GenAI Gateway processing 16M queries/month (Uber).
          </p>
          <div class="pat-roi-bar">
            <span><strong>Production ROI:</strong> +9.6% F1 over frontier APIs, 55% lower latency, and 30% reduction in live fraud.</span>
            <span class="pat-surface" style="color:var(--success);">☁️ Vertex AI Training &amp; Model Armor</span>
          </div>
        </article>
      </div>
    </section>

    <!-- INTERACTIVE 2x2 WORKLOAD ROUTER (§6.2) -->
    <section id="workload-router" class="workbench-card">
      <div class="wb-head">
        <div class="wb-top-row">
          <span class="wb-badge">⚡ Interactive Router · Section 6.2</span>
          <span class="wb-meta">Velocity / Duty Cycle × Sovereignty / Customization</span>
        </div>
        <h2 class="sec-h2">2×2 Workload Router &amp; Google Cloud Mapper</h2>
        <p class="wb-desc">Click any quadrant below to inspect its production reference stack, customer patterns, and matching hands-on series blueprint.</p>
      </div>

      <div class="quad-grid" id="quadrant-grid">
        <button type="button" class="quad-btn active" data-quadrant="2">
          <div class="quad-top"><span class="quad-tag" style="color:var(--coral);">QUADRANT II · GOVERN &amp; AUDIT</span><span style="color:var(--coral);">{SVG_SHIELD}</span></div>
          <h3 class="quad-title">Sovereign &amp; In-VPC Open Weights</h3>
          <p class="quad-sub">High Sovereignty · Regulated PII/PHI/Legal · Immutable SHA-256 Pinning</p>
        </button>

        <button type="button" class="quad-btn" data-quadrant="1">
          <div class="quad-top"><span class="quad-tag" style="color:var(--forest);">QUADRANT I · OWN THE MOAT</span><span style="color:var(--forest);">{SVG_MEDAL}</span></div>
          <h3 class="quad-title">Post-Trained &amp; Surgically Customized</h3>
          <p class="quad-sub">High Scale + Custom Encoders, Prefill Rankers &amp; &lt;$100 GRPO RL</p>
        </button>

        <button type="button" class="quad-btn" data-quadrant="3">
          <div class="quad-top"><span class="quad-tag" style="color:var(--on-surface-variant);">QUADRANT III · RENT FOR AGILITY</span><span style="color:var(--on-surface-variant);">{SVG_CLOUD}</span></div>
          <h3 class="quad-title">Frontier APIs &amp; Serverless OpenMaaS</h3>
          <p class="quad-sub">Spiky QPS (&lt;73% Duty Cycle) · $0 Idle Burn · Frontier Zero-Shot R&amp;D</p>
        </button>

        <button type="button" class="quad-btn" data-quadrant="4">
          <div class="quad-top"><span class="quad-tag" style="color:var(--success);">QUADRANT IV · SCALE &amp; FINOPS</span><span style="color:var(--success);">{SVG_SPEED}</span></div>
          <h3 class="quad-title">Sparse Weights, Harnesses &amp; System 1</h3>
          <p class="quad-sub">High-Velocity Coding, ADK Routing &amp; output_tokens: 0 Triage</p>
        </button>
      </div>

      <div class="quad-detail" id="quadrant-detail-box">
        <div class="qd-head">
          <h4 id="quadrant-title" class="qd-title"></h4>
          <span id="quadrant-badge" class="q-pill pill-coral" style="font-family:var(--font-code);"></span>
        </div>
        <p class="qd-desc"><strong>Enterprise Profile &amp; Industry Patterns:</strong> <span id="quadrant-desc"></span></p>
        <div class="qd-stack-box">
          <span class="qd-stack-lbl">Recommended Google Cloud Reference Stack:</span>
          <span id="quadrant-stack" class="qd-stack-code"></span>
        </div>
        <div class="qd-foot">
          <span id="quadrant-module"></span>
          <a id="quadrant-jump" href="#series-part-5" class="qd-cta"><span>View Hands-On Module</span>{SVG_ARROW}</a>
        </div>
      </div>
    </section>

    <!-- 04 · DEEP-DIVE WHITEPAPER CHAPTERS, INFOGRAPHICS & REFERENCES (§1–§8) -->
    <section id="full-playbook">
      <div class="sec-header">
        <div>
          <span class="sec-eyebrow">04 · COMPLETE PRACTITIONER WHITEPAPER (§1–§8)</span>
          <h2 class="sec-h2">Architecture Deep-Dive, Infographics &amp; Primary Sources</h2>
          <p class="sec-sub">Full release-tier specifications, three-layer runtime architecture, 7 operational risk mitigations, and cited bibliography ([1]–[20]).</p>
        </div>
        <a href="https://github.com/kanchpat/open-weight-models/blob/main/whitepaper/enterprise-playbook.md" target="_blank" rel="noopener noreferrer" class="btn-secondary-warm" style="font-size:12.5px;padding:7px 13px;">
          <span>Read Raw Markdown</span>
          {SVG_EXT}
        </a>
      </div>

      <div class="playbook-paper">
        {ent_body_html}
      </div>
    </section>

    <!-- 05 · 7-PART CODE & VIDEO SERIES -->
    <section id="series-overview">
      <div class="series-hero">
        <div class="series-orb"></div>
        <div class="series-hero-inner">
          <div>
            <span class="series-pill">{SVG_BOOK} Weekly Companion Hands-On Blueprint · Nov 6 – Dec 18, 2026</span>
            <h2 class="series-h2">Explore the 7-Part Code &amp; Video Series on Google Cloud</h2>
            <p class="series-lead">
              Every architectural pattern, FinOps model, and license triage rule in this guide ships with Friday releases containing runnable Vertex AI notebooks, vLLM Cloud Run Dockerfiles, ADK harnesses, and short video walkthroughs.
            </p>
          </div>
          <a href="https://github.com/kanchpat/open-weight-models" target="_blank" rel="noopener noreferrer" class="btn-amber-gold">
            <span>Clone Repo on GitHub</span>
            {SVG_EXT}
          </a>
        </div>
      </div>

      <div class="series-cards-grid">
        <article class="sc-card sc-live" id="series-part-1">
          <div>
            <div class="sc-date">Part 1 · Nov 6, 2026 · Live Now</div>
            <h3 class="sc-title">Open-Weight AI for the Enterprise: Strategy, Economics &amp; the 2×2 Portfolio Matrix</h3>
            <div class="sc-stack">Vertex AI Model Garden (Gemma 4, Qwen 3.8, DeepSeek-V4.1-Flash, Olmo 3)</div>
            <p class="sc-desc">Anchor executive whitepaper &amp; live toolkit: 4-tier openness spectrum, Green/Amber/Red license triage, 5 Industry Patterns, 73% duty-cycle FinOps rule, and 2×2 Workload Router.</p>
          </div>
          <div class="sc-foot">
            <button type="button" class="sc-btn-play" id="series-p1-play">▶ Play Video (5:01)</button>
            <a href="https://youtu.be/qcz1GhjCBOw" target="_blank" rel="noopener noreferrer" style="font-weight:700;">YouTube ↗</a>
          </div>
        </article>

        <article class="sc-card" id="series-part-2">
          <div>
            <div class="sc-date">Part 2 · Nov 13, 2026</div>
            <h3 class="sc-title">Start Serverless: Zero-Ops Open-Weight Agents on Vertex AI OpenMaaS</h3>
            <div class="sc-stack">series/part-02-openmaas-serverless/</div>
            <p class="sc-desc">Why OpenMaaS PayGo ($0.907/1M) beats dedicated self-deploy ($1.29/1M) by 1.42× below 73% utilization + building a tool-calling Gemma 4 / Qwen agent with $0 idle burn.</p>
          </div>
          <div class="sc-foot">
            <span style="color:var(--on-surface-variant);">Unlocks Friday Nov 13 · cURL + Vertex SDK</span>
            <a href="https://github.com/kanchpat/open-weight-models/tree/main/series/part-02-openmaas-serverless" target="_blank" rel="noopener noreferrer" style="font-weight:700;">Module ↗</a>
          </div>
        </article>

        <article class="sc-card" id="series-part-3">
          <div>
            <div class="sc-date">Part 3 · Nov 13, 2026</div>
            <h3 class="sc-title">&ldquo;Don&#39;t Train the Model, Evolve the Harness&rdquo;: ADK Routing &amp; System 1</h3>
            <div class="sc-stack">series/part-03-adk-harness-system1/</div>
            <p class="sc-desc">Combining Gemini 3.1 Pro + Gemma 4 / DeepSeek in Google ADK (-64% thread cost) with System 1 single-pass rubric verification gates (+16.7pp accuracy, 35× faster).</p>
          </div>
          <div class="sc-foot">
            <span style="color:var(--on-surface-variant);">Unlocks Friday Nov 13 · ADK + Pattern 3</span>
            <a href="https://github.com/kanchpat/open-weight-models/tree/main/series/part-03-adk-harness-system1" target="_blank" rel="noopener noreferrer" style="font-weight:700;">Module ↗</a>
          </div>
        </article>

        <article class="sc-card" id="series-part-4">
          <div>
            <div class="sc-date">Part 4 · Nov 20, 2026</div>
            <h3 class="sc-title">When &amp; How to Self-Host: Scale-to-Zero vLLM &amp; QAT on Cloud Run</h3>
            <div class="sc-stack">series/part-04-cloudrun-vllm-qat/</div>
            <p class="sc-desc">Avoiding idle GPU burn on custom containers using Cloud Run scale-to-zero GPUs, vLLM prefix caching / prefill heads (Pattern 1), and Gemma 4 FP4/INT4 QAT.</p>
          </div>
          <div class="sc-foot">
            <span style="color:var(--on-surface-variant);">Unlocks Friday Nov 20 · Cloud Run L4/H100</span>
            <a href="https://github.com/kanchpat/open-weight-models/tree/main/series/part-04-cloudrun-vllm-qat" target="_blank" rel="noopener noreferrer" style="font-weight:700;">Module ↗</a>
          </div>
        </article>

        <article class="sc-card" id="series-part-5">
          <div>
            <div class="sc-date">Part 5 · Nov 20, 2026</div>
            <h3 class="sc-title">Sovereign &amp; Matter-Isolated Agents: In-VPC Open Weights on Agent Runtime</h3>
            <div class="sc-stack">series/part-05-agent-runtime-vpc/</div>
            <p class="sc-desc">Deploying SHA-256-pinned open weights inside private VPC perimeters on Vertex AI Agent Runtime with System 1 guardrails, Model Armor, and PII redaction.</p>
          </div>
          <div class="sc-foot">
            <span style="color:var(--on-surface-variant);">Unlocks Friday Nov 20 · Sovereign VPC</span>
            <a href="https://github.com/kanchpat/open-weight-models/tree/main/series/part-05-agent-runtime-vpc" target="_blank" rel="noopener noreferrer" style="font-weight:700;">Module ↗</a>
          </div>
        </article>

        <article class="sc-card" id="series-part-6">
          <div>
            <div class="sc-date">Part 6 · Dec 4, 2026</div>
            <h3 class="sc-title">Beyond the Prompt Tax: LoRA, &lt;$100 Verifiable RL (GRPO) &amp; Multi-LoRA</h3>
            <div class="sc-stack">series/part-06-lora-grpo-verifiable-rl/</div>
            <p class="sc-desc">Eliminating 10,000-token few-shot prompt bloat via LoRA/QLoRA, single-GPU Verifiable RL (SkyRL GRPO: &lt;$100, +9.6% F1, Pattern 5), and dynamic Multi-LoRA serving.</p>
          </div>
          <div class="sc-foot">
            <span style="color:var(--on-surface-variant);">Unlocks Friday Dec 4 · Vertex AI + SkyRL</span>
            <a href="https://github.com/kanchpat/open-weight-models/tree/main/series/part-06-lora-grpo-verifiable-rl" target="_blank" rel="noopener noreferrer" style="font-weight:700;">Module ↗</a>
          </div>
        </article>

        <article class="sc-card" id="series-part-7" style="grid-column: 1 / -1;">
          <div>
            <div class="sc-date">Part 7 · Dec 11, 2026 · Series Wrap-Up Dec 18</div>
            <h3 class="sc-title">The &ldquo;Frontier-to-Open&rdquo; Distillation Playbook: 10× Cost Cut &amp; &lt;150 ms TTFT</h3>
            <div class="sc-stack">series/part-07-frontier-distillation/</div>
            <p class="sc-desc">Using Gemini 3.1 Pro as an offline teacher to synthesize rubric-verified domain pairs and distilling into compact Gemma 4 (26B-A4B / E4B) students for &lt;150 ms TTFT at 10% of frontier serving cost (Patterns 2 &amp; 4).</p>
          </div>
          <div class="sc-foot">
            <span style="color:var(--on-surface-variant);">Unlocks Friday Dec 11 · Teacher-Student Distillation</span>
            <a href="https://github.com/kanchpat/open-weight-models/tree/main/series/part-07-frontier-distillation" target="_blank" rel="noopener noreferrer" style="font-weight:700;">Module ↗</a>
          </div>
        </article>
      </div>
    </section>

    <!-- WARM EDITORIAL FOOTER & OFFICIAL DISCLAIMER -->
    <footer class="site-footer">
      <div class="footer-top">
        <div class="footer-brand">
          <span class="footer-mini-ow">OW</span>
          <span>Open-Weights Enterprise Architect Playbook</span>
        </div>
        <div class="footer-links">
          <span>Authored by <strong>Kanchana Patlolla</strong> &amp; <strong>Anusha Sabbineni</strong> · Guidance from <strong>Alan Blount</strong></span>
          <a href="https://github.com/kanchpat/open-weight-models" target="_blank" rel="noopener noreferrer">GitHub (Apache 2.0) ↗</a>
          <a href="https://youtu.be/qcz1GhjCBOw" target="_blank" rel="noopener noreferrer">YouTube Overview ↗</a>
        </div>
      </div>
      <p class="footer-disclaimer">
        <strong>Disclaimer:</strong> This website (<code>openweights.cloudrace.info</code>) and companion repository are an independent community practitioner guide. This is <strong>not</strong> an officially supported Google product, official Google Cloud documentation, an official statement on behalf of Google LLC, or legal advice. All architectural patterns, FinOps cost estimates, and license summaries are strictly the authors&#39; own.
      </p>
    </footer>

  </main>
</div>

<script>
(function () {{
  "use strict";

  // 1. 5-MINUTE YOUTUBE EXPLAINER PLAYER (Safe DOM APIs only)
  const YT_ID = "qcz1GhjCBOw";
  function playExplainerAt(startSec, shouldScroll) {{
    const safeStart = Math.max(0, Math.min(300, Math.floor(Number(startSec) || 0)));
    const spot = document.getElementById("video-briefing");
    if (shouldScroll && spot) {{
      spot.scrollIntoView({{ behavior: "smooth", block: "center" }});
    }}

    let originStr = "";
    try {{ originStr = String(window.location.origin || ""); }} catch (e) {{ originStr = ""; }}
    const proto = String(window.location.protocol || "");
    if ((proto !== "https:" && proto !== "http:") || !originStr || originStr === "null") {{
      const extUrl = safeStart > 0
        ? "https://youtu.be/" + YT_ID + "?t=" + String(safeStart)
        : "https://youtu.be/" + YT_ID;
      window.open(extUrl, "_blank", "noopener,noreferrer");
      return;
    }}

    const stage = document.getElementById("yt-player-stage");
    if (!stage) return;

    const iframe = document.createElement("iframe");
    iframe.setAttribute(
      "src",
      "https://www.youtube-nocookie.com/embed/" + YT_ID + "?autoplay=1&rel=0&modestbranding=1&playsinline=1&start=" + String(safeStart)
    );
    iframe.setAttribute("title", "Open-Weight AI Models for Enterprise Architects — 5-Minute Explainer");
    iframe.setAttribute("allow", "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share");
    iframe.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    iframe.setAttribute("allowfullscreen", "");
    stage.replaceChildren(iframe);
  }}

  const posterTrigger = document.getElementById("yt-poster-trigger");
  if (posterTrigger) {{
    posterTrigger.addEventListener("click", function () {{ playExplainerAt(0, false); }});
  }}
  const heroVideoBtn = document.getElementById("hero-video-btn");
  if (heroVideoBtn) {{
    heroVideoBtn.addEventListener("click", function () {{ playExplainerAt(0, true); }});
  }}
  const seriesP1Play = document.getElementById("series-p1-play");
  if (seriesP1Play) {{
    seriesP1Play.addEventListener("click", function () {{ playExplainerAt(0, true); }});
  }}

  // 2. FINOPS 73% DUTY-CYCLE BREAK-EVEN CALCULATOR
  const tokenSlider = document.getElementById("token-slider");
  const dutySlider = document.getElementById("duty-slider");

  function updateFinOps() {{
    const dailyM = Math.max(1, Math.min(150, parseInt(tokenSlider.value || "25", 10) || 25));
    const dutyPct = Math.max(10, Math.min(95, parseInt(dutySlider.value || "35", 10) || 35));
    const monthlyM = dailyM * 30;

    document.getElementById("token-val-display").textContent = dailyM + "M tokens/day (" + monthlyM.toLocaleString() + "M/mo)";
    document.getElementById("duty-val-display").textContent = dutyPct + "% Duty Cycle";

    const closedRate = 10.0;
    const maasRate = 0.907;
    const dedEffRate = maasRate * (73.0 / dutyPct);

    const totalClosed = Math.round(monthlyM * closedRate);
    const totalMaas = Math.round(monthlyM * maasRate);
    const totalDed = Math.round(monthlyM * dedEffRate);
    const totalSys1 = Math.max(45, Math.round(monthlyM * 0.05));
    const maxVal = Math.max(totalClosed, totalDed, totalMaas, 1);

    document.getElementById("cost-closed").textContent = "$" + totalClosed.toLocaleString() + "/mo";
    document.getElementById("cost-openmaas").textContent = "$" + totalMaas.toLocaleString() + "/mo";
    document.getElementById("cost-dedicated").textContent = "$" + totalDed.toLocaleString() + "/mo";
    document.getElementById("cost-dedicated-rate").textContent = "$" + dedEffRate.toFixed(2) + " / 1M effective";
    document.getElementById("cost-system1").textContent = "$" + totalSys1.toLocaleString() + "/mo";

    document.getElementById("bar-closed").style.width = Math.max(3, Math.round((totalClosed / maxVal) * 100)) + "%";
    document.getElementById("bar-maas").style.width = Math.max(3, Math.round((totalMaas / maxVal) * 100)) + "%";
    document.getElementById("bar-ded").style.width = Math.max(3, Math.round((totalDed / maxVal) * 100)) + "%";
    document.getElementById("bar-sys1").style.width = Math.max(2, Math.round((totalSys1 / maxVal) * 100)) + "%";

    const savingsPct = Math.round((1 - (Math.min(totalMaas, totalDed) / totalClosed)) * 100);
    document.getElementById("note-openmaas").textContent = savingsPct + "% savings vs closed API";

    const dedNote = document.getElementById("cost-dedicated-note");
    const banner = document.getElementById("verdict-banner");
    const vTitle = document.getElementById("verdict-title");
    const vText = document.getElementById("verdict-text");
    const icoInfo = document.getElementById("verdict-icon-info");
    const icoCheck = document.getElementById("verdict-icon-check");

    if (dailyM < 8 && dutyPct < 73) {{
      dedNote.textContent = (dedEffRate / maasRate).toFixed(2) + "× pricier than OpenMaaS";
      dedNote.style.color = "var(--danger)";
      banner.className = "verdict-box verdict-coral";
      icoInfo.style.display = "inline-flex";
      icoCheck.style.display = "none";
      vTitle.textContent = "FinOps Verdict: Pilot Volume (<8M tok/day) — Stay Serverless";
      vText.textContent = "At " + dailyM + "M tokens/day and " + dutyPct + "% utilization, keep zero-ops endpoints on Vertex AI OpenMaaS PayGo ($" + totalMaas.toLocaleString() + "/mo, $0 idle burn) or Closed Frontier APIs. Reserving 24/7 GPUs would cost $" + totalDed.toLocaleString() + "/mo.";
    }} else if (dutyPct < 73) {{
      dedNote.textContent = (dedEffRate / maasRate).toFixed(2) + "× pricier than OpenMaaS";
      dedNote.style.color = "var(--danger)";
      banner.className = "verdict-box verdict-coral";
      icoInfo.style.display = "inline-flex";
      icoCheck.style.display = "none";
      vTitle.textContent = "FinOps Verdict: Below 73% Duty Cycle — Start Serverless";
      vText.textContent = "At " + dutyPct + "% hardware utilization, dedicated GPUs burn idle budget nights and weekends ($" + totalDed.toLocaleString() + "/mo). Deploy on Vertex AI OpenMaaS ($" + totalMaas.toLocaleString() + "/mo) or Cloud Run Scale-to-Zero vLLM GPUs until steady batch traffic clears 73% (Series Parts 2 & 4).";
    }} else {{
      const saved = Math.max(0, totalMaas - totalDed);
      dedNote.textContent = "Beats PayGo (saves $" + saved.toLocaleString() + "/mo)";
      dedNote.style.color = "var(--success)";
      banner.className = "verdict-box verdict-green";
      icoInfo.style.display = "none";
      icoCheck.style.display = "inline-flex";
      vTitle.textContent = "FinOps Verdict: Above 73% Duty Cycle — Dedicated GPU Cluster Justified";
      vText.textContent = "At " + dutyPct + "% sustained utilization, dedicated vLLM instances ($" + totalDed.toLocaleString() + "/mo) clear the 73% duty-cycle barrier while saving " + savingsPct + "% vs. closed APIs. Pair with 1-yr/3-yr Committed Use Discounts and System 1 triage heads ($" + totalSys1.toLocaleString() + "/mo) for classification (Series Parts 4 & 5).";
    }}
  }}
  tokenSlider.addEventListener("input", updateFinOps);
  dutySlider.addEventListener("input", updateFinOps);
  updateFinOps();

  // 3. 11 MODELS FILTER PILLS
  const allowedFilters = {{ all: true, permissive: true, gcp: true, tier4: true, system1: true, capped: true }};
  const filterBtns = document.querySelectorAll(".model-filter-btn");
  const modelCards = document.querySelectorAll(".model-card");

  filterBtns.forEach(function (btn) {{
    btn.addEventListener("click", function () {{
      const rawFilter = btn.getAttribute("data-filter") || "all";
      const filter = allowedFilters[rawFilter] ? rawFilter : "all";
      filterBtns.forEach(function (b) {{ b.classList.remove("active"); }});
      btn.classList.add("active");
      modelCards.forEach(function (card) {{
        const cats = (card.getAttribute("data-category") || "").split(" ");
        card.style.display = (filter === "all" || cats.indexOf(filter) !== -1) ? "flex" : "none";
      }});
    }});
  }});

  // 4. LICENSE & DATA AUDITABILITY TRIAGE (All 11 Cohorts, Safe DOM Construction)
  const LICENSE_MODELS = [
    {{ name: "Google Gemma 4 (31B / 26B-A4B / E4B / MedGemma)", license: "Apache 2.0", origin: "US", auditLevel: 2, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "Apache 2.0 + explicit patent grant · US Origin · Open QAT Recipe · Vertex AI OpenMaaS" }},
    {{ name: "Ai2 Olmo 3 (32B Think) & Tülu 3", license: "Apache 2.0 / OpenMDW", origin: "US", auditLevel: 3, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "OpenMDW · US Origin · 100% Auditable Dolma 3 Pre-Training Corpus & Code (Tier 4)" }},
    {{ name: "Aleph Alpha Kolibri (78B-A3.5B MoE)", license: "Apache 2.0", origin: "EU", auditLevel: 3, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "Apache 2.0 · EU Sovereign Origin · Merlin-Arthur Grounded Citation Verification (Tier 4)" }},
    {{ name: "Reflection AI Beam 1.0 (501B-A23B)", license: "Apache 2.0", origin: "US", auditLevel: 2, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "Apache 2.0 · US Origin · Frontier Sparse MoE for Multi-Step Enterprise Agents" }},
    {{ name: "Alibaba Qwen 3.8 (27B & Flash-Next 180B-A6B)", license: "Apache 2.0", origin: "CN", auditLevel: 2, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "Permissive Apache 2.0 workhorse · Check FedRAMP / Defense geopolitical origin policies" }},
    {{ name: "DeepSeek-V4.1-Flash (763B / 8B–16B Active)", license: "MIT", origin: "CN", auditLevel: 2, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "Permissive MIT · 437× KV-cache compression (76× lower multi-turn coding cost)" }},
    {{ name: "Mistral Large 4 (1T/52B) & Timestral", license: "Apache 2.0 / Mod-MIT", origin: "EU", auditLevel: 1, cap10b: false, cap100m: false, cap700m: false, ncAdapter: false, note: "EU Origin · Large 4 is Apache 2.0 (93.3% Lakera B3 safety); Timestral weights use Mod-MIT" }},
    {{ name: "Meta Llama 4 (Maverick / Scout)", license: "Llama 4 Community", origin: "US", auditLevel: 1, cap10b: false, cap100m: false, cap700m: true, ncAdapter: false, note: "US Origin · Mandatory 'Llama' naming prefix + commercial license gate above 700M MAU" }},
    {{ name: "Moonshot Kimi K3.1 Pro & Muse Spark Open", license: "Custom 100M MAU Cap", origin: "CN/US", auditLevel: 1, cap10b: false, cap100m: true, cap700m: true, ncAdapter: false, note: "Requires commercial agreement above 100M MAU or $20M/mo inference revenue" }},
    {{ name: "Zhipu GLM-5.3-Flash (320B-A18B)", license: "Custom $10B Val Gate", origin: "CN", auditLevel: 1, cap10b: true, cap100m: true, cap700m: true, ncAdapter: false, note: "Triggers mandatory commercial/security gate if corporate valuation or revenue >= $10B" }},
    {{ name: "firelex/jeff (Sanctions & SOC LoRA Adapters)", license: "CC BY-NC 4.0", origin: "US", auditLevel: 2, cap10b: false, cap100m: false, cap700m: false, ncAdapter: true, note: "Split-artifact trap: base weights are Apache 2.0, but fine-tuned LoRA adapters carry CC BY-NC 4.0" }}
  ];

  const valSel = document.getElementById("val-select");
  const mauSel = document.getElementById("mau-select");
  const regSel = document.getElementById("region-select");
  const audSel = document.getElementById("audit-select");

  function updateLicenseTriage() {{
    const valStep = Math.max(1, Math.min(5, parseInt(valSel.value || "4", 10) || 4));
    const mauStep = Math.max(1, Math.min(5, parseInt(mauSel.value || "3", 10) || 3));
    const regStep = Math.max(1, Math.min(3, parseInt(regSel.value || "1", 10) || 1));
    const audStep = Math.max(1, Math.min(3, parseInt(audSel.value || "1", 10) || 1));

    const listEl = document.getElementById("license-results-list");
    const tallyEl = document.getElementById("triage-tally");
    if (!listEl) return;

    const frag = document.createDocumentFragment();
    let greenCnt = 0;
    let amberCnt = 0;
    let redCnt = 0;

    LICENSE_MODELS.forEach(function (m) {{
      let status = "green";
      let badgeText = m.auditLevel === 3 ? "🟢 Tier 4 Approved" : "🟢 Default Approved";
      const reasons = [];

      if (m.ncAdapter) {{
        status = "red";
        badgeText = "🔴 Non-Commercial Adapter";
        reasons.push("CC BY-NC 4.0 adapter prohibits commercial production use");
      }}
      if (valStep >= 4 && m.cap10b) {{
        status = "red";
        badgeText = "🔴 Hits $10B Gate";
        reasons.push("Exceeds $10B corporate valuation/revenue gate — requires commercial deal");
      }}
      if (mauStep >= 4 && m.cap100m && status !== "red") {{
        status = "amber";
        badgeText = "🟡 Hits 100M MAU Cap";
        reasons.push("Requires custom commercial agreement above 100M MAU / $20M rev");
      }}
      if (mauStep >= 5 && m.cap700m && !m.cap100m && status !== "red") {{
        status = "amber";
        badgeText = "🟡 Hits 700M MAU Cap";
        reasons.push("Requires custom commercial agreement above 700M MAU");
      }}
      if (regStep === 2 && m.origin !== "US" && m.origin !== "EU") {{
        status = "red";
        badgeText = "🔴 Origin Policy Gate";
        reasons.push("Blocked by US/EU-only sovereign origin filter (" + m.origin + ")");
      }}
      if (regStep === 3 && m.origin !== "EU") {{
        if (m.origin === "US" && status !== "red") {{
          status = "amber";
          badgeText = "🟡 US Origin (Host in EU VPC)";
          reasons.push("US-origin checkpoint — deploy inside EU Sovereign VPC perimeter");
        }} else {{
          status = "red";
          badgeText = "🔴 Non-EU Origin";
          reasons.push("Restricted under strict EU-origin sovereign policy (" + m.origin + ")");
        }}
      }}
      if (audStep > m.auditLevel) {{
        if (status !== "red") {{
          status = "amber";
          badgeText = audStep === 3 ? "🟡 Weights Only (Not Tier 4)" : "🟡 Recipe Undisclosed";
        }}
        reasons.push(audStep === 3 ? "Pre-training data corpus not publicly auditable" : "Post-training recipe not fully disclosed");
      }}

      if (status === "green") greenCnt++;
      else if (status === "amber") amberCnt++;
      else redCnt++;

      const row = document.createElement("div");
      row.className = "triage-row " + (status === "green" ? "tr-green" : (status === "amber" ? "tr-amber" : "tr-red"));

      const left = document.createElement("div");
      left.className = "tr-left";

      const dot = document.createElement("span");
      dot.className = "tr-dot " + (status === "green" ? "dot-green" : (status === "amber" ? "dot-amber" : "dot-red"));
      left.appendChild(dot);

      const textWrap = document.createElement("div");
      const h4 = document.createElement("h4");
      h4.className = "tr-name";
      h4.textContent = m.name;
      textWrap.appendChild(h4);

      const noteSpan = document.createElement("span");
      noteSpan.className = "tr-note";
      noteSpan.textContent = m.note;
      textWrap.appendChild(noteSpan);

      if (reasons.length > 0) {{
        const reasonSpan = document.createElement("span");
        reasonSpan.className = "tr-reason";
        reasonSpan.textContent = "⚠️ " + reasons.join(" · ");
        textWrap.appendChild(reasonSpan);
      }}

      left.appendChild(textWrap);
      row.appendChild(left);

      const pill = document.createElement("span");
      pill.className = "tr-pill " + (status === "green" ? "pill-green" : (status === "amber" ? "pill-amber" : "pill-red"));
      pill.textContent = badgeText;
      row.appendChild(pill);

      frag.appendChild(row);
    }});

    listEl.replaceChildren(frag);
    if (tallyEl) {{
      tallyEl.textContent = greenCnt + " Approved · " + amberCnt + " Conditional · " + redCnt + " Restricted";
    }}
  }}

  [valSel, mauSel, regSel, audSel].forEach(function (sel) {{
    if (sel) sel.addEventListener("change", updateLicenseTriage);
  }});
  updateLicenseTriage();

  // 5. 2x2 WORKLOAD ROUTER
  const QUADRANT_DATA = {{
    "2": {{
      title: "Quadrant II Selected: Sovereign & Reproducible Open Weights (In-VPC)",
      badge: "Part 5 Blueprint (Nov 20)",
      desc: "Pattern 3 (Harvey matter-isolated rubric gates), European banking (Aleph Alpha Kolibri), HIPAA/FDA clinical pinning (MedGemma), and full provenance audits (Ai2 Olmo 3).",
      stack: "Vertex AI Agent Runtime (In-VPC) + SHA-256 Checkpoint Pinning + System 1 Rubric Gate + Google Cloud Model Armor",
      module: "Matching Dispatch: Part 5 — Sovereign & Matter-Isolated Agents on Agent Runtime",
      href: "#series-part-5"
    }},
    "1": {{
      title: "Quadrant I Selected: Post-Trained & Surgically Customized (Own the Moat)",
      badge: "Parts 6 & 7 Blueprints (Dec 4–11)",
      desc: "Pattern 1 (Netflix GenRec vLLM prefill ranker), Pattern 2 (Pinterest vision encoder graft, -90% cost), Pattern 4 (DoorDash distillation, 10× cut), and Pattern 5 (Coinbase <$100 single-GPU GRPO RL, +9.6% F1).",
      stack: "Vertex AI Training (Ray + SkyRL GRPO) + Dynamic Multi-LoRA + Gemini 3.1 Pro → Gemma 4 Distillation",
      module: "Matching Dispatches: Part 6 (LoRA & GRPO RL) & Part 7 (Frontier-to-Open Distillation)",
      href: "#series-part-6"
    }},
    "3": {{
      title: "Quadrant III Selected: Frontier APIs & Serverless OpenMaaS (Rent for Agility)",
      badge: "Part 2 Blueprint (Nov 13)",
      desc: "Spiky exploratory enterprise workloads (<73% GPU duty cycle, $0 idle GPU burn), contractual IP indemnification, and zero-shot PhD science R&D (CritPt v2).",
      stack: "Vertex AI Model Garden OpenMaaS ($0.907/1M, $0 idle) + Gemini 3.1 Pro Fallback + Cloud Run Scale-to-Zero",
      module: "Matching Dispatch: Part 2 — Start Serverless on Vertex AI OpenMaaS",
      href: "#series-part-2"
    }},
    "4": {{
      title: "Quadrant IV Selected: Sparse Weights, Harnesses & System 1 (Scale & FinOps)",
      badge: "Parts 3 & 4 Blueprints (Nov 13–20)",
      desc: "High-velocity coding repositories (DeepSeek-V4.1-Flash 437× KV-cache cut, -76× cost), Google ADK multi-model harnesses (+16.7pp accuracy), and System 1 zero-token triage (35× faster).",
      stack: "Google ADK In-Harness Router + System 1 Single-Pass Heads (output_tokens: 0) + Cloud Run vLLM QAT GPUs",
      module: "Matching Dispatches: Part 3 (ADK & System 1) & Part 4 (Cloud Run Scale-to-Zero vLLM)",
      href: "#series-part-3"
    }}
  }};

  const qBtns = document.querySelectorAll(".quad-btn");
  function selectQuadrant(qId) {{
    const data = QUADRANT_DATA[qId] || QUADRANT_DATA["2"];
    qBtns.forEach(function (b) {{
      b.classList.toggle("active", b.getAttribute("data-quadrant") === qId);
    }});
    document.getElementById("quadrant-title").textContent = data.title;
    document.getElementById("quadrant-badge").textContent = data.badge;
    document.getElementById("quadrant-desc").textContent = data.desc;
    document.getElementById("quadrant-stack").textContent = data.stack;
    document.getElementById("quadrant-module").textContent = data.module;
    document.getElementById("quadrant-jump").setAttribute("href", data.href);
  }}
  qBtns.forEach(function (btn) {{
    btn.addEventListener("click", function () {{
      selectQuadrant(btn.getAttribute("data-quadrant") || "2");
    }});
  }});
  selectQuadrant("2");

  // 6. LEFT SIDEBAR LIVE SCROLL-SPY
  const tocLinks = Array.from(document.querySelectorAll("#sidebar-toc .toc-item[data-spy]"));
  const spySections = tocLinks
    .map(function (a) {{ return document.getElementById(a.getAttribute("data-spy")); }})
    .filter(Boolean);

  function updateScrollSpy() {{
    if (!spySections.length) return;
    let activeId = spySections[0].id;
    for (let i = 0; i < spySections.length; i++) {{
      const rect = spySections[i].getBoundingClientRect();
      if (rect.top <= 148) {{
        activeId = spySections[i].id;
      }}
    }}
    tocLinks.forEach(function (a) {{
      a.classList.toggle("active", a.getAttribute("data-spy") === activeId);
    }});
  }}
  window.addEventListener("scroll", updateScrollSpy, {{ passive: true }});
  updateScrollSpy();
}})();
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

print("Built Stitch Warm Editorial GitHub Pages site at:", out_html_path, "Size:", os.path.getsize(out_html_path))
