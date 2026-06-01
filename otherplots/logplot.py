'''import numpy as np
import matplotlib.pyplot as plt

# Simulated_Data includes configurations, there is 3 datafiles per configuration: original, added perturbation, subtracted perturbation
base = r"C:\Users\kaisa\My Drive\Simulated_Data\loopendedtriangles"

#body0 = np.loadtxt(base + "_body0.csv", delimiter=",")
#body1 = np.loadtxt(base + "_body1.csv", delimiter=",")
#body2 = np.loadtxt(base + "_body2.csv", delimiter=",")

# Load datasets
original_body0 = np.loadtxt(base + "_body0.csv", delimiter=",")
original_body1 = np.loadtxt(base + "_body1.csv", delimiter=",")
original_body2 = np.loadtxt(base + "_body2.csv", delimiter=",")

perturbed_body0 = np.loadtxt(base + "_body0_perturbed.csv", delimiter=",")
perturbed_body1 = np.loadtxt(base + "_body1_perturbed.csv", delimiter=",")
perturbed_body2 = np.loadtxt(base + "_body2_perturbed.csv", delimiter=",")

subtracted_body0 = np.loadtxt(base + "_body0_subtracted.csv", delimiter=",")
subtracted_body1 = np.loadtxt(base + "_body1_subtracted.csv", delimiter=",")
subtracted_body2 = np.loadtxt(base + "_body2_subtracted.csv", delimiter=",")

timesteps = np.loadtxt(base + "_timestep_sizes.csv")
cumulative_time = np.cumsum(timesteps)

# magnitude of position vector for each body
#mag0 = np.sqrt(body0[:, 0]**2 + body0[:, 1]**2)
#mag1 = np.sqrt(body1[:, 0]**2 + body1[:, 1]**2)
#mag2 = np.sqrt(body2[:, 0]**2 + body2[:, 1]**2)

# Compute magnitude of position vectors for each dataset
mag_orig_0 = np.sqrt(original_body0[:, 0]**2 + original_body0[:, 1]**2)
mag_orig_1 = np.sqrt(original_body1[:, 0]**2 + original_body1[:, 1]**2)
mag_orig_2 = np.sqrt(original_body2[:, 0]**2 + original_body2[:, 1]**2)

mag_perturbed_0 = np.sqrt(perturbed_body0[:, 0]**2 + perturbed_body0[:, 1]**2)
mag_perturbed_1 = np.sqrt(perturbed_body1[:, 0]**2 + perturbed_body1[:, 1]**2)
mag_perturbed_2 = np.sqrt(perturbed_body2[:, 0]**2 + perturbed_body2[:, 1]**2)

mag_subtracted_0 = np.sqrt(subtracted_body0[:, 0]**2 + subtracted_body0[:, 1]**2)
mag_subtracted_1 = np.sqrt(subtracted_body1[:, 0]**2 + subtracted_body1[:, 1]**2)
mag_subtracted_2 = np.sqrt(subtracted_body2[:, 0]**2 + subtracted_body2[:, 1]**2)

#fig, ax = plt.subplots(figsize=(10, 5))

#ax.semilogy(cumulative_time, mag0, color="blue", linewidth=1, label="body 0")
#ax.semilogy(cumulative_time, mag1, color="pink", linewidth=1, label="body 1")
#ax.semilogy(cumulative_time, mag2, color="green", linewidth=1, label="body 2")

#ax.set_xlabel("simulation time t [–]")
#ax.set_ylabel("position magnitude |r| [–]")
#ax.set_title("loopendedtriangles (log)")
#ax.legend()
#plt.tight_layout()
#plt.show()

# Hyperradius definition from:
# Šuvakov & Dmitrašinović (2013), "Three Classes of Newtonian Three-Body Planar Periodic Orbits"
# arXiv:1303.0181, eq. used: R = sqrt(|r1|^2 + |r2|^2 + |r3|^2)

# hyperradius: overall size of the three-body system
#hyperradius = np.sqrt(mag0**2 + mag1**2 + mag2**2)
hyperradius_orig = np.sqrt(mag_orig_0**2 + mag_orig_1**2 + mag_orig_2**2)
hyperradius_perturbed = np.sqrt(mag_perturbed_0**2 + mag_perturbed_1**2 + mag_perturbed_2**2)
hyperradius_subtracted = np.sqrt(mag_subtracted_0**2 + mag_subtracted_1**2 + mag_subtracted_2**2)

fig, ax = plt.subplots(figsize=(10, 5))
ax.semilogy(cumulative_time, hyperradius_orig, color="blue", linewidth=1, label="Original")
ax.semilogy(cumulative_time, hyperradius_perturbed, color="orange", linewidth=1, label="Perturbed")
ax.semilogy(cumulative_time, hyperradius_subtracted, color="green", linewidth=1, label="Subtracted")
#ax.semilogy(cumulative_time, hyperradius, color="pink", linewidth=1)

ax.set_xlabel("simulation time t (dt)")
ax.set_ylabel("hyperradius R (log)")
ax.set_title("trajectory r^3 over timestep dt in configuration with and without perturbation")
# the subtitle should include only the name of the configuration without perturbation
ax.set_subtitle(f"{configuration}")
plt.tight_layout()
plt.show()'''

# trajectory over time
# at the moment adjusted for just one
import numpy as np
import matplotlib.pyplot as plt
import os

base_dir = r"C:\Users\kaisa\My Drive\Simulated_Data"
dataset_names = ["figure8", "brouckeA2", "loopendedtriangles", "ovalswithflourishes", "orbit_O2", "orbit_O3", "orbit_O26"]

for name in dataset_names:
    # Construct file paths
    original_files = [
        os.path.join(base_dir, f"{name}.csv"),
        os.path.join(base_dir, f"{name}add.csv"),
        os.path.join(base_dir, f"{name}sub.csv")
    ]
    timestep_file = os.path.join(base_dir, f"{name}_timestep_sizes.csv")
    
    # Load data
    original_bodies = [np.loadtxt(f, delimiter=",") for f in original_files]
    timesteps = np.loadtxt(timestep_file) #sus
    cumulative_time = np.cumsum(timesteps)
    
    # Compute magnitudes
    mags = [np.sqrt(b[:,0]**2 + b[:,1]**2 + b[:,2]**2) for b in original_bodies]
    
    # Compute hyperradius
    hyperradius = np.sqrt(mags[0]**2 + mags[1]**2 + mags[2]**2)
    
    plt.figure(figsize=(10,5))
    plt.semilogy(cumulative_time, hyperradius, color="purple", linewidth=1)
    plt.xlabel("timestep (dt)")
    plt.ylabel("hyperradius R (log)")
    plt.title(f"trajectory |r^3|=R over timestep dt in {name} with r1_x ±ε=1e-10")
    plt.tight_layout()

    # Save plot
    save_path = os.path.join(base_dir, f"{name}_hyperradius_plot.png")
    plt.savefig(save_path)
    plt.close()

    # trajectory error over time

def error()
    def compute_error_pct(orig_hr, perturbed_hr):
        error = np.abs(perturbed_hr - orig_hr)
        return np.where(orig_hr != 0, (error / orig_hr) * 100, 0)

    error_add = compute_error_pct(hyperradius_orig, hyperradius_add)
    error_sub = compute_error_pct(hyperradius_orig, hyperradius_sub)

    plt.figure(figsize=(10,5))
    plt.plot(cumulative_time, error_add, label='Add Perturbation Error %')
    plt.plot(cumulative_time, error_sub, label='Sub Perturbation Error %')
    plt.xlabel("timestep (dt)")
    plt.ylabel("Error Percentage (%)")
    plt.title(f"Trajectory Error R over timestep dt in {name}")
    plt.legend()
    plt.tight_layout()

    save_path_error = os.path.join(base_dir, f"{name}_hyperradius_error.png")
    plt.savefig(save_path_error)
    plt.close()