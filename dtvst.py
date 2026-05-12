import numpy as np
import matplotlib.pyplot as plt

# load timestep sizes
timesteps = np.loadtxt(r"C:\Users\kaisa\My Drive\Simulated_Data\ovalswithflourishes_timestep_sizes.csv")

# cumulative time axis
cumulative_time = np.cumsum(timesteps)

plt.figure(figsize=(10, 4))
plt.plot(cumulative_time, timesteps, color="pink", linewidth=1)
plt.xlabel("simulation time [-]")
plt.ylabel("adaptive timestep size (dt) [-]")
plt.title("ovals with flourishes")
plt.tight_layout()
plt.show()