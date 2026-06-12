# taken from https://prappleizer.github.io/Tutorials/RK4/RK4_Tutorial.html

# content of all body files [x, y, z, vx, vy, vz]

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
# load all three bodies [x, y, z, vx, vy, vz]
base = r"C:\Users\kaisa\My Drive\Simulated_Data\butterflyI_LAST"
body0 = np.loadtxt(base + "_body0.csv", delimiter=",")
body1 = np.loadtxt(base + "_body1.csv", delimiter=",")
body2 = np.loadtxt(base + "_body2.csv", delimiter=",")
N = 20
body0 = body0[:N]
body1 = body1[:N]
body2 = body2[:N]

def smooth(x, y, n=2000, s=0.0001):
    tck, u = splprep([x, y], s=s)
    u_fine = np.linspace(0, 1, n)
    return splev(u_fine, tck)

fig, ax = plt.subplots(figsize=(8, 8))
x0, y0 = smooth(body0[:, 0], body0[:, 1])
x1, y1 = smooth(body1[:, 0], body1[:, 1])
x2, y2 = smooth(body2[:, 0], body2[:, 1])
ax.plot(x0, y0, color="blue", linewidth=1, label="body 0")
ax.plot(x1, y1, color="pink",    linewidth=1, label="body 1")
ax.plot(x2, y2, color="green", linewidth=1, label="body 2")
#ax.plot(body0[:, 0], body0[:, 1], color="blue", linewidth=1, label="body 0")
#ax.plot(body1[:, 0], body1[:, 1], color="pink",    linewidth=1, label="body 1")
#ax.plot(body2[:, 0], body2[:, 1], color="green", linewidth=1, label="body 2")

# mark starting positions
ax.scatter(body0[0, 0], body0[0, 1], color="darkblue", s=40, zorder=5)
ax.scatter(body1[0, 0], body1[0, 1], color="red",    s=40, zorder=5)
ax.scatter(body2[0, 0], body2[0, 1], color="darkgreen", s=40, zorder=5)

ax.set_xlabel("x [–]")
ax.set_ylabel("y [–]")
ax.set_title("Butterfly I in 2D")
ax.set_aspect("equal")
#ax.legend()
plt.tight_layout()
plt.show()