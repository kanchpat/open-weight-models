# Part 2 (Nov 13, 2026): Start Serverless — Building Zero-Ops Open-Weight Agents on Vertex AI OpenMaaS

> **Authored & Built by:** Kanchana Patlolla & Anusha Sabbineni  
> **⚠️ Unofficial Google Guide:** Independent practitioner guide — not an officially supported Google product or official Google Cloud documentation. Views expressed are the authors' own.

**Stack & Models:** Vertex AI OpenMaaS (`Gemma 4 31B/26B`, `Qwen 3.8`, `DeepSeek-V4.1-Flash`)

## Overview
Demonstrates why OpenMaaS PayGo (`$0.907/1M` output tokens) beats dedicated self-deploy (`$1.29/1M`, `1.42x` penalty) below `73%` GPU utilization, with cURL and Python SDK tool-calling agent templates.

## Lab 1 notebooks

| Notebook | What it shows | Runs on | Open |
| :--- | :--- | :--- | :--- |
| [gemma4_openmaas_vision_agent.ipynb](gemma4_openmaas_vision_agent.ipynb) | Serverless Gemma 4 (`gemma-4-26b-a4b-it-maas`): image in, bounding boxes out, then a bounded tool-calling agent with a map of its results. | A Google Cloud project, no GPU | [Colab](https://colab.research.google.com/github/kanchpat/open-weight-models/blob/main/series/part-02-openmaas-serverless/gemma4_openmaas_vision_agent.ipynb) |
| [medgemma_translategemma_clinical_demo.ipynb](medgemma_translategemma_clinical_demo.ipynb) | Bonus: MedGemma 1.5 4B chest X-ray bounding boxes and before/after comparison, with TranslateGemma 4B patient-summary translation and an optional Gradio UI. Educational only, not a medical device. | Colab or Kaggle T4 GPU, Hugging Face token | [Colab](https://colab.research.google.com/github/kanchpat/open-weight-models/blob/main/series/part-02-openmaas-serverless/medgemma_translategemma_clinical_demo.ipynb) |

*Video walkthrough links unlock with the weekly Friday release.*
