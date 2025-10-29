"""
Monte Carlo simulation of Nd isotope mixing fractions.

This script reads water mass data (Age, εNd), generates random realizations
of Nd isotopic compositions and concentrations within specified uncertainty
ranges, and computes the mixing fraction of two end-members using a Monte Carlo
approach. For each time step in the input data, it outputs the mean and standard
deviation of the calculated fraction.

Input:
    - water_mass_data.dat : ASCII file with two columns
        (i) Age (ka)
        (ii) εNd
        (iii) Error

Output:
    - frac_nd1.dat : ASCII file with three columns
        (i) Age (ka)
        (ii) Mean fraction of Nd1
        (iii) Standard deviation of fraction

Author:
    Prajeesh A G
    Email: prajeeshag@gmail.com
"""

import numpy as np

# -------- INPUTS --------
input_data = "NdDataForFractionCalculation.csv"
output_data = "water_mass_ratio.csv"
Num_Random = 10000
ENd1, err_ENd1 = -13.5, 1
ENd2, err_ENd2 = -4.5, 1
CNd1, err_CNd1 = 22, 5
CNd2, err_CNd2 = 42, 2

# Load data: 2 columns -> Age (ka), epsilon Nd
d1 = np.genfromtxt(input_data, delimiter=",", skip_header=1)

# Random values
rENd1 = (ENd1 - err_ENd1) + (2 * err_ENd1) * np.random.rand(Num_Random)
rENd2 = (ENd2 - err_ENd2) + (2 * err_ENd2) * np.random.rand(Num_Random)
rCNd1 = (CNd1 - err_CNd1) + (2 * err_CNd1) * np.random.rand(Num_Random)
rCNd2 = (CNd2 - err_CNd2) + (2 * err_CNd2) * np.random.rand(Num_Random)

# Result container
Frac_Nd1 = []

# Loop over input data
for tme, ENdm, err_ENdm in d1:
    rENdm = (ENdm - err_ENdm) + (2 * err_ENdm) * np.random.rand(Num_Random)
    f1 = rCNd2 * (rENd2 - rENdm) / (rCNd1 * (rENdm - rENd1) + rCNd2 * (rENd2 - rENdm))
    Frac_Nd1.append([tme, np.mean(f1), np.std(f1)])

Frac_Nd1 = np.array(Frac_Nd1)  # type: ignore

# Save result
np.savetxt(
    output_data,
    Frac_Nd1,
    delimiter=",",
    header="Age,Mean,Std",
    comments="",
    fmt="%.6f",
)
