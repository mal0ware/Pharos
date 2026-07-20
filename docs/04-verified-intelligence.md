# 04 · Verified intelligence

> You cannot fool the kernel. Formal proof as ground truth — for math *and* code.

This is the correctness layer of the [meta-thesis](00-thesis.md): the tightest
possible feedback loop, because the signal (does the proof check?) is
machine-verified and unfoolable.

---

## 1. Why now

Informal math is handwavy — "proof by intimidation," steps left implicit. **Lean**
(and Coq, Isabelle) is fully explicit and machine-checkable: the kernel accepts a
proof or it doesn't, and **you cannot fool it**. That property — a verifier that
can't be gamed — is precisely what a self-improving loop needs, which is why formal
methods and RL are converging.

Lean is not just a theorem prover. It's a **fast functional programming language**
with metaprogramming, macros, custom automation, and an FFI (CUDA bindings). Proofs
and programs unify. **Mathlib** is its enormous, high-quality math library (topology
to algebraic geometry, millions of lines).

## 2. The 2026 breakthroughs (this moved fast)

- **AlphaProof's successor** solved **nine open Erdős problems** in **May 2026**, two
  unsolved for **50+ years**, using **formal verification in the loop**.
- **AlphaProof Nexus** (Tsoukalas et al., 2026) — an **evolutionary Lean proof-search
  system**: prover subagents edit marked regions of Lean sketches, call AlphaProof on
  subgoals, validate candidates, and use rater agents + a population database to pick
  promising sketches. Resolved **492 OEIS conjectures**.
- **Harmonic's Aristotle** — fine-tuned proof-search + MCTS + an informal-reasoning
  pipeline; **IMO 2025 gold**, with a public API.
- **Axiom Math** — solved **all 12 Putnam 2025** problems (perfect score) and raised
  **$200M at $1.6B** (Mar 2026) explicitly to take the guarantee **from math into
  code**.
- **Math Inc.** formalized the **strong Prime Number Theorem** in Lean in **three
  weeks** — a task that had stalled after 18+ months of human effort.

The underlying engine is **AlphaZero-style**: AlphaProof learns to find formal proofs
by RL over **millions of auto-formalized problems** — i.e. [self-play](02-self-play.md)
with an unfoolable verifier as the reward. Formal verification is the *ideal*
self-play reward: it can't be reward-hacked.
([CACM](https://cacm.acm.org/research/formal-reasoning-meets-llms-toward-ai-for-mathematics-and-verification/),
[Nature](https://www.nature.com/articles/s41586-025-09833-y),
[LeanMarathon, arXiv 2606.05400](https://arxiv.org/html/2606.05400))

## 3. From math to code (the part that matters for builders)

The frontier is extending verification from theorems to **programs and science**.
Program verification = **spec + code + a proof that the code meets the spec.** The
rallying line, from the Lean-for-science talk and echoed by Tegmark:

> **Verifiable coding beats vibe coding.**

- **Bridge** — uses Lean-as-a-language to elicit better *verified* code from LLMs.
- **Torch** — the first framework for writing **neural nets natively in Lean**:
  PyTorch-style tensors compiling to a shared IR, **verified floating-point
  arithmetic**, provable properties (e.g. FlashAttention ≡ standard attention at the
  spec level; attention permutation-invariance without positional encodings). It even
  formalizes the **temperature-0 nondeterminism** result down toward the CUDA kernel —
  showing tiny float errors can flip the final argmax.
- **VerifiedCoding / CSL** (Clark Barrett's group, Stanford) — a growing library for
  contributing verified-code concepts.
- **Leanstral** (Mistral) — productized "prove your code is correct."

The spectrum of tools, low-effort/low-expressivity → high-effort/high-expressivity:
**SMT solvers** (automatic, limited) → **interactive provers** (Lean/Coq/Isabelle,
expressive, more human effort). LLMs are increasingly the glue that makes the
high-expressivity end usable.

## 4. Open problems

- **Autoformalization is the bottleneck.** Turning informal intent/spec into a
  correct formal statement is still hard and error-prone (LeanMarathon exists to
  measure long-horizon autoformalization).
- **Coverage.** Verified code is real but narrow; most software has no formal spec.
- **Human intent capture.** A proof that code meets a *wrong* spec is worthless. The
  spec is where human judgment stays essential.

## 5. Implication for our work

This speaks directly to a correctness-first instinct:

- **Hermes** (a private trading-research repo of ours) — the risk-advisory invariants and the **DSR-promotion
  logic** (deciding when a strategy earns live capital) are exactly the kind of
  hot-path where "looks right" must become "is right." Full Lean proof may be
  overkill, but the *framing* — **spec + implementation + a machine-checkable proof
  the implementation meets the spec** — is the right one. At minimum: encode the DSR
  gate's invariants as property-based tests (the poor man's formal spec).
- **[Oneiros](06-oneiros-positioning.md)** — LeCun's world model literally "earned a
  formal proof" (the [LeJEPA identifiability](01-world-models.md) conditions). Treat
  those conditions as a *spec* the latent space must satisfy, and you can verify
  properties of the world model rather than hoping they hold.
- **General:** anywhere a self-play loop needs a reward, ask whether a **verifier**
  can replace a **learned judge**. Verifiers can't be reward-hacked; judges can.

---

*Prev: [03 · Continual learning](03-continual-learning.md) · Next: [05 · Applied frontiers →](05-applied-frontiers.md)*
