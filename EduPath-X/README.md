# EduPath-X — AI-Powered Adaptive Learning Platform

> **EduPath-X** is a production-quality, academically defensible AI-powered adaptive learning platform for Data Structures & Algorithms (DSA). It replaces rigid linear curricula with dynamic Bayesian Knowledge Tracing (BKT), continuous state estimation, data-driven recommendation explainability, simulated long-term timeline replay, and scientific evaluation engines.

---

## 🌟 Key Features

1. **Central Adaptive Learning Loop**:
   $$\text{Learn} \longrightarrow \text{Observe} \longrightarrow \text{Estimate Knowledge } P(K) \longrightarrow \text{Recommend} \longrightarrow \text{Learner Responds} \longrightarrow \text{Update State}$$
2. **Bayesian Knowledge Tracing (BKT)**: Continuous estimation of learner knowledge state $P(K_c)$ per concept. Dynamically incorporates response correctness, question difficulty, and response times.
3. **Data-Driven Recommendation Rationale**: Every recommendation provides an explicit evidence payload ("WHY THIS RECOMMENDATION?") containing recent accuracy %, prerequisite satisfaction status, attempt volume, and mistake patterns.
4. **Dual Demonstration Modes**:
   - **Mode A (Real Learning Mode)**: Daily persistence, real learning materials, verified source references, interactive quiz solver, and historical audit trail.
   - **Mode B (Accelerated Timeline Simulation)**: Simulate 1 Day, 7 Days, 30 Days, or Reset using realistic probabilistic learner profiles (*Balanced, Strong, Struggling with Trees, Inconsistent*).
5. **Interactive DAG Knowledge Map**: Visual node graph representing concept prerequisite dependencies and color-coded mastery statuses (*Mastered, In Progress, Weak, Locked*).
6. **Scientific Evaluation Engine**: Parallel Monte Carlo simulation comparing fixed linear curriculum policy against EduPath-X adaptive engine to calculate empirical efficiency gains, time-to-mastery, and retention rates.
7. **AI Learning Assistant**: Natural language query engine backed by live database/model state.
8. **Verified Educational Sources**: Explicit Source Registry featuring MIT OpenCourseWare 6.006, OpenStax, and MDN Web Docs.

---

## 🏗️ Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0, Pydantic v2, Pytest, SQLite / PostgreSQL.
- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons, Recharts.
- **ML / Algorithmic Core**: Bayesian Knowledge Tracing Engine, Retention Decay Model ($e^{-\lambda \Delta t}$), Adaptive Recommendation Engine, Policy Evaluation Simulator.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js v18+

### 1. Run Backend Server
```bash
# From workspace root
cd backend
python -m pip install -r requirements.txt
python app/database/seed_data.py
python -m uvicorn app.main:app --reload --port 8000
```
Backend API will be running at `http://localhost:8000` with Interactive Swagger docs at `http://localhost:8000/docs`.

### 2. Run Frontend Client
```bash
# Open a new terminal tab from workspace root
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 🧪 Running Automated Tests

```bash
# Run backend pytest suite
python -m pytest backend
```

---

## 📚 Documentation Index

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — System Architecture & Data Flow
- [`docs/ML_METHODOLOGY.md`](docs/ML_METHODOLOGY.md) — Bayesian Knowledge Tracing & Recommendation Mathematics
- [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) — Database Schema & ORM Entities
- [`docs/CONTENT_SOURCES.md`](docs/CONTENT_SOURCES.md) — Source Registry & Content Integrity Rules
- [`docs/EVALUATION_METHODOLOGY.md`](docs/EVALUATION_METHODOLOGY.md) — Adaptive vs Fixed Policy Evaluation Framework
- [`docs/DEMO_GUIDE.md`](docs/DEMO_GUIDE.md) — Step-by-Step Evaluator & Presentation Script
