import numpy as np
import matplotlib.pyplot as plt
import os

base_dir = r"C:\Users\kaisa\My Drive\Simulated_Data"

def load_variant(base_dir, variant_name):
    bodies = []
    for i in range(0, 3):
        path = os.path.join(base_dir, f"{variant_name}_LAST_body{i}.csv")
        bodies.append(np.loadtxt(path, delimiter=","))
    return bodies

def hyperradius(bodies):
    mags = [np.sqrt(b[:,0]**2 + b[:,1]**2 + b[:,2]**2) for b in bodies]
    return np.sqrt(mags[0]**2 + mags[1]**2 + mags[2]**2)

def compute_error(r_main, r_add, r_sub):
    delta_r = np.abs(r_add - r_sub)
    return np.where(r_main != 0, (delta_r / r_main) * 100, 0)

name      = "yarn"
title     = "yarn ±ε=1e-4"
add_name  = "yarn_add"
sub_name  = "yarn_sub"

print(f"Processing {name}...")
timesteps   = np.loadtxt(os.path.join(base_dir, f"{name}_LAST_timestep_sizes.csv"))
bodies_main = load_variant(base_dir, name)
bodies_add  = load_variant(base_dir, add_name)
bodies_sub  = load_variant(base_dir, sub_name)

cumulative_time = np.cumsum(timesteps)
hr_main = hyperradius(bodies_main)
hr_add  = hyperradius(bodies_add)
hr_sub  = hyperradius(bodies_sub)

min_len = min(len(cumulative_time), len(hr_main), len(hr_add), len(hr_sub))
cumulative_time = cumulative_time[:min_len]
hr_main = hr_main[:min_len]
hr_add  = hr_add[:min_len]
hr_sub  = hr_sub[:min_len]

error = compute_error(hr_main, hr_add, hr_sub)

# --- plot 1: hyperradius ---
plt.figure(figsize=(10, 5))
plt.semilogy(cumulative_time, hr_sub,  color="turquoise", linewidth=1, label="r1_x−ε")
plt.semilogy(cumulative_time, hr_add,  color="lime",      linewidth=1, label="r1_x+ε")
plt.semilogy(cumulative_time, hr_main, color="deeppink",  linewidth=1, label="r1_x")
plt.xlabel("simulation time")
plt.ylabel("hyperradius R (log)")
plt.title(f"Hyperradius over time — {title}")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(base_dir, f"{name}_hyperradius.png"), dpi=150)
plt.close()

# --- plot 2: trajectory error ---
plt.figure(figsize=(10, 5))
plt.plot(cumulative_time, error, color="purple", linewidth=1)
plt.xlabel("simulation time")
plt.ylabel("δ (%)")
plt.title(f"Trajectory error over time — {title}")
plt.tight_layout()
plt.savefig(os.path.join(base_dir, f"{name}_trajectory_error.png"), dpi=150)
plt.close()

print(f"Done. Saved {name}_hyperradius.png + {name}_trajectory_error.png")