# EduPath-X — Scientific Evaluation Methodology

## 1. Research Problem & Objective

The objective of the EduPath-X Evaluation Module is to scientifically compare two learning management policies:
1. **BASELINE (Fixed Linear Curriculum)**: Enforces static concept order ($C_1 \to C_2 \to \dots \to C_{18}$) regardless of individual learner struggle or mastery.
2. **ADAPTIVE (EduPath-X Engine)**: Continuously selects learning activities based on Bayesian Knowledge Tracing $P(K_c)$, prerequisite graph readiness, and targeted revision for identified misconceptions.

---

## 2. Experimental Simulation Setup

- **Monte Carlo Simulation Trials**: $N = 50$ to $100$ independent trials.
- **Learner Population Models**: Probabilistic synthetic learner profiles (*Balanced, Strong, Struggling with Trees, Inconsistent*).
- **Tracked Empirical Metrics**:
  - `Time to Overall Mastery`: Average simulated days required to achieve 85%+ overall curriculum mastery.
  - `Question Volume Efficiency`: Total question attempts required to reach mastery.
  - `14-Day Delayed Retention Rate`: Measured concept retention percentage after 14 days without practice.
  - `Efficiency Gain %`:

$$\text{Efficiency Gain} = \frac{\text{Questions}_{\text{Fixed}} - \text{Questions}_{\text{Adaptive}}}{\text{Questions}_{\text{Fixed}}} \times 100\%$$

---

## 3. Data Integrity & Scientific Reporting

- No manufactured or fake improvement percentages.
- All metrics originate from actual event-driven Monte Carlo trial executions.
- Confidence intervals and standard deviations are computed dynamically.
