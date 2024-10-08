"""Compute the equilibration times for all desired methods for the synthetic data."""

import red
import tqdm
import typer
import numpy as np
import pickle as pkl
from pathlib import Path
from itertools import repeat
from functools import partial
import multiprocessing as mp

# Adapted from https://stackoverflow.com/questions/45718523/pass-kwargs-to-starmap-while-using-pool-in-python
def starmap_with_kwargs(pool, fn, args_iter, kwargs_iter):
    args_for_starmap = zip(repeat(fn), args_iter, kwargs_iter)
    return pool.starmap(apply_arg_and_kwargs, args_for_starmap)

def apply_arg_and_kwargs(fn, arg, kwargs):
    return fn(arg, **kwargs)

def naive_equil_fn(data, fraction):
    """Truncate the data at the given fraction of the total number of samples"""
    start_idx = round(data.shape[0] * fraction)
    return (start_idx,None, None)

def main(input_file: Path, output_file: Path):
    # Load the synthetic data
    with open(input_file, "rb") as f:
        synthetic_data = pkl.load(f)

    # Define the methods to use, with what arguments (as implemented in red)
    methods= {
        "Uncorrelated Estimate": {"function": red.detect_equilibration_window, "kwargs": {"window_size_fn": None, "window_size": 1}},
        "Window Size 5": {"function": red.detect_equilibration_window, "kwargs": {"window_size_fn": None, "window_size": 5}},
        "Window Size 50": {"function": red.detect_equilibration_window, "kwargs": {"window_size_fn": None, "window_size": 50}},
        "Window Size $\\sqrt{N_{n_0}}$": {"function": red.detect_equilibration_window, "kwargs": {"window_size": None}}, # Use default n**0.5 size - avoid issues with pickling for pool
        "Initial Sequence: Chodera" : {"function": red.detect_equilibration_init_seq, "kwargs": {"sequence_estimator": "positive", "min_max_lag_time":3, "smooth_lag_times": False}},
        "Initial Sequence: Positive": {"function": red.detect_equilibration_init_seq, "kwargs": {"sequence_estimator": "initial_positive", "min_max_lag_time":3, "smooth_lag_times": False}},
        "Initial Sequence: Monotone": {"function": red.detect_equilibration_init_seq, "kwargs": {"sequence_estimator": "initial_monotone", "min_max_lag_time":3, "smooth_lag_times": False}},
        "Initial Sequence: Convex": {"function": red.detect_equilibration_init_seq, "kwargs": {"sequence_estimator": "initial_convex", "min_max_lag_time":3, "smooth_lag_times": False}},
        "Initial Sequence: Smoothed Lag Convex": {"function": red.detect_equilibration_init_seq, "kwargs": {"sequence_estimator": "initial_convex", "min_max_lag_time":3, "smooth_lag_times": True}},
    }
    # Add methods which are simply truncation at a given fraction of the data, from 0 to 1 at 0.05 intervals
    naive_methods = {f"Discard Fraction {i}": {"function": partial(naive_equil_fn, fraction=i), "kwargs": {}} for i in np.arange(0, 1.05, 0.05)}
    methods |= naive_methods

    # Cycle through all the synthetic dataset, all systems, and all data
    for dataset_name in tqdm.tqdm(synthetic_data, desc="Datasets"):
        for system_name in tqdm.tqdm([system for system in synthetic_data[dataset_name] if system != "times"], desc="Systems"):
            for method in tqdm.tqdm(methods, desc="Methods"):
                # Skip if we've already analysed.
                if method in synthetic_data[dataset_name][system_name][0]:
                    continue
                # Speed things up with multiprocessing to process data in parallel
                with mp.Pool(mp.cpu_count()) as pool:
                    timeseries = [data["data"] for data in synthetic_data[dataset_name][system_name].values()] 
                    fn = methods[method]["function"]
                    kwargs = [methods[method]["kwargs"] for _ in range(len(synthetic_data[dataset_name][system_name].values()))]
                    results = starmap_with_kwargs(pool, fn, timeseries, kwargs)
                for i, result in enumerate(results):
                    idx, g, ess = result
                    # Get the mean using this index
                    mean = synthetic_data[dataset_name][system_name][i]["data"][idx:].mean()
                    # Fraction of data discarded
                    frac_discarded = idx / len(synthetic_data[dataset_name][system_name][i]["data"])
                    # Store everything
                    synthetic_data[dataset_name][system_name][i][method] = {"idx": idx, "g": g, "ess": ess, "mean": mean, "frac_discarded": frac_discarded}

                # Keep saving the data to a pickle file
                with open(output_file, "wb") as f:
                    pkl.dump(synthetic_data, f)

if __name__ == "__main__":
    typer.run(main)
