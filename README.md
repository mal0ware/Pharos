<!-- ════════════════════════════════════════════════════════════════ -->
<!--                       PHAROS · FRONTIER MAP                        -->
<!--   Accent: #7800F0 · A living survey of the 2026 AI frontier        -->
<!-- ════════════════════════════════════════════════════════════════ -->

<div align="center">

# Pharos

**A living map of the AI frontier.**

<sub>The lighthouse of Alexandria let ships see the harbor from far out at sea.<br/>
This repo does the same for AI research: a maintained, cited survey<br/>
of where the field stands, so the projects that use it can aim at where AI is heading.</sub>

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=7800F0&height=3" alt="" />

`maintained by Mal0 · Mal0ss Network` · `last synthesis: 2026-07` · `status: living document`

</div>

---

## Why this exists

AI research moves weekly now, and it is easy to keep reasoning from a 2025 mental
model as if it were still current. Pharos keeps the frontier in one place. It is
rebuilt on a schedule and written to be used as the design basis for the projects
built on top of it, mainly [Oneiros](docs/06-oneiros-positioning.md).

Each area doc covers the core idea, what changed, the main papers and players, the
open problems, and what it means for my own projects.

## The thesis

> The frontier has stopped being "make the transformer bigger." Three threads are
> converging: alternative architectures (JEPA / world models), unbounded learning
> (self-play & self-improvement), and verifiable correctness (formal methods).
> Together they point at one program: systems that build an internal model of a
> domain, improve themselves against it, and can prove they got it right.

## The map

| # | Area | The core shift | Doc |
|---|------|----------------|-----|
| 00 | The meta-thesis | Progress = better feedback loops, not more parameters | [00-thesis.md](docs/00-thesis.md) |
| 01 | World models & JEPA | Predict in *latent space*, not pixels/tokens (the biggest contrarian bet in AI) | [01-world-models.md](docs/01-world-models.md) |
| 02 | Self-play & self-improvement | Remove the human from the training loop; learn past the human subspace | [02-self-play.md](docs/02-self-play.md) |
| 03 | Continual-learning architectures | Beyond static transformers: memory, test-time training, nested optimization | [03-continual-learning.md](docs/03-continual-learning.md) |
| 04 | Verified intelligence | Formal proof (Lean) as the ground truth for math *and* code | [04-verified-intelligence.md](docs/04-verified-intelligence.md) |
| 05 | Applied frontiers | Biology as a world model; agentic engineering as an RTS game | [05-applied-frontiers.md](docs/05-applied-frontiers.md) |
| 06 | Oneiros positioning | Where my own world-model project sits, and its roadmap | [06-oneiros-positioning.md](docs/06-oneiros-positioning.md) |

All citations are in [SOURCES.md](SOURCES.md).

## The 2026 headlines

- Yann LeCun left Meta and raised a ~$1.03B seed round at a $3.5B valuation (Mar 2026) for AMI Labs, the largest seed round in European history. Its thesis is that JEPA world models will replace LLMs, not supplement them. ([TechCrunch](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/))
- The world-models race is now three-way: LeCun's abstract-reasoning JEPA, Fei-Fei Li's World Labs / Marble (persistent 3D from one image, raising at ~$5B), and DeepMind's Genie 3 (the first real-time interactive world model with long-term consistency). ([Introl](https://introl.com/blog/world-models-race-agi-2026))
- Self-play has grown into self-evolving world models. 2026 work (WorldEvolver, ProPlay) improves the world model itself through interaction, which joins the two threads. ([arXiv 2606.30639](https://arxiv.org/abs/2606.30639))
- Architectures are moving past the static transformer. Google's Nested Learning attacks catastrophic forgetting by treating a model as nested optimizers at different timescales. ([Google Research](https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/))
- In formal verification, AlphaProof's successor solved nine open Erdős problems, and Axiom Math raised $200M at $1.6B to take Lean-grade guarantees from math into code ("verifiable coding beats vibe coding"). ([CACM](https://cacm.acm.org/research/formal-reasoning-meets-llms-toward-ai-for-mathematics-and-verification/))

## How to read this repo

- For the overview, read this README and [00-thesis.md](docs/00-thesis.md).
- If you're building something, go straight to the area doc, then [06-oneiros-positioning.md](docs/06-oneiros-positioning.md) for what it means in practice.
- For something you can run, the first working exhibit is in [`demos/self-play/`](demos/self-play/): a zero-dependency simulation of asymmetric self-play that reproduces the central result of *Scaling Self-Play with Self-Guidance* (SGS).

## Maintenance contract

This document goes out of date fast, so it gets rebuilt rather than appended to.

- Re-synthesize monthly, or sooner when a tier-1 result lands.
- Every claim carries a citation in [SOURCES.md](SOURCES.md); undated claims get deleted.
- The field is full of hype and fundraising narratives, so keep *shipped + reproduced* separate from *announced*. [SOURCES.md](SOURCES.md) tags each citation as shipped, announced or theory.

<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=7800F0&height=3" alt="" />

<div align="center"><sub>Pharos · part of the Mal0ss Network · for the love of the game.</sub></div>
