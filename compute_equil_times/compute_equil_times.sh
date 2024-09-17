# Compute equilibration times for the bound and free data

# Bound vanish multi window data
python compute_equil_times.py ../synthetic_data_creation/output/synthetic_data_bound_vanish.pkl \
                              output/synthetic_data_bound_vanish_with_equil_times.pkl

# Free vanish multi window data
python compute_equil_times.py ../synthetic_data_creation/output_free/synthetic_data_bound_vanish.pkl \
                              output_free/synthetic_data_free_vanish_with_equil_times.pkl

# Bound vanish single window data
python compute_equil_times.py ../synthetic_data_creation/output_single/synthetic_data_bound_vanish.pkl \
                              output_single/synthetic_data_bound_vanish_with_equil_times.pkl
