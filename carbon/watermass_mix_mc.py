"""
Monte Carlo simulation of

Author:
    Prajeesh A G
    Email: prajeeshag@gmail.com
"""

import numpy as np

# -------- INPUTS --------
output_data = "water_mass_ratio.csv"
Num_Random = 10000

# Load data: 2 columns -> Age (ka), epsilon Nd
ncw_dat = np.genfromtxt("NCW.csv", delimiter=",", skip_header=1)
pdw_dat = np.genfromtxt("PDW.csv", delimiter=",", skip_header=1)
sample_dat = np.genfromtxt("Sample.csv", delimiter=",", skip_header=1)

ncw_r = 1.0
ncw_err = 0.1
pdw_r = -0.5
pdw_err = 0.1

# Result container
Fnsw = []

# Loop over input data
for i in range(len(ncw_dat)):
    tme, ncw = ncw_dat[i]
    if np.isnan(ncw):
        continue
    _, pdw = pdw_dat[i]
    if np.isnan(pdw):
        continue
    _, sample = sample_dat[i]
    if np.isnan(sample):
        continue

    # r_na_stack = (na_stack - na_stack_err) + (2 * na_stack_err) * np.random.rand(
    #     Num_Random
    # ) * 0.0
    ncw = (ncw - ncw_err) + (2 * ncw_err) * np.random.rand(Num_Random)
    pdw = (pdw - pdw_err) + (2 * pdw_err) * np.random.rand(Num_Random)

    f1 = (sample - pdw) / (ncw - pdw) * 100.0
    f1_mean = np.mean(f1)
    f1_std = np.std(f1)
    # f1 = (u1385 - r_u1479) / (r_na_stack - r_u1479) * 100.0
    if f1_mean > 100.0 or f1_mean < 0.0:
        print(i + 2, sample, f1_mean)

    Fnsw.append([tme, f1_mean, f1_std])
Fnsw = np.array(Fnsw)  # type: ignore

print("Min:", Fnsw.min(axis=0))
print("Max:", Fnsw.max(axis=0))

# Save result
np.savetxt(
    output_data,
    Fnsw,
    delimiter=",",
    header="Age,Mean,Std",
    comments="",
    fmt="%.6f",
)
