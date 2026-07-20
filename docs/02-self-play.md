# 02 · Self-play & self-improvement

> Generate your own tasks, solve them, improve at both. Learn past the human subspace.

This is the training paradigm that pairs with [world models](01-world-models.md):
one gives you a thing to plan against, the other gives you an unbounded source of
learning signal. The runnable exhibit for this doc lives in
[`../demos/self-play/`](../demos/self-play/).

---

## 1. Why it's the answer to a real wall

Post-training RL now rivals or exceeds pretraining compute. As you add RL tasks +
compute, downstream performance improves smoothly (see the Composer-2 report's
task-vs-performance curves). The recipe *works* — but it demands you **hand-collect
RL tasks on a log scale**, and eventually you want the model to surpass **any**
problem a human can author.

**Self-play removes the human from the loop.** One model plays two (or three) roles:

- a **conjecturer** that generates whole RL tasks,
- a **solver** that attempts them,
- (in the good versions) a **guide/judge** that scores whether the task is worth learning from.

Both/all roles are trained. In principle nothing bounds the learning: keep
generating new tasks at the frontier of the solver's ability, solve them, repeat —
the way AlphaZero kept improving past human Go.

### Symmetric vs asymmetric self-play

- **Symmetric** (AlphaGo/AlphaZero): the "task generator" is just an older copy of
  the agent acting as opponent. Same role twice.
- **Asymmetric** (the LLM wave): a distinct **conjecturer** generates arbitrary
  tasks (a coding problem + unit tests, a math statement in Lean) for a **solver**.
  This is the more general and more fragile setting.

## 2. The failure mode everyone hits (and it generalizes)

**Naive self-play plateaus exactly like plain RL.** The diagnosis, from *Scaling
Self-Play with Self-Guidance* (Bailey et al., Tatsu/Tengyu lab), is sharp and worth
internalizing because you will hit it in any self-improving pipeline:

> If you reward the conjecturer purely for producing problems the solver **can't
> solve**, the easiest way to win is to generate **artificially complex, degenerate
> garbage** — the equivalent of a three-page calculus problem the solver slips on
> somewhere. **Tricky ≠ useful.** The signal is real but worthless.

The fix (**SGS**, self-guided self-play):

1. **Ground each synthetic task in a real unsolved target** ("generate a problem
   *related to this one*") so the synthetic distribution stays anchored to a
   distribution you care about.
2. **Add a third "guide" role** — an LLM judge that scores whether the synthetic
   problem is genuinely related and not needlessly complex.
3. **Reward = trickiness × guide-score.** Difficulty still matters (it's what gives
   the solver RL signal), but only *useful* difficulty is rewarded.

**Result:** a **7B** model with SGS + 8× self-play compute reaches roughly the
pass-rate of a **~670B** model on formal-math (Lean) problems. Not solved (not
100%), but a clean, general template. ([arXiv 2604.20209](https://arxiv.org/pdf/2604.20209))

## 3. The 2025 → 2026 arc

**2025 — self-play from zero:**
- **Absolute Zero (AZR)** — RLVR with **no external data at all**: the model
  proposes and refines every problem itself, initialized from a base LLM with no SFT.
  ([arXiv 2505.03335](https://arxiv.org/pdf/2505.03335))
- **R-Zero** — a **challenger** generates problems rewarded by the **solver's
  uncertainty**; the solver is fine-tuned on them and rewarded for solving. The
  canonical challenger/solver co-evolution.
- **SeRL, SSP, Dr.Zero, self-rewarding LLMs** — variants on examiner/student loops
  and models judging their own outputs to build preference data.

**2026 — self-play fused with world models:**
- **WorldEvolver** (Jun 2026) — a **self-evolving world model** that revises its
  deployment-time context while keeping the agent and all weights **frozen**:
  Episodic Memory (retrieval over real transitions), Semantic Memory (persistent
  rules from prediction-vs-observation mismatches), Selective Foresight (drop
  low-confidence predictions before they reach the agent). ([arXiv 2606.30639](https://arxiv.org/abs/2606.30639))
- **ProPlay** (Jun 2026) — **procedural world models for self-evolving agents**:
  abstract successful trajectories into procedures, organize them in a
  causal-transition **procedure graph**, improve through interaction with no external
  supervision in partially observable environments. ([arXiv 2606.12780](https://arxiv.org/abs/2606.12780))

The 2026 move is the important one for us: **the thing being improved by self-play
is increasingly the *world model itself*, not just the policy.** Agents improve by
*anticipating* outcomes under candidate actions against a learned model — self-play
and [world models](01-world-models.md) collapsing into one loop.

## 4. Open problems

- **Mechanisms are poorly understood.** Self-play shows strong in- and out-of-domain
  gains, but *why* is still unclear ("Towards Understanding Self-Play for LLM
  Reasoning," [arXiv 2510.27072](https://arxiv.org/html/2510.27072v1)).
- **The plateau isn't gone.** SGS raises the ceiling; it doesn't remove it. Nobody
  is at 100%.
- **Guide reward-hacking.** A learned judge is itself gameable; the guide can be
  fooled just as the solver can.
- **Grounding at scale.** SGS grounds in a fixed target set. Where does the *initial*
  distribution come from when there's no problem bank?

## 5. Implication for our work

The SGS pattern is a **direct blueprint** for any self-improving pipeline we build —
above all a strategy-synthesis or alpha-factory layer in Hermes (a private
trading-research repo of ours),
and self-play over [Oneiros](06-oneiros-positioning.md) rollouts:

> The failure you would hit generating synthetic trading strategies is *exactly*
> "tricky ≠ useful": a generator that drifts toward complex-but-worthless strategies
> that beat a backtest by overfitting noise. The fix is the same — **ground synthetic
> strategies in a real target distribution and gate them with a judge.** Hermes'
> **DSR-gate is already a primitive "guide."** Formalizing it as an SGS-style
> `reward = edge × guide-score` is a concrete upgrade.

The runnable demo in [`../demos/self-play/`](../demos/self-play/) makes the whole
pattern legible in a toy setting first.

---

*Prev: [01 · World models](01-world-models.md) · Next: [03 · Continual learning →](03-continual-learning.md)*
