import numpy as np
import matplotlib.pyplot as plt
import os

base_dir = r"C:\Users\kaisa\My Drive\Simulated_Data"

#dataset_names = ["yarn", "paino_trio_O50_04"]

#def load_variant(base_dir, name, suffix=""):
    #"""Load 3 bodies for one variant (main/add/sub). Returns (N,3) array per body."""
    #bodies = []
    #for i in range(0, 3):
    #    path = os.path.join(base_dir, f"{name}{suffix}_LAST_body{i}.csv")
    #    bodies.append(np.loadtxt(path, delimiter=","))
    #return bodies  # list of 3 arrays, each (N, 3)

# (name, title, suffix_sep)
dataset_names = [("brouckeA2","broucke A2 ±ε=1e-4",""),("butterflyI","butterfly I ±ε=1e-4",""),
                 ("figure8","figure 8 ±ε=1e-4",""),("yinyang","yinyang III 12.A.a ±ε=1e-4",""),
                 ("brouckeA1","broucke A1 ±ε=1e-4",""),("brouckeA7","broucke A7 ±ε=1e-4",""),
                 ("yinyang312ABeta","yinyang III 12.A.b ±ε=1e-4",""),("brouckeA1","broucke A1 ±ε=1e-4",""),
                 ("orbit_O3","O3 ±ε=1e-4",""),("orbit_O26","O26 ±ε=1e-4",""),]

def load_variant(base_dir, name, suffix="", sep=""):
    bodies = []
    for i in range(0, 3):
        variant_name = f"{name}{sep}{suffix}" if suffix else name
        path = os.path.join(base_dir, f"{variant_name}_LAST_body{i}.csv")
        bodies.append(np.loadtxt(path, delimiter=","))
    return bodies

for name, title, sep in dataset_names:
    print(f"Processing {name}...")
    try:
        timesteps     = np.loadtxt(os.path.join(base_dir, f"{name}_LAST_timestep_sizes.csv"))
        bodies_main   = load_variant(base_dir, name, suffix="",    sep=sep)
        bodies_add    = load_variant(base_dir, name, suffix="add", sep=sep)
        bodies_sub    = load_variant(base_dir, name, suffix="sub", sep=sep)
    except FileNotFoundError as e:
        print(f"  Skipping — file not found: {e}")
        continue
    # ... rest unchanged

def hyperradius(bodies):
    """Compute hyperradius R = sqrt(|r1|² + |r2|² + |r3|²) at each timestep."""
    mags = [np.sqrt(b[:,0]**2 + b[:,1]**2 + b[:,2]**2) for b in bodies]
    return np.sqrt(mags[0]**2 + mags[1]**2 + mags[2]**2)

#def compute_error(r_main, r_add, r_sub):
#    """δ = (r - Δr) / r * 100, where Δr = |r_add - r_sub|."""
#    delta_r = np.abs(r_add - r_sub)
#    return np.where(r_main != 0, (r_main - delta_r) / r_main * 100, 0)

def compute_error(r_main, r_add, r_sub):
    delta_r = np.abs(r_add - r_sub)
    return np.where(r_main != 0, (delta_r / r_main) * 100, 0)

for name in dataset_names:
    print(f"Processing {name}...")

    # --- load ---
    try:
        timesteps = np.loadtxt(os.path.join(base_dir, f"{name}_LAST_timestep_sizes.csv"))
        bodies_main = load_variant(base_dir, name, suffix="")
        bodies_add  = load_variant(base_dir, name, suffix="add")
        bodies_sub  = load_variant(base_dir, name, suffix="sub")
    except FileNotFoundError as e:
        print(f"  Skipping — file not found: {e}")
        continue

    cumulative_time = np.cumsum(timesteps)

    # --- hyperradius ---
    hr_main = hyperradius(bodies_main)
    hr_add  = hyperradius(bodies_add)
    hr_sub  = hyperradius(bodies_sub)

# after loading cumulative_time and hr_main/add/sub
    min_len = min(len(cumulative_time), len(hr_main), len(hr_add), len(hr_sub))
    cumulative_time = cumulative_time[:min_len]
    hr_main = hr_main[:min_len]
    hr_add  = hr_add[:min_len]
    hr_sub  = hr_sub[:min_len]

    # --- plot 1: hyperradius over time ---
    plt.figure(figsize=(10, 5))
    plt.semilogy(cumulative_time, hr_sub,  color="turquoise", linewidth=1, label=f"{name} (r1_x−ε)")
    plt.semilogy(cumulative_time, hr_add,  color="lime",      linewidth=1, label=f"{name} (r1_x+ε)")
    plt.semilogy(cumulative_time, hr_main, color="deeppink",  linewidth=1, label=f"{name} r1_x")
    plt.xlabel("simulation time")
    plt.ylabel("hyperradius R (log)")
    plt.title(f"Hyperradius over time — {name}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, f"{name}_hyperradius.png"), dpi=150)
    plt.close()

    # --- plot 2: trajectory error over time ---
    error = compute_error(hr_main, hr_add, hr_sub)

    plt.figure(figsize=(10, 5))
    plt.plot(cumulative_time, error, color="purple", linewidth=1)
    plt.xlabel("simulation time")
    plt.ylabel("δ (%)")
    plt.title(f"Trajectory error over time — {name}")
    plt.tight_layout()
    plt.savefig(os.path.join(base_dir, f"{name}_trajectory_error.png"), dpi=150)
    plt.close()

    print(f"  Saved plots for {name}.")

print("Done.")