# Google Cloud × Open-Weight AI Models: Enterprise Architect's Playbook & 7-Part Code Series

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Interactive%20Playbook-0B57D0?style=for-the-badge&logo=googlecloud)](https://kanchpat.github.io/open-weight-models/)
[![License](https://img.shields.io/badge/License-Apache%202.0-16A34A?style=for-the-badge)](https://opensource.org/licenses/Apache-2.0)

> **Authors:** Kanchana Patlolla & Anusha Sabbineni · Google Cloud  
> **Live Interactive Documentation & FinOps Toolkit:** **[https://kanchpat.github.io/open-weight-models/](https://kanchpat.github.io/open-weight-models/)**  
> **Repository:** **[https://github.com/kanchpat/open-weight-models](https://github.com/kanchpat/open-weight-models)**

![Google Cloud x Open-Weight AI Models](docs/assets/hero_google_cloud_open_weights.jpg)

---

## ❓ 5 Key Questions Answered in This Playbook

Open-weight models now power **56% of enterprise gateway token volume at 14% of total spend**. Before downloading a model checkpoint or reserving dedicated GPUs, enterprise architects use this repository and interactive documentation site to answer five critical questions:

1. **Release Tiers & Licensing (`§1–2`):** *What are we actually downloading (Tier 1–4 Openness Gradient), and how do we filter out `$10B` corporate valuation gates (`GLM-5.3`), `100M–700M` MAU caps (`Kimi K3`, `Llama 4`), and non-commercial `CC BY-NC` LoRA adapters?*
2. **Runtime Harnesses & `System 1` Models (`§3–4.2`):** *How do we gain `+16.7pp` accuracy by evolving the agent harness in **Google ADK** and achieve `35×` faster, `200×` cheaper triage with single-pass **`System 1` decision heads (`output_tokens: 0`)**?*
3. **Security, Sovereignty & Risk Watch-Outs (`§4.3`):** *How do we defend against `$1,200` weight abliteration, shadow checkpoints, and data residency barriers using **`SHA-256` pinning in Artifact Registry**, in-VPC execution, and **Model Armor**?*
4. **Industry Patterns (`§5`):** *How are **Netflix (`GenRec`)**, **Pinterest**, **Harvey**, **DoorDash**, and **Coinbase & Uber** deploying open-weight models in production today?*
5. **The `73%` FinOps Rule & Google Cloud Stack (`§6–7`):** *Why does self-deploying dedicated GPUs cost **`1.42×` more** than serverless **Vertex AI OpenMaaS (`$0.907/1M` tokens)** below a **`73%` hardware duty cycle**—and when should you switch to **Cloud Run scale-to-zero GPUs (`vLLM` + `QAT`)** or **Vertex AI Agent Runtime**?*

---

## 🧩 All 11 Open-Weight Model Families Covered

| Model Family | Openness Tier | License & Governance | Enterprise Sweet Spot | Recommended Google Cloud Surface |
| :--- | :--- | :--- | :--- | :--- |
| **Google `Gemma 4` (`31B`, `26B-A4B`, `E4B`, `MedGemma`)** | **Tier III** (Open Recipe + QAT) | 🟢 `Apache 2.0` | Zero tool-call drift under `FP4`/`INT4` QAT; `<150 ms` teacher-student distillation target | **Vertex AI OpenMaaS · Cloud Run `vLLM` · ADK** |
| **Ai2 `Olmo 3` (`32B Think`) & `Tülu 3`** | **Tier IV** (100% Open Source) | 🟢 `Apache 2.0` / `OpenMDW` | Full pre-training corpus (`Dolma 3`) + RLVR code for EU AI Act & copyright auditability | **Vertex AI Model Garden · Agent Runtime VPC** |
| **`DeepSeek-V4.1-Flash` (`1017`)** | **Tier III** (Open Weights) | 🟢 `MIT` | `763B` total / `8B–16B` active MoE with `CSA2` (`437×` KV-cache cut; `76×` lower coding cost) | **Vertex AI OpenMaaS · ADK Tiered Router** |
| **Alibaba `Qwen 3.8` (`27B` & `Flash-Next 180B-A6B`)** | **Tier III** (Open Weights) | 🟢 `Apache 2.0` | High-throughput multilingual & coding workhorse; vision encoder graft base (*Pattern 2*) | **Vertex AI OpenMaaS · Cloud Run GPUs** |
| **Mistral `Large 4` (`1T/52B`) & `Timestral`** | **Tier III** (Open Weights) | 🟢 `Apache 2.0` / `Mod-MIT` | `93.3%` Lakera B3 adversarial safety defense; `Timestral` zero-shot forecasting (`5,000` series/s) | **Vertex AI Model Garden · Cloud Run `vLLM`** |
| **Reflection AI `Beam 1.0` (`501B-A23B`)** | **Tier III** (Open Weights) | 🟢 `Apache 2.0` | US-origin frontier Sparse MoE (`501B` total / `23B` active) for multi-step agentic workflows | **Vertex AI Model Garden · Agent Runtime** |
| **Aleph Alpha `Kolibri` (`78B-A3.5B` MoE)** | **Tier IV** (Sovereign Verified) | 🟢 `Apache 2.0` | European sovereign MoE with cryptographic citation verification (`44%` abstention) | **Vertex AI Agent Runtime (EU Sovereign VPC)** |
| **`System 1` Decision Models (`dgem`, `Clef`, `Clairic`, `Decision-1`)** | **Tier III** (Single-Pass Heads) | 🟢 `Apache 2.0` | `0.6B–4B` single forward pass (`output_tokens: 0`); `35×` faster (`5.8–84 ms`) & `200×` cheaper triage | **Google ADK Gate · Cloud Run · Agent Runtime** |
| **Meta `Llama 4` (`Maverick` / `Scout`)** | **Tier III** (Threshold License) | 🟡 `700M MAU Cap` | Multimodal native MoE (`17B` active); requires `"Llama"` naming prefix & commercial deal `>700M` MAU | **Vertex AI Model Garden** |
| **Moonshot `Kimi K3.1 Pro` & `K3`** | **Tier III** (Threshold License) | 🟡 `100M MAU / $20M Cap` | Long-horizon deep-research MoE; requires custom commercial license above `100M` MAU | **Self-Hosted `vLLM` on GKE / Cloud Run** |
| **Zhipu `GLM-5.3-Flash` (`320B-A18B`)** | **Tier III** (Valuation Gate) | 🔴 `$10B Valuation Cap` | Fast agentic coding, but triggers mandatory commercial & security gate if corporate valuation `>= $10B` | **Requires Commercial Gate Clearance** |

---

## 📂 Repository Structure

```text
open-weight-models/
├── README.md                                   # Repository overview & quick-start guide
├── docs/                                       # GitHub Pages site root (Deploy from main -> /docs)
│   ├── index.html                              # Self-contained Interactive Playbook + FinOps Calculators
│   ├── .nojekyll                               # Bypasses Jekyll processing on GitHub Pages
│   └── assets/                                 # High-resolution architecture diagrams & hero visuals
├── whitepaper/
│   └── enterprise-playbook.md                  # Canonical Markdown source of the Enterprise Playbook
├── scripts/
│   └── build_github_pages.py                   # Rebuilds docs/index.html from whitepaper/enterprise-playbook.md
└── series/                                     # 7-Part Weekly Google Cloud Code & Video Series
    ├── part-02-openmaas-serverless/            # Nov 13: Zero-Ops OpenMaaS Serverless Agents ($0.907/1M)
    ├── part-03-adk-harness-system1/            # Nov 13: ADK Multi-Model Routing & System 1 Rubric Gates
    ├── part-04-cloudrun-vllm-qat/              # Nov 20: Scale-to-Zero vLLM & Gemma 4 QAT on Cloud Run GPUs
    ├── part-05-agent-runtime-vpc/              # Nov 20: Sovereign In-VPC Agents & Guardrails on Agent Runtime
    ├── part-06-lora-grpo-verifiable-rl/        # Dec 04: LoRA, <$100 Single-GPU GRPO RL & Multi-LoRA
    └── part-07-frontier-distillation/          # Dec 11: Gemini 3.1 Pro -> Gemma 4 Distillation (<150 ms TTFT)
```

---

## 🚀 Publishing & Keeping GitHub Pages Current

1. **Push to `https://github.com/kanchpat/open-weight-models`:**
   ```bash
   cd ~/open-weight-models
   git push -u origin main
   ```
2. **Enable GitHub Pages:**
   - Open **[github.com/kanchpat/open-weight-models/settings/pages](https://github.com/kanchpat/open-weight-models/settings/pages)**.
   - Under **Build and deployment**, select **Deploy from a branch** → Branch: **`main`** → Folder: **`/docs`** → click **Save**.
   - Your interactive site will publish at **`https://kanchpat.github.io/open-weight-models/`**.
3. **Keep the Document Current:**
   - Edit `whitepaper/enterprise-playbook.md` and run `python3 scripts/build_github_pages.py` to regenerate `docs/index.html`, then commit and push.
