# trajectory error over time
import numpy as np
import matplotlib.pyplot as plt
import os

def compute_trajectory_error(original_bodies, perturbed_bodies):
    # Compute Euclidean distance at each timestep
    error = np.linalg.norm(perturbed_bodies - original_bodies, axis=1)
    mag_original = np.linalg.norm(original_bodies, axis=1)
    # Avoid division by zero
    error_percentage = np.where(mag_original != 0, (error / mag_original) * 100, 0)
    return error_percentage

base_dir = r"C:\Users\kaisa\My Drive\Simulated_Data"
dataset_names = ["figure8", "brouckeA2", "loopendedtriangles", "ovalswithflourishes", "orbit_O2", "orbit_O3", "orbit_O26"]

for name in dataset_names:
    # Load original and perturbed trajectories for body0 (or any body you choose)
    original_body0 = np.loadtxt(os.path.join(base_dir, f"{name}.csv"), delimiter=",")
    add_body0 = np.loadtxt(os.path.join(base_dir, f"{name}add.csv"), delimiter=",")
    sub_body0 = np.loadtxt(os.path.join(base_dir, f"{name}sub.csv"), delimiter=",")
    
    # Compute error percentages
    error_pct_add = compute_trajectory_error(original_body0, add_body0)
    error_pct_sub = compute_trajectory_error(original_body0, sub_body0)
    
    # Plot both errors
    plt.figure(figsize=(10, 5))
    plt.plot(error_pct_add, label='Add Perturbation Error %')
    plt.plot(error_pct_sub, label='Sub Perturbation Error %')
    plt.xlabel("Time step")
    plt.ylabel("Error Percentage (%)")
    plt.title(f"Trajectory Error Percentage over Time for {name}")
    plt.legend()
    plt.tight_layout()

    # Save plot
    save_path = os.path.join(base_dir, f"{name}_trajectory_error_comparison.png")
    plt.savefig(save_path)
    plt.close()