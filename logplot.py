import numpy as np
import matplotlib.pyplot as plt

base = r"C:\Users\kaisa\My Drive\Simulated_Data\ovalswithflourishes"
body0 = np.loadtxt(base + "_body0.csv", delimiter=",")
body1 = np.loadtxt(base + "_body1.csv", delimiter=",")
body2 = np.loadtxt(base + "_body2.csv", delimiter=",")

timesteps = np.loadtxt(base + "_timestep_sizes.csv")
cumulative_time = np.cumsum(timesteps)

# magnitude of position vector for each body
mag0 = np.sqrt(body0[:, 0]**2 + body0[:, 1]**2)
mag1 = np.sqrt(body1[:, 0]**2 + body1[:, 1]**2)
mag2 = np.sqrt(body2[:, 0]**2 + body2[:, 1]**2)

fig, ax = plt.subplots(figsize=(10, 5))

ax.semilogy(cumulative_time, mag0, color="blue", linewidth=1, label="body 0")
ax.semilogy(cumulative_time, mag1, color="pink", linewidth=1, label="body 1")
ax.semilogy(cumulative_time, mag2, color="green", linewidth=1, label="body 2")

ax.set_xlabel("simulation time t [–]")
ax.set_ylabel("position magnitude |r| [–]")
ax.set_title("ovals with flourishes (log)")
ax.legend()
plt.tight_layout()
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Hyperradius definition from:
# Šuvakov & Dmitrašinović (2013), "Three Classes of Newtonian Three-Body Planar Periodic Orbits"
# arXiv:1303.0181, eq. used: R = sqrt(|r1|^2 + |r2|^2 + |r3|^2)

# hyperradius: overall size of the three-body system
hyperradius = np.sqrt(mag0**2 + mag1**2 + mag2**2)

fig, ax = plt.subplots(figsize=(10, 5))

ax.semilogy(cumulative_time, hyperradius, color="pink", linewidth=1)

ax.set_xlabel("simulation time t [–]")
ax.set_ylabel("hyperradius R [–]")
ax.set_title("log total of ovals with flourishes")
plt.tight_layout()
plt.show()