# 00 · The meta-thesis

> The tools keep changing. The invariant is the feedback loop.

## The observation

Across the five areas this repo tracks, the same pattern recurs so consistently it
is worth stating as a law:

> **Durable progress in 2026 comes from building a better feedback loop, not from
> adding parameters. Whoever closes the loop tighter — self-play, formal
> verification, world-model rollouts, continual learning — wins the domain.**

This was said out loud at YC Paper Club (June 2026): five talks on wildly different
subjects — protein biology, LLM self-play, streaming RAG, Lean, agentic coding —
all circled back to the same idea. The subject changes; the challenge is always
*how do you learn reliably from each new step.*

## Why scale alone stopped being the story

The scaling era was real and is not over — scaling laws still hold, including in
[biology](05-applied-frontiers.md) and [protein models](05-applied-frontiers.md).
But three walls came into view at once:

1. **The data wall.** Pretraining is running out of fresh human tokens. RL
   post-training now rivals *or exceeds* pretraining compute, but RL tasks are
   **hand-collected on a log scale** — you run out of humans to write problems long
   before the model runs out of capacity to learn. ([Self-play](02-self-play.md).)

2. **The human-subspace ceiling.** If you only train on human-generated solutions
   (call it subspace **H**), no feasible amount of test-time compute or recursive
   self-improvement reliably samples the rest of the solution space (**F − H**).
   AlphaGo (human-biased) vs AlphaZero (self-play, unbiased) is the proof that
   *removing* the human prior is what broke past superhuman play. To go beyond
   human data you need a loop that generates its own signal.

3. **The static-weights ceiling.** A human who plays 10,000 games keeps improving on
   the same algorithm. An LLM's weights freeze at training time; in-context learning
   does **not** improve monotonically with more examples — it wobbles, then hits the
   context-length cliff and stops. "Intelligence per sample" and "intelligence per
   watt" are the two open problems that scaling does not touch.
   ([Continual learning](03-continual-learning.md).)

## The convergence

Each area is a different way to close a loop that scaling leaves open:

```
                    ┌─────────────────────────────────────────┐
                    │      THE LOOP scaling can't close         │
                    └─────────────────────────────────────────┘
                                     │
   ┌──────────────┬──────────────────┼──────────────────┬──────────────┐
   ▼              ▼                  ▼                  ▼              ▼
WORLD MODELS   SELF-PLAY       CONTINUAL          VERIFIED        APPLIED
(01)           (02)            LEARNING (03)      INTEL. (04)     (05)

predict the    generate your   keep learning      prove the       same recipe,
world in       own tasks &     after training,    output is       new domains
latent space,  solve them,     without            correct,        (biology,
plan against   improve past    forgetting         machine-        engineering)
it             human data                          checkable
```

The endgame they're all reaching toward is the same system:

> **an agent that (a) holds an internal model of a domain, (b) improves that model
> and itself by acting against it, and (c) can verify it got the answer right.**

That is not five programs. It is one. **[Oneiros](06-oneiros-positioning.md)** — a
learned latent world model an agent plans with — is our attempt to sit at the
center of it: (a) is the world model, (b) is self-play over its rollouts, (c) is the
verification layer.

## What this means for how we build

- **Instrument the loop first.** Before optimizing a model, ask what signal it
  learns from and how tight that loop is. A mediocre model in a tight verified loop
  beats a strong model in a loose one.
- **Prefer self-generated signal where it's safe.** Anywhere you're hand-writing
  training tasks or eval cases, ask whether the system can generate and grade its
  own — with a guard against the [degeneracy failure mode](02-self-play.md).
- **Make correctness checkable, not vibed.** Where an output has a spec, encode the
  spec. [Verified intelligence](04-verified-intelligence.md) is the discipline that
  turns "looks right" into "is right."

---

*Next: [01 · World models & JEPA →](01-world-models.md)*
