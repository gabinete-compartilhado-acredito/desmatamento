import numpy as np

def compute_correlation(a, b):
    """
    Return the Pearson correlation between 
    `a` (array-like) and `b` (array-like).
    """
    return np.corrcoef(a, b)[0, 1]


def bootstrap_correlation(series_a, series_b, n_trials=10000):
    """
    Return `n_trials` (int) correlations (array) 
    computed from `series_a` (Series) and `series_b` 
    (Series) when the second series is scrambled.
    """
    
    assert len(series_a) == len(series_b)
    n_instances = len(series_b)
    
    corrs = np.array([compute_correlation(series_a, series_b.sample(n_instances)) for _ in range(n_trials)])
    
    return corrs
