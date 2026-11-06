# Part 4 (Nov 20, 2026): When & How to Self-Host — Scale-to-Zero vLLM & QAT Open Models on Cloud Run

> **Authored & Built by:** Kanchana Patlolla & Anusha Sabbineni  
> **⚠️ Unofficial Google Guide:** Independent practitioner guide — not an officially supported Google product or official Google Cloud documentation. Views expressed are the authors' own.

**Stack & Models:** Google Cloud Run GPUs (`vLLM` + `Gemma 4` QAT `E4B`/`26B-A4B`)

## Overview
Avoids idle GPU burn on bursty custom containers using Cloud Run scale-to-zero GPUs, `vLLM` prefix caching, and `Gemma 4` Quantization-Aware Training (`FP4`/`INT4` with zero tool-call drift).

*Code notebooks, Dockerfiles, and video walkthrough links unlock with the weekly Friday release.*
