# Demo · Self-play, and why "tricky ≠ useful"

The first working exhibit of [Pharos](../../README.md). A **zero-dependency**,
runnable simulation of asymmetric self-play that reproduces the central result of
[*Scaling Self-Play with Self-Guidance* (SGS)](../../docs/02-self-play.md):

> Naive self-play **plateaus** — the conjecturer learns to generate tricky-but-useless
> problems. Self-**guided** self-play keeps **climbing**.

## Run it

```bash
python3 selfplay_demo.py
```

No installs. Pure Python standard library. ~1 second.

## What you'll see

```
  NAIVE self-play   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄...
    start=0.38  ->  end=0.38   (mean problem complexity generated: 7.7)   ← PLATEAU

  SGS  self-guided  ▄▄▄▅▅▆▆▆▆▇▇▇▇▇▇▇▇▇█████████████████████████...
    start=0.38  ->  end=0.99   (mean problem complexity generated: 1.4)   ← CLIMBS
```

Two things to notice:

1. **The curves.** Naive self-play flatlines; SGS rises to near-mastery on the *real*
   target distribution. Same solver, same compute — only the **conjecturer's reward**
   differs.
2. **The complexity gap.** Naive inflates problem complexity (~7.7) to stump the
   solver; SGS keeps it low (~1.4). That *is* "tricky ≠ useful" made visible: the
   naive conjecturer wins its reward by producing degenerate junk that teaches
   nothing.

## How it maps to the paper

This is a toy on purpose — no neural net, no LLM. The mechanism is what matters.

| Paper concept | In this demo |
|---------------|--------------|
| **Solver** | a scalar `skill` (competence on the target distribution) |
| **Conjecturer** | a search that picks the `BATCH` problems maximizing its reward |
| **Task** | a `(concept c, complexity k)` pair |
| **Naive reward** | `1 − p_solve` — pure trickiness (stump the solver) |
| **SGS reward** | `trickiness × guide`, where `guide = grounding(c) × simplicity(k)` |
| **"Grounded in a real target"** | `transfer(c)` — only on-distribution problems improve target competence |
| **The guide/judge** | the `guide` term penalizing off-distribution + needlessly complex problems |
| **"Learn at the frontier"** | `frontier(p) = 4p(1−p)` — max learning when `p_solve ≈ 0.5` |
| **Held-out eval** | `held_out_competence()` — solve-rate on canonical target problems |

The key modeling choice that makes the lesson bite: a problem only improves the
solver's *real* competence when it is **both on-distribution (transfers) and at the
frontier (useful difficulty)**. Naive self-play satisfies neither; SGS is designed to
satisfy both.

## Why this is the first exhibit

It's [Oneiros'](../../docs/06-oneiros-positioning.md) step 6 in miniature. When
Oneiros improves its world model via self-generated scenarios, this is the exact
failure it must avoid — and the exact fix. It's also the pattern for a
strategy-synthesis layer in Hermes (a private trading-research repo of ours): a generator that drifts toward
complex-but-worthless strategies (overfitting a backtest) is "tricky ≠ useful," and
the DSR-gate is already a primitive **guide**. Formalize it as
`reward = edge × guide_score` and you have SGS for trading strategies.

## Knobs

Edit the constants at the top of `selfplay_demo.py`:

- `TARGETS` — the real concept distribution you care about.
- `GUIDE_LAMBDA` — how hard the guide penalizes needless complexity. Set it to `0`
  and watch SGS degrade toward naive.
- `TRANSFER_WIDTH` — how quickly off-distribution training stops helping.
- `ROUNDS`, `CANDIDATES`, `BATCH` — compute knobs.

Try `GUIDE_LAMBDA = 0.0` first — it's the cleanest way to see the guide is what's
doing the work.

## Output

Writes `results.csv` (`round, naive, sgs`) for plotting. It is intentionally
**not committed** (see `.gitignore`): the demo is seeded and regenerates the exact
same file deterministically in well under a second — just run the script.

---

*Back to [Pharos](../../README.md) · concept: [02 · Self-play](../../docs/02-self-play.md)*
