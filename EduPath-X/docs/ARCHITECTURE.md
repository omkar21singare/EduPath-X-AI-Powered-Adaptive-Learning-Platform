# EduPath-X — System Architecture Document

## 1. High-Level Architecture Overview

EduPath-X is built using a decoupled, reactive client-server architecture designed for high throughput, real-time Bayesian Knowledge Tracing (BKT), dynamic recommendation generation, and event-driven timeline simulation.

```
+-------------------------------------------------------------------------------+
|                               REACT FRONTEND                                  |
|   (Vite + TypeScript + Tailwind CSS + Recharts + Interactive SVG DAG Graph)   |
+-------------------------------------------------------------------------------+
                                       │
                                       │ HTTP / REST API (FastAPI)
                                       ▼
+-------------------------------------------------------------------------------+
|                              FASTAPI BACKEND                                  |
|  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────────────┐   |
|  │ Auth & Learner   │   │ Content & Quiz   │   │ Dashboard & Progress     │   |
|  │ API              │   │ Engine           │   │ Analytics API            │   |
|  └────────┬─────────┘   └────────┬─────────┘   └────────────┬─────────────┘   |
|           │                      │                          │                 |
|           ▼                      ▼                          ▼                 |
|  ┌─────────────────────────────────────────────────────────────────────────┐  |
|  │                          CORE ADAPTIVE ENGINES                          │  |
|  │  ┌────────────────────┐ ┌────────────────────┐ ┌─────────────────────┐  │  |
|  │  │ Bayesian Knowledge │ │ Retention Decay    │ │ Adaptive            │  │  |
|  │  │ Tracing (BKT)      │ │ Model (exp decay)  │ │ Recommendation      │  │  |
|  │  └────────────────────┘ └────────────────────┘ └─────────────────────┘  │  |
|  │  ┌────────────────────┐ ┌────────────────────┐                          │  |
|  │  │ Learner Timeline   │ │ Adaptive vs Fixed  │                          │  |
|  │  │ Simulator          │ │ Evaluation Engine  │                          │  |
|  │  └────────────────────┘ └────────────────────┘                          │  |
|  └───────────────────────────────────┬─────────────────────────────────────┘  |
+--------------------------------------│----------------------------------------+
                                       │
                                       ▼
+-------------------------------------------------------------------------------+
|                           PERSISTENCE LAYER                                   |
|               (SQLite / PostgreSQL ORM via SQLAlchemy 2.0)                    |
+-------------------------------------------------------------------------------+
```

---

## 2. Central Adaptive Data Flow

```
[ Learner Interaction ] ──> [ Question Attempt Recorded ]
                                       │
                                       ▼
                       [ BKT State Update Math Executed ]
                       (Prior P_t-1 -> Posterior P_t)
                                       │
                                       ▼
                       [ KnowledgeState & Audit History Saved ]
                                       │
                                       ▼
                  [ Prerequisite DAG Satisfaction Re-evaluated ]
                                       │
                                       ▼
                [ Adaptive Recommendation Generated w/ Evidence ]
                                       │
                                       ▼
                    [ Dashboard & Knowledge Map UI Refreshed ]
```

---

## 3. Directory Structure

```
EduPath-X/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI Endpoint Routers
│   │   ├── database/        # DB Session & Seed Data
│   │   ├── evaluation/      # Scientific Evaluation Engine
│   │   ├── ml/              # BKT, Retention & Recommendation Engines
│   │   ├── models/          # SQLAlchemy Database Models
│   │   ├── schemas/         # Pydantic Schemas
│   │   ├── simulation/      # Learner Profile Simulator
│   │   └── main.py          # FastAPI Application Setup
│   ├── tests/               # Pytest Test Suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Dashboard Widgets, Graph & Modals
│   │   ├── services/        # Axios API Client
│   │   ├── types/           # TypeScript Type Definitions
│   │   └── App.tsx          # Main React Application
│   └── package.json
└── docs/                    # Architecture & ML Documentation
```
