# taken from https://prappleizer.github.io/Tutorials/RK4/RK4_Tutorial.html

# content of all body files [x, y, z, vx, vy, vz]

import numpy as np
import matplotlib.pyplot as plt

# load all three bodies [x, y, z, vx, vy, vz]
base = r"C:\Users\kaisa\My Drive\Simulated_Data\panio_trio_O50_04_LAST"
body0 = np.loadtxt(base + "_body0.csv", delimiter=",")
body1 = np.loadtxt(base + "_body1.csv", delimiter=",")
body2 = np.loadtxt(base + "_body2.csv", delimiter=",")

fig, ax = plt.subplots(figsize=(8, 8))

ax.plot(body0[:, 0], body0[:, 1], color="blue", linewidth=1, label="body 0")
ax.plot(body1[:, 0], body1[:, 1], color="pink",    linewidth=1, label="body 1")
ax.plot(body2[:, 0], body2[:, 1], color="green", linewidth=1, label="body 2")

# mark starting positions
ax.scatter(body0[0, 0], body0[0, 1], color="darkblue", s=40, zorder=5)
ax.scatter(body1[0, 0], body1[0, 1], color="red",    s=40, zorder=5)
ax.scatter(body2[0, 0], body2[0, 1], color="darkgreen", s=40, zorder=5)

ax.set_xlabel("x [–]")
ax.set_ylabel("y [–]")
ax.set_title("O50 in 2D")
ax.set_aspect("equal")
ax.legend()
plt.tight_layout()
plt.show()