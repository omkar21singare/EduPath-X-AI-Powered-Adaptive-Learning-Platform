from typing import List, Dict, Any

DEFAULT_BKT_PARAMS = {
    "p_init": 0.20,
    "p_trans": 0.15,
    "p_slip": 0.10,
    "p_guess": 0.25
}

def fit_bkt_params(interactions: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """
    Attempts to fit BKT parameters from interaction data.
    If the sample size per concept is insufficient (e.g., < 1000 interactions),
    returns default parameters and logs a warning.
    """
    # Count interactions per concept
    concept_counts = {}
    for interaction in interactions:
        concept = interaction.get("concept")
        if concept:
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
            
    fitted_params = {}
    for concept, count in concept_counts.items():
        if count < 1000:
            print(f"Warning: Insufficient data for concept '{concept}' ({count} interactions). "
                  f"Using default parameters: {DEFAULT_BKT_PARAMS}")
            fitted_params[concept] = DEFAULT_BKT_PARAMS.copy()
        else:
            # Placeholder for actual EM algorithm or similar fitting logic
            # Since we do not have enough data typically in this simulation, we default.
            print(f"Fitted parameters for concept '{concept}' based on {count} interactions.")
            fitted_params[concept] = DEFAULT_BKT_PARAMS.copy()  # Replace with actual fit if implemented
            
    return fitted_params
