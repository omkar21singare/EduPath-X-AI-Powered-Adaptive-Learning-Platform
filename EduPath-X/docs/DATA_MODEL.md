# EduPath-X — Data Model & Database Schema

EduPath-X uses a normalized relational schema supporting persistent learner tracking, content sourcing, audit trails, simulation, and scientific evaluation.

---

## Entity Relationship Summary

```
                      +-------------------+
                      |       User        |
                      +─────────┬─────────+
                                │ 1:1
                                ▼
                      +-------------------+
                      |  LearnerProfile   |
                      +────┬──────────┬───+
                       1:N │       1:N │
                           ▼           ▼
        +--------------------+       +--------------------+
        |   KnowledgeState   |       |  QuestionAttempt   |
        +─────────┬──────────+       +─────────┬──────────+
               1:N│                            │ N:1
                  ▼                            ▼
  +-----------------------+          +--------------------+
  | KnowledgeStateHistory |          |      Question      |
  +-----------------------+          +─────────┬──────────+
                                            N:1│
                                               ▼
                                     +--------------------+
                                     |      Concept       |
                                     +─────────┬──────────+
                                            1:N│
                                               ▼
                                     +--------------------+
                                     |ConceptPrerequisites|
                                     +--------------------+
```

---

## Core Tables

### 1. `users`
- `id` (PK, Integer)
- `email` (String, Unique)
- `password_hash` (String)
- `full_name` (String)
- `role` (String)
- `is_demo` (Boolean)

### 2. `learner_profiles`
- `id` (PK, Integer)
- `user_id` (FK -> users.id)
- `class_name` (String)
- `semester` (String)
- `streak_count` (Integer)
- `last_active_date` (String)

### 3. `concepts`
- `id` (PK, Integer)
- `code` (String, Unique) — e.g. `'DFS'`, `'TREES'`
- `title` (String)
- `description` (Text)
- `category` (String)
- `difficulty_level` (String)
- `display_order` (Integer)

### 4. `concept_prerequisites`
- `id` (PK, Integer)
- `concept_id` (FK -> concepts.id)
- `prerequisite_id` (FK -> concepts.id)
- `minimum_mastery` (Float, Default: 0.70)

### 5. `content_sources` (Registry)
- `id` (PK, Integer)
- `source_name` (String) — e.g. `'MIT OpenCourseWare 6.006'`
- `official_url` (String)
- `license` (String)
- `retrieved_at` (String)
- `status` (String) — `'VERIFIED'`

### 6. `knowledge_states`
- `id` (PK, Integer)
- `learner_id` (FK -> learner_profiles.id)
- `concept_id` (FK -> concepts.id)
- `mastery_probability` (Float, P(K))
- `total_attempts` (Integer)
- `correct_attempts` (Integer)

### 7. `knowledge_state_history`
- `id` (PK, Integer)
- `learner_id` (FK)
- `concept_id` (FK)
- `timestamp` (DateTime)
- `mastery_probability` (Float)
- `change_delta` (Float)
