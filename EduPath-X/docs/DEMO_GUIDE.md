# EduPath-X — Evaluator & Presentation Demo Guide

## 1. Executive Summary

This guide outlines how to present **EduPath-X** during a college presentation, faculty evaluation, or live demonstration. EduPath-X is a genuine adaptive learning system that estimates learner knowledge, persists user state, provides data-backed recommendations, and simulates long-term timelines.

---

## 2. Recommended 5-Minute Presentation Flow

### Phase 1: Mode A — Real Daily Learning (2 Minutes)
1. **Dashboard Inspection**: Point out that every number (68% progress, 5/17 concepts mastered, 7-day streak, 24.5 hrs learning time) originates from stored database interactions.
2. **Interactive Knowledge Map**: Click on the **Trees** node. Show that Trees is in an *In Progress* state ($P(K) = 54\%$) and **Graph Traversal (DFS)** is *Weak/Locked* because prerequisite thresholds are not yet met.
3. **Targeted Practice**: Click **"Start Practice"** on Tree Traversal.
4. **Bayesian State Update**: Answer a practice question correctly. Show the instant BKT update card displaying:
   $$\text{BKT State Update } P(K): 54\% \longrightarrow 67\% \ (+13\%)$$

### Phase 2: Mode B — Accelerated Simulation & Presentation Demo (2 Minutes)
1. **Simulation Control Bar**: Locate the Mode B header bar at the top.
2. **Profile Selection**: Select **"Struggling with Trees"**.
3. **Simulate Days**: Click **`Simulate 1 Day`** or **`+7 Days`**. Watch as the dashboard KPIs, streak, and recent activity automatically update as real synthetic attempts are generated and processed.
4. **Start Guided Demo**: Click the **`Guided Demo`** button. Step through the 8-stage interactive story demonstrating:
   - Initial weakness detection
   - Targeted revision override
   - MIT OCW source study
   - Knowledge state graph transition
   - Fast-forward 7 days

### Phase 3: Research Evaluation Engine (1 Minute)
1. **Adaptive vs Fixed Evaluation**: Click **`Evaluation Engine`**.
2. **Run Experiment**: Set `50 Trials` and click **`Run Comparative Experiment`**.
3. **Review Empirical Output**: Show the comparative efficiency gains (EduPath-X achieved target mastery ~35% faster with significantly fewer required question repetitions and higher 14-day retention).

---

## 3. Project Limitations Statement

- **Initial Scope**: DSA curriculum with 18 core graph-structured concepts.
- **Model Nature**: Bayesian Knowledge Tracing estimates probability of cognitive mastery; it is an algorithmic model estimate, not a direct measurement of human intelligence.
- **Simulated Learners**: Probabilistic learner profiles generate synthetic behavior for demo/evaluation purposes; clinical educational effectiveness requires human subject trial protocols.
