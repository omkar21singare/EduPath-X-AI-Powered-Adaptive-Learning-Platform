"""Phase 4D — Live state audit script."""
import urllib.request
import json

BASE = "http://localhost:8000"

def get(path):
    with urllib.request.urlopen(BASE + path) as r:
        return json.loads(r.read())

# ---------- Dashboard ----------
d = get("/api/dashboard?learner_id=1")
km = d["knowledge_map"]

print("=" * 80)
print("KNOWLEDGE MAP")
print("=" * 80)
hdr = f"{'Code':<24} {'Mastery':>8} {'Unlock':>7} {'PractAvail':>11} {'Qcnt':>5} {'Status'}"
print(hdr)
print("-" * 80)
for n in km:
    print(
        f"{n['code']:<24} {n['mastery_percentage']:>7.1f}%"
        f" {str(n['is_unlocked']):>7}"
        f" {str(n.get('practice_available','?')):>11}"
        f" {str(n.get('question_count','?')):>5}"
        f" {n['status']}"
    )

print()
print("=" * 80)
print("GOAL")
print("=" * 80)
g = d.get("goal")
if g:
    print(f"  Title   : {g['title']}")
    print(f"  Concept : {g['concept_title']}")
    print(f"  Current : {g['current_mastery']*100:.1f}%")
    print(f"  Target  : {g['target_mastery']*100:.0f}%")
    print(f"  Progress: {g['progress_percentage']:.0f}%")
    print(f"  Status  : {g['status']}")
else:
    print("  No active goal")

print()
print("=" * 80)
print("RECOMMENDATIONS")
print("=" * 80)
for r in d.get("recommendations", []):
    print(f"  Concept : {r['concept_code']} — {r['concept_title']}")
    print(f"  Action  : {r['action_type']}  Difficulty: {r['target_difficulty']}")
    print(f"  Mastery : {r['current_mastery']:.1f}%")
    print(f"  Reason  : {r['reason_text']}")
    print()

print("=" * 80)
print("QUESTIONS CHECK (concept 3 = ARRAYS)")
print("=" * 80)
qs = get("/api/questions?concept_id=3")
print(f"  Count: {len(qs)}")
for q in qs[:5]:
    print(f"  [{q['id']}] {q['difficulty']} — {q['text'][:70]}")

print()
print("=" * 80)
print("KPIs")
print("=" * 80)
for k, v in d.get("kpis", {}).items():
    print(f"  {k}: {v}")

print()
print("=" * 80)
print("PERFORMANCE OVERVIEW")
print("=" * 80)
for k, v in d.get("performance_overview", {}).items():
    print(f"  {k}: {v}")
