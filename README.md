<!-- ════════════════════════════════════════════════════════════════ -->
<!--                       PHAROS · FRONTIER MAP                        -->
<!--   Accent: #7800F0 · A living survey of the 2026 AI frontier        -->
<!-- ════════════════════════════════════════════════════════════════ -->

<div align="center">

# Pharos

**A living map of the AI frontier.**

<sub>The lighthouse of Alexandria let ships see the harbor from far out at sea.<br/>
This repo is the same instrument pointed at AI research: a maintained, cited survey<br/>
of where the field actually is — so we build for where it's going, not where it was.</sub>

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=7800F0&height=3" alt="" />

`maintained by Mal0 · Mal0ss Network` · `last synthesis: 2026-07` · `status: living document`

</div>

---

## Why this exists

Research moves weekly now. It is easy to keep operating on last year's mental model
as if it were current — to reason from 2025 when the ground has shifted underneath.
Pharos is the antidote: a single place that holds the frontier, is rebuilt on a
cadence, and is written to be *used* — as the design substrate for the projects
that build on top of it (chiefly **[Oneiros](docs/06-oneiros-positioning.md)**).

It is a **deep survey**, not a news feed. Every area gets: the core idea, what
changed, the key papers/players, the open problems, and the direct implication for
our own work.

---

## The one-sentence thesis

> **The frontier has stopped being "make the transformer bigger." Three threads —
> alternative architectures (JEPA / world models), unbounded learning (self-play &
> self-improvement), and verifiable correctness (formal methods) — are converging
> into a single program: systems that build an internal model of a domain, improve
> themselves against it, and can prove they got it right.**

Everything below is a facet of that sentence.

---

## The map

| # | Area | The core shift | Doc |
|---|------|----------------|-----|
| 00 | **The meta-thesis** | Progress = better feedback loops, not more parameters | [00-thesis.md](docs/00-thesis.md) |
| 01 | **World models & JEPA** | Predict in *latent space*, not pixels/tokens — the biggest contrarian bet in AI | [01-world-models.md](docs/01-world-models.md) |
| 02 | **Self-play & self-improvement** | Remove the human from the training loop; learn past the human subspace | [02-self-play.md](docs/02-self-play.md) |
| 03 | **Continual-learning architectures** | Beyond static transformers: memory, test-time training, nested optimization | [03-continual-learning.md](docs/03-continual-learning.md) |
| 04 | **Verified intelligence** | Formal proof (Lean) as the ground truth for math *and* code | [04-verified-intelligence.md](docs/04-verified-intelligence.md) |
| 05 | **Applied frontiers** | Biology as a world model; agentic engineering as an RTS game | [05-applied-frontiers.md](docs/05-applied-frontiers.md) |
| 06 | **Oneiros positioning** | Where our own world-model project sits, and its roadmap | [06-oneiros-positioning.md](docs/06-oneiros-positioning.md) |

All citations live in **[SOURCES.md](SOURCES.md)**.

---

## The 2026 headline, in five bullets

- **Yann LeCun left Meta** and raised **~$1.03B seed at a $3.5B valuation** (Mar 2026) for **AMI Labs** — the largest seed round in European history — on the thesis that **JEPA world models replace LLMs**, not supplement them. The alternative architecture became the main event. ([TechCrunch](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/))
- **The world-models race is now three-way:** LeCun's abstract-reasoning JEPA, **Fei-Fei Li's World Labs / Marble** (persistent 3D from one image, raising at ~$5B), and **DeepMind's Genie 3** (first real-time interactive world model with long-term consistency). ([Introl](https://introl.com/blog/world-models-race-agi-2026))
- **Self-play grew up into self-*evolving world models*** — 2026 work (WorldEvolver, ProPlay) improves the *world model itself* through interaction, fusing the two threads. ([arXiv 2606.30639](https://arxiv.org/abs/2606.30639))
- **Architecture is escaping the static transformer** — Google's **Nested Learning** attacks catastrophic forgetting by treating a model as nested optimizers at different timescales. ([Google Research](https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/))
- **Formal verification hit escape velocity** — AlphaProof's successor solved **nine open Erdős problems**; Axiom Math raised **$200M at $1.6B** to take Lean-grade guarantees from math into code. ("verifiable coding beats vibe coding.") ([CACM](https://cacm.acm.org/research/formal-reasoning-meets-llms-toward-ai-for-mathematics-and-verification/))

---

## How to read this repo

- **Just want the lay of the land?** Read this README + [00-thesis.md](docs/00-thesis.md).
- **Building something?** Go straight to the area doc, then [06-oneiros-positioning.md](docs/06-oneiros-positioning.md) for the "so what."
- **Want proof, not prose?** The first working exhibit is a runnable self-play loop in [`demos/self-play/`](demos/self-play/) — a model that bootstraps from zero with no human data.

---

## Maintenance contract

This document decays. To stay honest it must be rebuilt, not appended to.

- **Cadence:** re-synthesize monthly (or when a tier-1 result lands).
- **Rule:** every claim carries a citation in [SOURCES.md](SOURCES.md); undated claims get deleted.
- **Bias check:** the field is full of hype and fundraising narratives. Separate *shipped + reproduced* from *announced*. Each doc flags which is which.

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=7800F0&height=3" alt="" />

<div align="center"><sub>Pharos · part of the Mal0ss Network · for the love of the game.</sub></div>
