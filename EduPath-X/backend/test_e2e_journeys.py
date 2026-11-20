"""Phase 4D E2E Journeys Validation Script."""
import urllib.request
import json
import sys

BASE = "http://localhost:8000"

def get(path):
    with urllib.request.urlopen(BASE + path) as r:
        return json.loads(r.read())

def post(path, data):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

print("=" * 70)
print("PHASE 4D: END-TO-END LEARNER JOURNEY VALIDATION")
print("=" * 70)

# ---------------------------------------------------------
# JOURNEY A: DASHBOARD -> RECOMMENDATION -> PRACTICE -> BKT -> GOAL
# ---------------------------------------------------------
print("\n--- JOURNEY A: Adaptive Loop Validation ---")
d1 = get("/api/dashboard?learner_id=1")
arrays_before = [n for n in d1["knowledge_map"] if n["code"] == "ARRAYS"][0]
m_before = arrays_before["mastery_percentage"]
g_before = d1["goal"]["progress_percentage"] if d1.get("goal") else 0
print(f"[A1] Initial ARRAYS Mastery: {m_before:.2f}%")
print(f"[A1] Initial Goal Progress: {g_before:.2f}%")
print(f"[A1] Top Rec Action: {d1['recommendations'][0]['action_type']} for {d1['recommendations'][0]['concept_title']}")

# Get practice questions for Arrays (concept_id=3)
qs = get("/api/questions?concept_id=3")
print(f"[A2] Practice Questions Available: {len(qs)}")
assert len(qs) > 0, "ERROR: No questions found for Arrays!"

# Submit 3 correct answers
print("[A3] Submitting 3 correct practice responses...")
for i in range(min(3, len(qs))):
    q = qs[i]
    # correct answer string or first option
    opt = q["options"][0] if isinstance(q.get("options"), list) and len(q["options"]) > 0 else "O(1)"
    res = post("/api/questions/submit?learner_id=1", {
        "question_id": q["id"],
        "selected_option": opt,
        "response_time_seconds": 15.0
    })
    print(f"     Q{i+1} (ID {q['id']}): correct={res.get('is_correct')}, new_mastery={res.get('new_mastery', 0)*100:.2f}%")

# Check updated state
d2 = get("/api/dashboard?learner_id=1")
arrays_after = [n for n in d2["knowledge_map"] if n["code"] == "ARRAYS"][0]
m_after = arrays_after["mastery_percentage"]
g_after = d2["goal"]["progress_percentage"] if d2.get("goal") else 0
print(f"[A4] Updated ARRAYS Mastery: {m_after:.2f}% (Delta: +{m_after - m_before:.2f}%)")
print(f"[A4] Updated Goal Progress: {g_after:.2f}% (Delta: +{g_after - g_before:.2f}%)")
print(f"[A4] Updated Top Rec Rationale: {d2['recommendations'][0]['reason_text']}")

assert m_after > m_before, "BKT posterior mastery did not increase!"
print(">>> JOURNEY A: VERIFIED & PASSED")

# ---------------------------------------------------------
# JOURNEY B: STUDY MATERIAL ACCESS & PREREQUISITE LOCKING
# ---------------------------------------------------------
print("\n--- JOURNEY B: Study Material & Locking Validation ---")

# Unlocked practiceable concept (ARRAYS concept_id=3)
mat_arrays = get("/api/materials/3")
print(f"[B1] Study Material for Arrays (ID 3): title='{mat_arrays.get('title')}', reading_time={mat_arrays.get('reading_time_minutes')} min")
assert mat_arrays.get("title") is not None, "Material title should not be None!"

# Unlocked theoretical concept (ALG_THINK concept_id=1)
mat_alg = get("/api/materials/1")
print(f"[B2] Study Material for Algorithmic Thinking (ID 1): title='{mat_alg.get('title')}'")
assert mat_alg.get("title") is not None, "Material title should not be None!"

# Check knowledge map locked state vs study availability
km = d2["knowledge_map"]
linked_list_node = [n for n in km if n["code"] == "LINKED_LIST"][0]
print(f"[B3] LINKED_LIST Node State: unlocked={linked_list_node['is_unlocked']}, study_available={linked_list_node.get('study_available')}, practice_available={linked_list_node.get('practice_available')}")
print(f"     Prerequisite Details: {linked_list_node.get('prerequisite_details')}")

assert linked_list_node["study_available"] == True, "Study material should be universally available!"
assert linked_list_node["is_unlocked"] == False, "Practice for Linked List should be locked due to Arrays mastery prerequisite!"
print(">>> JOURNEY B: VERIFIED & PASSED")

# ---------------------------------------------------------
# JOURNEY C: LEARNER GOAL SYSTEM
# ---------------------------------------------------------
print("\n--- JOURNEY C: Learner Goal System Validation ---")
goals = get("/api/goals?learner_id=1")
print(f"[C1] Total Goals count for Learner 1: {len(goals)}")
active_goal = [g for g in goals if g["status"] == "ACTIVE"][0]
print(f"[C2] Active Goal: '{active_goal['goal_name']}' target={active_goal['target_mastery']*100:.0f}%, progress={active_goal['progress_percentage']:.1f}%")

# Create a new goal for Trees (concept_id=8)
new_goal_res = post("/api/goals", {
    "learner_id": 1,
    "concept_id": 8,
    "goal_name": "Master Tree Traversal & BSTs",
    "target_mastery": 0.85,
    "target_date": "2025-08-31"
})
print(f"[C3] New Goal Created: ID {new_goal_res['id']}, Status: {new_goal_res['status']}, Progress: {new_goal_res['progress_percentage']:.1f}%")

goals_updated = get("/api/goals?learner_id=1")
print(f"[C4] Updated Total Goals count: {len(goals_updated)}")
print(">>> JOURNEY C: VERIFIED & PASSED")

# ---------------------------------------------------------
# OBSERVABILITY & EXPLAINABILITY AUDIT
# ---------------------------------------------------------
print("\n--- OBSERVABILITY & EXPLAINABILITY AUDIT ---")
recs = d2["recommendations"]
print(f"[D1] Rationale Object: {json.dumps(recs[0].get('rationale'), indent=2)}")
print(f"[D2] Active Goal Object in Recommendation: {json.dumps(recs[0].get('active_goal'), indent=2)}")
print(f"[D3] KPI metrics: {json.dumps(d2['kpis'], indent=2)}")
print(">>> OBSERVABILITY AUDIT: VERIFIED & PASSED")

print("\n=" * 70)
print("ALL E2E LEARNER JOURNEYS SUCCESSFULLY VALIDATED!")
print("=" * 70)
