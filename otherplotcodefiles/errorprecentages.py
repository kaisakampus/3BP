import numpy as np
import os

# to produce these systematically, I used ai to save time
base_dir = r"C:\Users\kaisa\My Drive\Simulated_Data"

dataset_names = [("brouckeA2","broucke A2 ±ε=1e-4",""),("butterflyI","butterfly I ±ε=1e-4",""),
                 ("figure8","figure 8 ±ε=1e-4",""),("yinyang","yinyang III 12.A.a ±ε=1e-4",""),
                 ("brouckeA1","broucke A1 ±ε=1e-4",""),("brouckeA7","broucke A7 ±ε=1e-4",""),
                 ("yinyang312ABeta","yinyang III 12.A.b ±ε=1e-4",""),
                 ("orbit_O3","O3 ±ε=1e-4",""),
                 ("yarn","yarn ±ε=1e-4", "_"),("panio_trio_O50_04","O50 ±ε=1e-4", "_"),
                 ("brouckeA11","broucke A11 ±ε=1e-4",""),]

def load_variant(base_dir, name, suffix="", sep=""):
    bodies = []
    for i in range(3):
        variant_name = f"{name}{sep}{suffix}" if suffix else name
        path = os.path.join(base_dir, f"{variant_name}_LAST_body{i}.csv")
        bodies.append(np.loadtxt(path, delimiter=","))
    return bodies

def hyperradius(bodies):
    mags = [np.sqrt(b[:,0]**2 + b[:,1]**2 + b[:,2]**2) for b in bodies]
    return np.sqrt(mags[0]**2 + mags[1]**2 + mags[2]**2)

def compute_error(r_main, r_add, r_sub):
    delta_r = np.abs(r_add - r_sub)
    return np.where(r_main != 0, (delta_r / r_main) * 100, 0)

all_avg_errors = {}

for name, title, sep in dataset_names:
    print(f"{name}")
    try:
        timesteps   = np.loadtxt(os.path.join(base_dir, f"{name}_LAST_timestep_sizes.csv"))
        bodies_main = load_variant(base_dir, name, suffix="",    sep=sep)
        bodies_add  = load_variant(base_dir, name, suffix="add", sep=sep)
        bodies_sub  = load_variant(base_dir, name, suffix="sub", sep=sep)
    except FileNotFoundError as e:
        print(f"file not found: {e}")
        continue

    hr_main = hyperradius(bodies_main)
    hr_add  = hyperradius(bodies_add)
    hr_sub  = hyperradius(bodies_sub)

    min_len = min(len(hr_main), len(hr_add), len(hr_sub))
    hr_main = hr_main[:min_len]
    hr_add  = hr_add[:min_len]
    hr_sub  = hr_sub[:min_len]

    avg_error = np.mean(compute_error(hr_main, hr_add, hr_sub))
    #avg_error = np.median(compute_error(hr_main, hr_add, hr_sub)) median does not help me much here though
    all_avg_errors[title] = avg_error
    print(f"  Average error: {avg_error:.4f}%")

print("\naverage trajectory error per configuration")
for title, avg in all_avg_errors.items():
    print(f"  {title}: {avg:.4f}%")

overall_avg = np.mean(list(all_avg_errors.values()))
#overall_avg = np.median(list(all_avg_errors.values()))
print(f"\noverall average error across all configurations: {overall_avg:.4f}%")
print("complete")