"""Utility functions.
"""
import numpy as np
import os
import pandas as pd


__all__ = []


def reduce_cores(n_core, cpu_count=None):
    if cpu_count is None:
        cpu_count = os.cpu_count()
    n_core = min(n_core, cpu_count)
    return n_core


def remove_variables(data, exclude_variables=None):
    if exclude_variables is not None:
        data = data.drop(exclude_variables, axis=1, inplace=False)
    return data


def process_coefficients(coefs, column_names, survival_rate_cutoff=0.05):
    n = coefs.shape[0]
    survived = 1 * (abs(coefs) > 0)
    survival_rate = np.sum(survived, axis=0) / float(n)
    mask = 1 * (survival_rate > survival_rate_cutoff)
    coefs_updated = coefs * mask
    betas = pd.DataFrame({'predictor': column_names})
    betas['mean'] = np.mean(coefs_updated, axis=0)
    betas['lb'] = np.percentile(coefs_updated, q=2.5, axis=0)
    betas['ub'] = np.percentile(coefs_updated, q=97.5, axis=0)
    betas['survival'] = mask
    betas['sig'] = betas['survival']
    betas['dotColor1'] = 1 * (betas['mean'] != 0)
    betas['dotColor2'] = (1 * np.logical_and(betas['dotColor1'] > 0, betas['sig'] > 0)) + 1
    betas['dotColor'] = betas['dotColor1'] * betas['dotColor2']
    return betas
