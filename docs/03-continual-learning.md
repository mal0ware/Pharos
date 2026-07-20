# 03 · Continual-learning architectures

> The transformer is static after training. Humans aren't. This is the gap.

---

## 1. The problem, stated precisely

An LLM's weights **freeze** at training time. It cannot acquire new knowledge or
skills from new interactions — it can only be *re-*trained. Two consequences framed
as the field's two hardest open problems (Chaubard):

- **Intelligence per sample.** Given one new example, what is the *optimal* update?
  In practice people use in-context learning (ICL) — but ICL does **not**
  monotonically improve with more examples. It bobs and weaves, sometimes gets
  *worse*, then hits the **context-length cliff** and simply stops. Low-rank
  fine-tuning (LoRA) does well at low sample counts then peters out; full SFT wins
  only at the far end. There's a *different* optimal method at every point along the
  stream — which is nothing like how a human learns.
- **Intelligence per watt.** Smaller models can be *better* per unit energy. Bigger
  isn't automatically smarter once you price in compute.

A human who plays 10,000 games keeps improving **on the same algorithm**. That
suggests a learning procedure with far higher intelligence-per-sample exists and we
haven't found it. ([Continual Learning Bench, arXiv 2606.05661](https://arxiv.org/html/2606.05661))

## 2. The 2026 candidate: Nested Learning

Google introduced **Nested Learning** — reframing a model not as one continuous
process but as **a system of nested optimization problems, each with its own update
workflow and timescale**, optimized simultaneously. The brain-inspired claim: learn
at multiple levels of abstraction and multiple speeds at once, which **mitigates or
avoids catastrophic forgetting** (where learning new tasks destroys old skills).

Reported framing: architectural shifts like this deliver **4–17× effective
performance** over raw scaling in memory/reasoning-heavy domains — the strongest
signal yet that "beyond the static transformer" is a real direction, not a slogan.
([Google Research](https://research.google/blog/introducing-nested-learning-a-new-ml-paradigm-for-continual-learning/), [VentureBeat](https://venturebeat.com/ai/googles-nested-learning-paradigm-could-solve-ais-memory-and-continual))

## 3. The adjacent thread: test-time training & self-evolving memory

- **Test-time training (TTT)** — keep training the model *at inference time*, on the
  task in front of it. Extends test-time adaptation (adjusting to distribution shift
  during deployment) toward **continuous self-improvement**.
  ("Learning on the Job: Test-Time Curricula," [arXiv 2510.04786](https://arxiv.org/pdf/2510.04786))
- **Self-evolving memory** — agents that carry an external memory that updates as
  they act, benchmarked by **Evo-Memory** ([arXiv 2511.20857](https://arxiv.org/pdf/2511.20857)).
  This is the same idea as **WorldEvolver** in [self-play](02-self-play.md): improve
  the *context/memory* while keeping weights frozen — a cheap, safe form of continual
  learning.

The design question of 2026: **where does adaptation live?** In the weights (Nested
Learning, TTT) or in an external, updatable store (memory, world-model context)?
Weight updates are powerful but risk forgetting and are expensive; memory updates
are cheap and auditable but bounded by retrieval quality.

## 4. Open problems

- **Catastrophic forgetting isn't solved**, only mitigated; the weight-vs-memory
  tradeoff is unsettled.
- **Evaluation of "statefulness."** New benchmarks (Continual Learning Bench,
  Evo-Memory) exist precisely because we can't yet measure continual learning well.
- **The optimal per-sample update** — the theoretical core of intelligence-per-sample
  — remains open. Alternatives to backprop (e.g. SPSA) are being probed but unproven.

## 5. Implication for our work

Two of our projects are *already* continual-learning systems in disguise:

- **Kaizen** (a private repo of ours) — "always-on, self-improving," with a background scribe
  that distills streams into structured + semantic memory. That is **exactly** the
  frozen-weights + evolving-memory pattern (Evo-Memory / WorldEvolver). The 2026 work
  is a literature to borrow from, and a warning: **memory update is the safe,
  auditable path** — lean on it before touching weights.
- **[Oneiros](06-oneiros-positioning.md)** — a world model that improves as the agent
  acts is a continual-learning system whose "memory" is the world model's context.
  WorldEvolver's three-module design (episodic / semantic / selective foresight) is a
  ready-made architecture to adapt.

**Takeaway:** we don't need to solve continual learning to benefit from it. Adopt the
**frozen-weights, evolving-context** pattern now; watch Nested Learning / TTT for
when weight-level continual learning becomes safe to ship.

---

*Prev: [02 · Self-play](02-self-play.md) · Next: [04 · Verified intelligence →](04-verified-intelligence.md)*
