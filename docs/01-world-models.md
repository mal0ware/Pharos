# 01 · World models & JEPA

> Predict the **world**, not the next token. Predict it in **latent space**, not pixels.

This is the area that reframed the field in 2026, and the one Oneiros lives in.

---

## 1. The core idea

A **language model** predicts the next *word*. A **world model** predicts the next
*state of the world* — it holds a compressed internal picture of how a domain
behaves and can roll it forward ("if I take action X, what happens?") **before**
acting. That forward-rollout is what makes *planning* possible: you search over
imagined futures instead of acting blind.

**JEPA (Joint Embedding Predictive Architecture)** is Yann LeCun's specific recipe
for building one. Its one defining move:

> **Predict in representation (embedding) space, not input space.**

A generative model (GPT for text, a diffusion/video model for pixels) is trained to
reconstruct *every detail* — every pixel, every token. That forces it to spend
capacity modeling inherently unpredictable noise (the exact texture of grass, the
exact phrasing). A JEPA instead:

1. takes an input, masks part of it,
2. encodes both the visible part and the masked part into embeddings,
3. trains a predictor to predict the **embedding** of the masked part from the
   visible part.

Because the target is an abstract embedding, the model is free to **throw away what
it can't predict** and keep only the structure that matters. That is why JEPAs learn
efficient, abstract, plannable features — and why they resist the "blurry average"
failure that dogs pixel-level prediction. LeCun's analogy: it learns the rules of
the world from observation the way a baby learns gravity — not by memorizing frames.

## 2. The lineage (what's real and shipped)

| Model | Year | Modality | What it proved |
|-------|------|----------|----------------|
| **I-JEPA** | 2023 | Images | Latent-space prediction learns strong features with no augmentation hacks |
| **V-JEPA** | 2024 | Video | Same recipe learns physical interactions between objects from raw video |
| **V-JEPA 2** | 2025 | Video → action | A genuine **world model**: zero-shot **robot planning/control** by imagining action outcomes in latent space |

V-JEPA 2 is the load-bearing result: it showed a self-supervised video model can be
used by a robot to *plan* in a new environment it was never trained on. That is the
"learned latent world model an agent plans with" — i.e. exactly the Oneiros premise,
proven at lab scale. ([Meta AI](https://ai.meta.com/research/vjepa/))

## 3. The 2026 shift: this became the biggest bet in AI

- **Yann LeCun left Meta** after 12 years and founded **AMI Labs** (Advanced
  Machine Intelligence), Paris. It raised **~$1.03B seed at a $3.5B valuation**
  (Mar 2026) — the **largest seed round in European history** — backers including
  NVIDIA, Samsung, Bezos Expeditions. The entire thesis: **JEPA world models are the
  successor to LLMs**, not an add-on. ([TechCrunch](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/), [MIT Tech Review](https://www.technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/))

The world-model race is now **three distinct architectural bets**:

| Player | Approach | Product / status |
|--------|----------|------------------|
| **AMI Labs** (LeCun) | Abstract-reasoning JEPA in latent space — common sense & planning | Research stage, $1B+ funded |
| **World Labs** (Fei-Fei Li) | **Spatial intelligence**: persistent, navigable **3D** worlds from one image via Gaussian splatting | **Marble** shipped; raising ~$500M at ~$5B |
| **DeepMind** | **Generative-interactive**: real-time playable worlds, frame-by-frame | **Genie 3** — first to solve long-term consistency (turn around, the building's still there); opened via Project Genie |

The disagreement between them is substantive, not cosmetic: **is a world model an
abstract predictor of dynamics (LeCun) or a renderable 3D environment (Li /
DeepMind)?** LeCun argues pixel-perfect generation is the wrong target; Li argues
spatial grounding is the missing ingredient. Both may be right for different tasks.
([entropytown](https://entropytown.com/articles/2025-11-13-world-model-lecun-feifei-li/), [Introl](https://introl.com/blog/world-models-race-agi-2026))

## 4. The theory caught up (this is the part to actually read)

In **late May 2026**, LeCun's group posted two preprints that, for the first time,
define **precisely when a JEPA learns a *faithful* world model** — the
identifiability question. Headline results from *"When Does LeJEPA Learn a World
Model?"* ([arXiv 2605.26379](https://arxiv.org/abs/2605.26379)):

- **LeJEPA learns a linearly identifiable representation *if and only if* the latent
  variables are Gaussian** and evolve under stable, predictable dynamics. (Forward
  direction from a spectral penalty on nonlinearity; the converse rules out
  non-Gaussian alternatives.)
- An **approximate** identifiability result shows the guarantee **degrades
  gracefully** as assumptions weaken.
- **Linear, orthogonal identifiability enables optimal latent-space planning** — i.e.
  when the representation is identified, planning in latent space is provably clean.

The companion empirical work built a benchmark and found **current world models
still brittle** against this standard. So the theory says *what a good world model
must satisfy*, and the benchmark says *we're not there yet*. That gap is the
research runway. ([Tech Times](https://www.techtimes.com/articles/317452/20260531/yann-lecuns-world-model-earns-formal-proof-benchmark-finds-current-models-brittle.htm))

**Why this matters for us:** it turns "build a world model" from vibes into a
checklist. The identifiability conditions are literal design constraints for Oneiros'
latent space — and they connect directly to [verified intelligence](04-verified-intelligence.md):
a JEPA world model "earned a formal proof."

## 5. Open problems

- **Non-Gaussian / nonstationary worlds.** Real domains rarely have Gaussian latents
  with stable dynamics. How far does graceful degradation actually carry?
- **Abstract vs renderable.** Which tasks need LeCun-style abstract prediction vs
  Li/DeepMind-style renderable 3D? No settled answer.
- **Evaluation.** World models are hard to score. "Long-range contact precision" (bio),
  "does the building persist" (Genie), planning success (V-JEPA 2) are all proxies.
- **Action-conditioning at scale.** V-JEPA 2 plans, but conditioning latent rollouts
  on rich action spaces (beyond robotics) is open — and is exactly Oneiros' territory.

## 6. Implication for our work → [Oneiros](06-oneiros-positioning.md)

Oneiros ("a learned latent world model an agent plans with, exposed over MCP") is a
**direct instantiation of the V-JEPA 2 premise, delivered as agent infrastructure.**
The 2026 developments hand us three gifts:

1. **A validated thesis** — the category is now the field's main bet, not a fringe idea.
2. **Design constraints** — the LeJEPA identifiability conditions are a concrete spec
   for the latent space.
3. **A distribution wedge** — nobody is exposing a plannable world model **over MCP**
   as a callable tool for arbitrary agents. That's an integration nobody in the
   "race" is building, because they're building end-to-end products, not tools.

---

*Prev: [00 · Meta-thesis](00-thesis.md) · Next: [02 · Self-play →](02-self-play.md)*
