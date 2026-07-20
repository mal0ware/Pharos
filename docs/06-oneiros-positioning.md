# 06 · Oneiros positioning

> A learned latent world model an agent plans with, exposed over MCP.

This is the "so what" doc: where our own world-model project sits inside the 2026
frontier, and where it should head.

> ✅ **Repo pulled & assessed (2026-07).** Oneiros is cloned locally and read. It is
> **not** an idea or a stub — it's a **complete, verified v0.1.0 research artifact**.
> §6 below is written from the actual code.

---

## 1. What Oneiros is, in one breath

A normal LLM predicts the next **word**. Oneiros predicts the next **state of the
world** — it holds a compressed internal model of a domain and can roll it forward
("if I do X, what happens?") so an agent can **plan against imagined futures instead
of guessing**. And it's delivered as an **MCP tool**, so *any* agent can call it.

That is the [V-JEPA 2](01-world-models.md) premise (a learned latent world model an
agent plans with) — packaged as infrastructure rather than an end-to-end product.

## 2. Where it sits in the 2026 race

The [world-models race](01-world-models.md) has three big players building
**products**: AMI Labs (abstract JEPA reasoning), World Labs (renderable 3D), and
DeepMind (interactive generative worlds). **None of them ships a plannable world
model as a callable tool over MCP.** That's the wedge:

| | AMI / World Labs / DeepMind | **Oneiros** |
|---|---|---|
| Form | End-to-end product / model | **Tool over MCP** any agent can call |
| User | Their own stack | **Arbitrary external agents** |
| Bet | Win the model | Win the **integration** |

Oneiros doesn't need to beat AMI Labs at building the best world model. It needs to
be the **easiest way for an agent to plan against one.** That's a distribution and
interface play, and it's uncontested.

## 3. The frontier hands us a spec

Three 2026 results are directly load-bearing for the design:

1. **LeJEPA identifiability** ([01](01-world-models.md)) — the conditions under which a
   JEPA learns a *faithful* latent world model (Gaussian latents, stable dynamics →
   linearly identifiable → **optimal latent-space planning**). These are **design
   constraints for Oneiros' latent space**, not abstract theory.
2. **WorldEvolver / ProPlay** ([02](02-self-play.md)) — how a world model *improves
   itself* through interaction while weights stay frozen (episodic + semantic memory +
   selective foresight). A ready-made architecture for Oneiros' learning loop.
3. **World models earned a formal proof** ([04](04-verified-intelligence.md)) — treat
   the identifiability conditions as a **spec you can verify**, not hope holds.

## 4. Proposed architecture (v0 sketch — validate against the real repo)

```
                ┌──────────────────────────────────────────────┐
   observations │                  ONEIROS                       │
   ────────────▶│  ┌──────────┐   ┌───────────┐   ┌───────────┐ │
                │  │ Encoder  │──▶│  Latent   │──▶│ Predictor │ │  latent
   action a ───▶│  │ (JEPA)   │   │  state z  │   │ z' = f(z,a)│─┼─▶ rollout
                │  └──────────┘   └───────────┘   └───────────┘ │
                │        ▲              │  self-evolving memory  │
                │        └──────────────┴── (episodic/semantic)  │
                └───────────────────────────────┬────────────────┘
                                                │  MCP surface
                        tools: encode() · rollout(z, actions) · plan(goal) · why()
```

- **Encoder** — JEPA-style, maps observations → latent `z` (predict in latent space).
- **Predictor** — `z' = f(z, a)`: the forward model an agent plans with. Recurrent/
  looped head → a test-time-compute lever ([more loops = better](01-world-models.md)).
- **Self-evolving memory** — WorldEvolver's three modules keep the model current
  without weight updates ([03](03-continual-learning.md)).
- **MCP surface** — `encode`, `rollout`, `plan`, and a `why`/introspection call so
  the calling agent can audit the plan.

## 5. Roadmap (proposed — sequence, not dates)

> Per [05](05-applied-frontiers.md): don't ask an agent for time estimates. Sequence
> and ship.

1. **Clone & assess.** Get the real repo local; rewrite §6 from actual code.
2. **Pick a bounded domain.** A world model needs a world. Start with a *small,
   fully-observable* one where rollouts are cheap and checkable (a grid/game, or —
   on-brand — a toy market microstructure tied to Hermes, a private
   trading-research repo of ours). Resist
   starting with "the world."
3. **Latent encoder + forward predictor** in that domain; validate against the
   [identifiability](01-world-models.md) checklist.
4. **Planning loop** — search over `rollout()` to reach a goal; this is the payoff
   that distinguishes a world model from a predictor.
5. **MCP surface** — expose `encode/rollout/plan/why`; now any agent can use it. This
   is the distribution wedge and the thing nobody else ships.
6. **Self-play over rollouts** — improve the model via [SGS-style](02-self-play.md)
   self-generated scenarios, grounded + guide-gated to avoid "tricky ≠ useful."
7. **Verify** — encode the world model's required properties as checkable specs ([04](04-verified-intelligence.md)).

The **[self-play demo](../demos/self-play/)** is deliberately step 6 in miniature,
built first in a toy setting so the pattern is legible before Oneiros needs it.

## 6. Current state — v0.1.0 (last commit 3 weeks ago, ~1,284 LOC, CPU-only)

**Further along than expected. It's a genuine, end-to-end, verified proof-of-concept —
the whole loop exists and works.**

What's **built and working**:

- **Environment** — deterministic 2D point-mass (`env.py`).
- **JEPA world model** (`model.py`) — encoder `f` + predictor `g`, **no decoder, no
  pixel loss**. Anti-collapse done properly: **EMA target encoder + stop-gradient +
  VICReg variance/covariance** penalty. This is the real JEPA recipe, not a sketch.
- **Latent-space MPC planner** (`planner.py`) — cross-entropy method rolling `g`
  forward `H` steps, receding-horizon replanning.
- **MCP surface** (`mcp_server.py`) — `encode_observation`, `predict_rollout`,
  `plan_to_goal`, `reset_env`/`step_env`. The distribution wedge is **already shipped**:
  an agent plans by calling the world model as a tool.
- **Trained checkpoint committed** (~240 KB); trains in ~21s.
- **Tests = three "honesty gates"** (`tests/test_gates.py`), all passing:
  (a) predictor beats no-op identity baseline **0.0185 vs 0.1076 (~5.8×)**;
  (b) latent not collapsed (per-dim std **1.04**, threshold 0.1);
  (c) MPC beats random **95% vs 15–20%** goal-reaching over 20 seeds.

What's **honestly limited** (stated in the README, not hidden):

- Toy 2D env; tiny models; latent dynamics nearly linear.
- Default obs is **vector-state**, not image. The **image CNN encoder trains without
  collapse but doesn't beat the identity baseline** here — consecutive 32×32 frames
  barely change, so "predict no change" is already near-optimal and there's no margin
  to prove learned dynamics. This is documented as the next problem, not papered over.

**Nearest runnable milestone / documented next step:** image-based perception via a
**frozen pretrained encoder ([V-JEPA 2](01-world-models.md)) + a learned latent
dynamics head** — exactly the scale-up recipe this toy mirrors.

**The Hermes tie is already written** — see that (private) repo's `SYNERGY.md`: an
HMM market regime *is* a discrete-latent world model (encoder = filtering, predictor =
transition matrix), and the extension is a **continuous JEPA-style regime dynamics
model** — predict the decision-relevant latent regime, not the next tick, and apply the
same three honesty gates before trusting it.

### Revised roadmap (grounded in the real repo)

The v0 sketch in §5 was close. Given what actually exists, the live sequence is:

1. ~~Clone & assess~~ ✅ done.
2. **Harden the win.** The point-mass loop is proven — lock it with CI (the repo has a
   `ci.yml`) so the honesty gates guard every change.
3. **Break the image barrier** — swap the toy CNN for a **frozen V-JEPA 2 encoder +
   learned dynamics head** on a slightly richer env where frames actually change. This
   is the single highest-value next step and it's already the documented one.
4. **Grow the action/goal space** — richer planning tasks to stress the MPC.
5. **Self-play over rollouts** — the [SGS pattern](02-self-play.md) / the
   [demo](../demos/self-play/), grounded + guide-gated.
6. **Sharpen the MCP surface** — add a `why()`/introspection tool so a calling agent
   can audit a plan; this deepens the wedge nobody else is building.
7. **Bridge to Hermes** — prototype the `SYNERGY.md` continuous-regime model as a real
   experiment.

---

*Prev: [05 · Applied frontiers](05-applied-frontiers.md) · Back to [README](../README.md)*
