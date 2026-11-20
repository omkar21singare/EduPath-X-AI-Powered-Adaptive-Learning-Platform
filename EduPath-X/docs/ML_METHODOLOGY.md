# EduPath-X — Machine Learning & Adaptive Methodology

## 1. Bayesian Knowledge Tracing (BKT) Engine

EduPath-X employs standard Bayesian Knowledge Tracing (BKT) to continuously model a learner's latent knowledge state $P(K_c)$ for each concept $c$ in the curriculum graph.

### Core Parameters
- $P(L_0)$: Initial prior probability of knowing concept (Default: 0.20)
- $P(T)$: Probability of transitioning from unlearned to learned state after an attempt (Default: 0.15)
- $P(S)$: Slip probability — wrong response despite knowing concept (Default: 0.10)
- $P(G)$: Guess probability — correct response despite not knowing concept (Default: 0.25)

### Mathematical Formulations

#### 1. Observation Update (Bayes' Rule)
Given an observed response $y \in \{0, 1\}$ (0 = incorrect, 1 = correct):

If $y = 1$ (Correct):
$$P(L_{t | y=1}) = \frac{P(L_{t-1}) \cdot (1 - P(S))}{P(L_{t-1}) \cdot (1 - P(S)) + (1 - P(L_{t-1})) \cdot P(G)}$$

If $y = 0$ (Incorrect):
$$P(L_{t | y=0}) = \frac{P(L_{t-1}) \cdot P(S)}{P(L_{t-1}) \cdot P(S) + (1 - P(L_{t-1})) \cdot (1 - P(G))}$$

#### 2. Transition Update (Learning Step)
$$P(L_t) = P(L_{t | y}) + (1 - P(L_{t | y})) \cdot P(T)$$

---

## 2. Retention Decay Model

Knowledge decays over elapsed days without practice according to an exponential memory decay function:

$$P(K_t) = P(K_0) \cdot e^{-\lambda \Delta t}$$

Where:
- $\Delta t$: Elapsed days since last concept practice.
- $\lambda = 0.025$: Memory decay coefficient.

---

## 3. Dynamic Recommendation Policy

The recommendation engine evaluates concept prerequisites and state thresholds:
- **REVISE**: Triggered if $P(K) < 0.60$ and recent accuracy < 60%.
- **PRACTICE**: Triggered if $0.50 \le P(K) < 0.85$ and prerequisites satisfied.
- **LEARN**: Triggered if $P(K) < 0.40$, zero prior attempts, and all prerequisites meet threshold ($P(K_{\text{prereq}}) \ge 0.70$).
