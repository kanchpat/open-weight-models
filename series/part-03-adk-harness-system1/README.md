# Part 3 (Nov 13, 2026): 'Don't Train the Model, Evolve the Harness' — Multi-Model Routing & Verification with ADK

> **Authored & Built by:** Kanchana Patlolla & Anusha Sabbineni  
> **⚠️ Unofficial Google Guide:** Independent practitioner guide — not an officially supported Google product or official Google Cloud documentation. Views expressed are the authors' own.

**Stack & Models:** Google ADK + `Gemma 4 26B-A4B` (Vertex OpenMaaS / AI Studio) + `Gemini 3.1 Pro` *(or `Gemini 3 Flash` in AI Studio mode)* + `System 1` Single-Pass Verification (`gemini-decision-1` → 1-line swap to [`dgem`](https://github.com/GoogleCloudPlatform/dgem))

## Overview
Demonstrates why evolving the surrounding agent harness beats retraining base weights: builds a Support Refund & Escalation Triage Agent in **Google ADK** combining tiered in-harness routing (`64%` cost-cut pattern), single-pass `System 1` (`output_tokens: 0`) pre-submission rubric verification (`DeliverableLandingGate`, `+16.7pp` accuracy pattern), and a 5-ticket **Before vs. After Harness** mini-benchmark.

## Lab 2 notebook

| Notebook | What it shows | Runs on | Open |
| :--- | :--- | :--- | :--- |
| [adk_harness_routing_system1.ipynb](adk_harness_routing_system1.ipynb) | Google ADK `LoopAgent` harness with a System 1 front-door router (`Gemma 4` via Vertex OpenMaaS or AI Studio vs. `gemini-3.1-pro-preview` / `gemini-3-flash-preview`), 3 ADK tools, a 4-check single-pass `DeliverableLandingGate` (`gemini-decision-1`, 1-line swap to `dgem`), and a 5-ticket Before vs. After benchmark chart. | CPU Colab (Vertex AI OpenMaaS + free `GOOGLE_API_KEY`, or single-key `ai_studio` mode, no GPU) | [Colab](https://colab.research.google.com/github/kanchpat/open-weight-models/blob/main/series/part-03-adk-harness-system1/adk_harness_routing_system1.ipynb) |

## Graduating to Production
- **System 1 Gate → Apache 2.0 `dgem`:** Set `GATE_BACKEND = "dgem"` and `DGEM_GATEWAY_URL` in Step 0 to point the exact same ADK gate at a self-hosted [`GoogleCloudPlatform/dgem`](https://github.com/GoogleCloudPlatform/dgem) (`DiffusionGemma`) endpoint (see [`examples/python-adk-guard/`](https://github.com/GoogleCloudPlatform/dgem/tree/main/examples/python-adk-guard)).
- **Open-Weight Worker → Vertex AI OpenMaaS:** Built directly into Step 0 (`OPEN_BACKEND = "vertex_openmaas"`, powered by `LiteLlm("openai/google/gemma-4-26b-a4b-it-maas", ...)` + Vertex `gemini-3.1-pro-preview`), or switch `OPEN_BACKEND = "ai_studio"` for zero-GCP single-key prototyping.

*Video walkthrough link unlocks with the Part 3 release.*
