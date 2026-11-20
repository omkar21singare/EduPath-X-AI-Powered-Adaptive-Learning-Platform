import json
with open('simulation/results/experiment_results.json', 'r') as f:
    data = json.load(f)
print(json.dumps(data[0], indent=2))
