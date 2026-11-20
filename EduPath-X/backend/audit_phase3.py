import json
import collections

results_path = "simulation/results/experiment_results.json"
with open(results_path, "r") as f:
    data = json.load(f)

print("1. Total Response Observations:", len(data))

learners = set()
items = set()
concepts = set()
responses_per_learner = collections.Counter()
responses_per_item = collections.Counter()
learners_per_item = collections.defaultdict(set)
items_per_learner = collections.defaultdict(set)
correct_count = 0
correct_per_item = collections.defaultdict(int)
correct_per_concept = collections.defaultdict(int)
responses_per_concept = collections.defaultdict(int)

item_concepts = {}

for row in data:
    learner_id = f"{row['profile']}_{row['arm']}_{row['learner_id']}"
    item_id = row['question_id']
    concept_id = row['concept']
    
    learners.add(learner_id)
    items.add(item_id)
    concepts.add(concept_id)
    
    item_concepts[item_id] = concept_id
    
    responses_per_learner[learner_id] += 1
    responses_per_item[item_id] += 1
    
    learners_per_item[item_id].add(learner_id)
    items_per_learner[learner_id].add(item_id)
    
    responses_per_concept[concept_id] += 1
    
    is_correct = row.get("correctness", False)
    if is_correct:
        correct_count += 1
        correct_per_item[item_id] += 1
        correct_per_concept[concept_id] += 1

print("2. Unique Learners:", len(learners))
print("3. Unique Items:", len(items))
print("4. Unique Concepts:", len(concepts))

rpl_vals = list(responses_per_learner.values())
if rpl_vals:
    rpl_vals.sort()
    print("5. Responses per Learner: min=", rpl_vals[0], "median=", rpl_vals[len(rpl_vals)//2], "mean=", sum(rpl_vals)/len(rpl_vals), "max=", rpl_vals[-1])

rpi_vals = list(responses_per_item.values())
if rpi_vals:
    rpi_vals.sort()
    print("6. Responses per Item: min=", rpi_vals[0], "median=", rpi_vals[len(rpi_vals)//2], "mean=", sum(rpi_vals)/len(rpi_vals), "max=", rpi_vals[-1])

lpi_vals = [len(s) for s in learners_per_item.values()]
print("7. Unique learners per item average:", sum(lpi_vals)/len(lpi_vals) if lpi_vals else 0)

ipl_vals = [len(s) for s in items_per_learner.values()]
print("8. Unique items per learner average:", sum(ipl_vals)/len(ipl_vals) if ipl_vals else 0)

print("9. Overall correctness rate:", correct_count / len(data) if data else 0)

print("\n10. Concept Correctness Rates:")
for concept_id, count in sorted(correct_per_concept.items()):
    print(f"Concept {concept_id}: {count / responses_per_concept[concept_id]:.2f}")

print("\n11. Item Analysis:")
zero_correct = []
all_correct = []
low_response = []
high_response = []

coverage_by_concept = collections.defaultdict(lambda: {'answered': 0, 'ge5': 0, 'ge10': 0, 'ge20': 0, 'ge50': 0})

for item_id in items:
    c = item_concepts[item_id]
    ans = responses_per_item[item_id]
    rate = correct_per_item[item_id] / ans
    
    coverage_by_concept[c]['answered'] += 1
    if ans >= 5: coverage_by_concept[c]['ge5'] += 1
    if ans >= 10: coverage_by_concept[c]['ge10'] += 1
    if ans >= 20: coverage_by_concept[c]['ge20'] += 1
    if ans >= 50: coverage_by_concept[c]['ge50'] += 1
    
    if rate == 0.0: zero_correct.append(item_id)
    if rate == 1.0: all_correct.append(item_id)
    if ans < 5: low_response.append(item_id)
    if ans > 500: high_response.append(item_id)

print("\nCoverage by concept:")
totals = {"ARRAYS": 8, "LINKED_LIST": 8, "STACKS": 12, "TREES": 8, "GRAPHS": 8, "QUEUES": 0, "ALG_THINK": 0}
for c in ["ARRAYS", "LINKED_LIST", "STACKS", "TREES", "GRAPHS", "QUEUES", "ALG_THINK"]:
    d = coverage_by_concept[c]
    print(f"{c}: Total={totals[c]}, >=1={d['answered']}, >=5={d['ge5']}, >=10={d['ge10']}, >=20={d['ge20']}, >=50={d['ge50']}")

print("\nExtremes:")
print("100% correct items:", len(all_correct))
print("0% correct items:", len(zero_correct))
print("< 5 responses items:", len(low_response))
print("> 500 responses items:", len(high_response))

