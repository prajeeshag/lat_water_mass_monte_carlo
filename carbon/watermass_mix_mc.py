"""
Monte Carlo simulation of

Author:
    Prajeesh A G
    Email: prajeeshag@gmail.com
"""

import numpy as np

# -------- INPUTS --------
input_data = "NdDataForFractionCalculation.csv"
output_data = "water_mass_ratio.csv"
Num_Random = 10000

# Load data: 2 columns -> Age (ka), epsilon Nd
na_stack_dat = np.genfromtxt("NA_Stack.csv", delimiter=",", skip_header=1)
u1385_dat = np.genfromtxt("U1385orU1475.csv", delimiter=",", skip_header=1)
u1479_dat = np.genfromtxt("U1479orPacific.csv", delimiter=",", skip_header=1)

print(na_stack_dat)

# Result container
Fnsw = []

# Loop over input data
for i in range(len(na_stack_dat)):
    tme, na_stack, na_stack_err = na_stack_dat[i]
    _, u1479, u1479_err = u1479_dat[i]
    _, u1385 = u1385_dat[i]
    r_na_stack = (na_stack - na_stack_err) + (2 * na_stack_err) * np.random.rand(
        Num_Random
    )
    r_u1479 = (u1479 - u1479_err) + (2 * u1479_err) * np.random.rand(Num_Random)

    f1 = (u1385 - r_u1479) / (r_na_stack - r_u1479) * 100.0
    Fnsw.append([tme, np.mean(f1), np.std(f1)])
Fnsw = np.array(Fnsw)  # type: ignore

# Save result
np.savetxt(
    output_data,
    Fnsw,
    delimiter=",",
    header="Age,Mean,Std",
    comments="",
    fmt="%.6f",
)
