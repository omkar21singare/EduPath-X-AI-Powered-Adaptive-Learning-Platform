import json
import pandas as pd
with open('experiments/phase3b/results/experiment_results.json') as f:
    results = json.load(f)
    print(len(results), "trajectories loaded.")
    if len(results) > 0:
        print(results[0].keys())
        print(results[0].get('arm'))
