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


def p_value(trials, threshold):
    """
    Compute the right-side p-value by counting the 
    fraction of random `trials` (numerical array-like) 
    that are greater than `threshold` (number).
    """
    pvalue = (trials > threshold).sum() / len(trials)
    return pvalue


def shuffle_data(data, random_state=None):
    """
    Shuffle the data whiule maintaining 
    the same index.
    
    Parameters
    ----------
    data : DataFrame or Series
        Data to be shuffled.
    random_state : int or None
        Seed for the number generator.
        Set to `None` for a random seed.
    
    Returns
    -------
    shuffled : DataFrame or Series
        Same as `data` but with shuffled
        entries, keeping the index order 
        exactly the same.
    """
    # Shuffle entries:
    shuffled = data.sample(len(data), random_state=random_state)
    # Keep the same index as before:
    shuffled.index = data.index
    
    return shuffled
