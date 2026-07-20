#!/usr/bin/env python3
"""
selfplay_demo.py — the "tricky != useful" lesson, made runnable.

A minimal, zero-dependency simulation of asymmetric self-play (conjecturer +
solver + guide) that reproduces the central result from *Scaling Self-Play with
Self-Guidance* (SGS): naive self-play PLATEAUS because the conjecturer learns to
generate tricky-but-useless problems, while self-GUIDED self-play keeps improving.

It is a toy on purpose. There is no neural net and no LLM — the "solver" is a
scalar competence and the "conjecturer" is a search over candidate problems that
maximizes its reward. That is enough to expose the *dynamics* the paper is about,
which is the point of a demo: make the mechanism legible before you scale it.

Run:   python3 selfplay_demo.py
No dependencies beyond the Python standard library.

See README.md in this folder for the mapping back to the paper and to Oneiros.
"""

import math
import random

# ─────────────────────────────── world constants ──────────────────────────────
random.seed(7)

TARGETS = [0.30, 0.65]     # the "real" concept distribution we ultimately care about
TRANSFER_WIDTH = 0.02      # how quickly training-transfer decays off the target concepts
FRONTIER_SHARP = 1.0       # learning is maximal when p_solve ~ 0.5 (the frontier)
LR = 0.06                  # solver learning rate per round
DIFF_SLOPE = 6.0           # sigmoid sharpness: p_solve = sigmoid(SLOPE*(skill - difficulty))
K_DIFF = 0.18              # each extra complexity step adds this much difficulty
OFFTARGET_DIFF = 1.2       # difficulty added for being far from any target concept
GUIDE_LAMBDA = 1.3         # SGS guide penalty on needless complexity
ROUNDS = 60
CANDIDATES = 240           # problems the conjecturer searches over each round
BATCH = 32                 # problems the solver trains on each round


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def nearest_target_dist(c: float) -> float:
    return min(abs(c - t) for t in TARGETS)


def transfer(c: float) -> float:
    """How much training on concept c improves competence on the TARGET distribution.
    Off-distribution problems teach the solver ~nothing about what we care about."""
    d = nearest_target_dist(c)
    return math.exp(-(d * d) / TRANSFER_WIDTH)


def difficulty(c: float, k: int) -> float:
    """Harder if far from a target concept, and harder with each complexity step."""
    return OFFTARGET_DIFF * nearest_target_dist(c) + K_DIFF * (k - 1)


def p_solve(skill: float, c: float, k: int) -> float:
    return sigmoid(DIFF_SLOPE * (skill - difficulty(c, k)))


def frontier(p: float) -> float:
    """You learn most at the FRONTIER of your ability (p~0.5), little from
    trivial (p~1) or impossible (p~0) problems."""
    return (4.0 * p * (1.0 - p)) ** FRONTIER_SHARP


def learn_gain(skill: float, c: float, k: int) -> float:
    """Actual competence gained by training on this problem: only when it both
    TRANSFERS (on-distribution) and sits at the solver's FRONTIER (useful difficulty)."""
    p = p_solve(skill, c, k)
    return LR * transfer(c) * frontier(p)


# ─────────────────────────────── conjecturers ─────────────────────────────────
def sample_candidate():
    c = random.random()               # concept anywhere in [0,1]
    k = random.randint(1, 8)          # complexity 1..8
    return c, k


def reward_naive(skill, c, k):
    """Naive self-play: reward the conjecturer purely for stumping the solver.
    The easy way to win is to crank difficulty -> degenerate, off-frontier junk."""
    return 1.0 - p_solve(skill, c, k)


def reward_sgs(skill, c, k):
    """Self-guided: reward = trickiness x guide.
       trickiness wants a hard-ish problem; the GUIDE demands it be grounded in the
       target distribution AND not needlessly complex."""
    trickiness = 1.0 - p_solve(skill, c, k)
    guide = transfer(c) * math.exp(-GUIDE_LAMBDA * (k - 1))
    return trickiness * guide


def conjecture_batch(skill, reward_fn):
    """Stand-in for a trained conjecturer: search candidates, keep the best BATCH
    by the conjecturer's own reward."""
    cands = [sample_candidate() for _ in range(CANDIDATES)]
    cands.sort(key=lambda ck: reward_fn(skill, ck[0], ck[1]), reverse=True)
    return cands[:BATCH]


# ─────────────────────────────── evaluation ───────────────────────────────────
def held_out_competence(skill: float) -> float:
    """The number that actually matters: solve-rate on the REAL target distribution
    (canonical low-complexity problems on the target concepts)."""
    probs = [(t, k) for t in TARGETS for k in (1, 2)]
    return sum(p_solve(skill, c, k) for c, k in probs) / len(probs)


def run(reward_fn):
    skill = 0.0
    curve = [held_out_competence(skill)]
    mean_k = []
    for _ in range(ROUNDS):
        batch = conjecture_batch(skill, reward_fn)
        gains = [learn_gain(skill, c, k) for c, k in batch]
        skill += sum(gains) / len(gains)
        curve.append(held_out_competence(skill))
        mean_k.append(sum(k for _, k in batch) / len(batch))
    return curve, (sum(mean_k) / len(mean_k))


# ─────────────────────────────── presentation ─────────────────────────────────
BLOCKS = "▁▂▃▄▅▆▇█"


def sparkline(xs):
    lo, hi = 0.0, 1.0
    out = []
    for x in xs:
        i = int((x - lo) / (hi - lo) * (len(BLOCKS) - 1) + 0.5)
        out.append(BLOCKS[max(0, min(len(BLOCKS) - 1, i))])
    return "".join(out)


def main():
    naive_curve, naive_k = run(reward_naive)
    sgs_curve, sgs_k = run(reward_sgs)

    print("=" * 72)
    print("  SELF-PLAY: tricky != useful   (held-out competence on the REAL target)")
    print("=" * 72)
    print(f"  rounds={ROUNDS}  candidates/round={CANDIDATES}  batch={BATCH}\n")

    print(f"  NAIVE self-play   {sparkline(naive_curve)}")
    print(f"    start={naive_curve[0]:.2f}  ->  end={naive_curve[-1]:.2f}"
          f"   (mean problem complexity generated: {naive_k:.1f})")
    print(f"    the conjecturer chases difficulty, drifts off-distribution/off-frontier,")
    print(f"    and the solver learns almost nothing useful -> PLATEAU.\n")

    print(f"  SGS  self-guided  {sparkline(sgs_curve)}")
    print(f"    start={sgs_curve[0]:.2f}  ->  end={sgs_curve[-1]:.2f}"
          f"   (mean problem complexity generated: {sgs_k:.1f})")
    print(f"    grounded in the target distribution + guide-gated on complexity ->")
    print(f"    problems land at the solver's frontier -> competence CLIMBS.\n")

    lift = sgs_curve[-1] - naive_curve[-1]
    print("-" * 72)
    print(f"  SGS beats naive by {lift:+.2f} held-out competence "
          f"({sgs_curve[-1]/max(naive_curve[-1],1e-9):.1f}x).")
    print(f"  Note the complexity gap: naive inflates it ({naive_k:.1f}) to stump the")
    print(f"  solver; SGS keeps it low ({sgs_k:.1f}) because tricky != useful.")
    print("-" * 72)

    # machine-readable output for anyone who wants to plot it
    try:
        with open("results.csv", "w") as f:
            f.write("round,naive,sgs\n")
            for i, (n, s) in enumerate(zip(naive_curve, sgs_curve)):
                f.write(f"{i},{n:.4f},{s:.4f}\n")
        print("  wrote results.csv")
    except OSError:
        pass


if __name__ == "__main__":
    main()
