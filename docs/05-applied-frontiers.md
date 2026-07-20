# 05 · Applied frontiers

> The same recipe, pointed at new domains: biology as a world model, and engineering
> as a real-time strategy game.

Two applied areas that show the [meta-thesis](00-thesis.md) in the wild — one
scientific, one about how we actually work day-to-day.

---

## A. The bitter lesson comes from biology (protein world models)

The scaling/self-supervision recipe transferred cleanly to **protein biology** —
strong evidence the [world-model](01-world-models.md) approach generalizes beyond
language and vision.

**ESM Cambrian (ESMC)** — a BERT-style masked model trained on evolutionary protein
sequences (20-amino-acid alphabet), told **nothing but the sequence**:

- **Scaling laws hold.** Log-linear improvement across 300M / 600M / 6B params,
  measured by **long-range contact precision** (an unsupervised readout of learned
  3D structure). The unlock over the earlier ESM2 plateau wasn't architecture — it
  was **data scaling**: 50M → **2.8B** samples, largely **metagenomic** (sequences
  from dirt, oceans, guts). Evolution has been generating training data for 4 billion
  years; we've sampled <1% of known protein diversity.
- **The bitter lesson holds vs AlphaFold.** AlphaFold leans on hand-built multiple
  sequence alignments (MSAs). ESMC throws them away, feeds its own embeddings to a
  structure head, and lands **within ~3 points of AlphaFold3** generally — and
  **beats it on antibody design**, precisely where data is scarce and hand-features
  don't help. A **looped/recurrent structure head** gives a **test-time-compute
  lever** (more loops → better) — the [inference-time compute](02-self-play.md) idea,
  in biology.
- **Interpretability transfers.** Sparse autoencoders find clean, hierarchical,
  **monosemantic** biological features (amino acid → motif → domain → function), all
  learned with **zero supervision** — the LLM mech-interp toolkit ported to proteins.

**Why it's here:** it is the cleanest proof that "predict masked latents at scale"
is a *general* world-model recipe, not a language trick. And the biology data curve
is still bending upward, unlike text. ([Biohub / ESM](https://ai.meta.com/research/vjepa/) — see [SOURCES](../SOURCES.md))

---

## B. Programming is an RTS game now (agentic engineering)

The most immediately usable area: how to actually *run* agentic development. The
reframe (Lukens Orthwein, channel AI):

> Old programming was **chess** — linear, careful, single-threaded, robust-by-design.
> Agentic programming is **real-time strategy** — balance many things at once, keep
> everything busy, parallelize both your systems *and your attention*, course-correct
> as the map reveals.

The concrete playbook (measured result: **3.5× PRs/engineer/month** from LLMs, **+60%**
more once the whole team adopted it):

- **Orchestrator + worker agents on git worktrees** so many repos develop in parallel
  without stepping on each other. **Minimize keystrokes from idea → work started**;
  grab a unit, click across the map, correct later.
- **Workers push to a PR before asking for feedback**, even if wrong — low premium on
  their time, high on yours. Run many in parallel even if token-wasteful; **idle
  Claude tokens are an inefficient economy.**
- **Bake known weaknesses into `CLAUDE.md`** and a graph of linked MD files — e.g.
  Claude is terrible at time estimates (trained on human durations; says "two weeks"
  for a 20-minute task), so instruct it to never trust itself there.
- **Aggressive wiki-style docs.** Code is an *expensive* source of truth for agents;
  linked MD docs are cheap to parse and benefit future agents + human auditability.
- **High visibility over fire-and-forget.** Jump between agents like RTS hotkeys;
  audio/color cues per agent; an **APM tracker** counting **tool calls per minute**.
- **Principles:** macro by default, micro when it counts; satisficing (good enough,
  not perfect); mix ticket sizes; everyone full-stack always.

**Why it's here:** this is a direct upgrade to how we run Claude Code across the
Mal0ss repos. It also *is* the meta-thesis — a tight human-in-the-loop
feedback cycle with visibility and course-correction.

### Adopt-now checklist for our repos

- [ ] A real `CLAUDE.md` weakness-list per active repo (time estimates, known
      footguns, house style, which browser/tools).
- [ ] Worktree-based orchestrator flow for parallel work (start with Hermes + net).
- [ ] Wiki-style linked MD docs as the agent substrate — Pharos itself is an example;
      Hermes' `HERMES_SUPER_PROMPT.md` and Kaizen's design log already do this.
- [ ] Workers → PR-first, corrected after.

---

*Prev: [04 · Verified intelligence](04-verified-intelligence.md) · Next: [06 · Oneiros positioning →](06-oneiros-positioning.md)*
