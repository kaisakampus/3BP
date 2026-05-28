import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# load all three bodies [x, y, z, vx, vy, vz]
base = r"C:\Users\kaisa\My Drive\Simulated_Data\ovalswithflourisheslowermax"
body0 = np.loadtxt(base + "_body0.csv", delimiter=",")
body1 = np.loadtxt(base + "_body1.csv", delimiter=",")
body2 = np.loadtxt(base + "_body2.csv", delimiter=",")

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot(body0[:, 0], body0[:, 1], body0[:, 2], color="blue",  linewidth=1, label="body 0")
ax.plot(body1[:, 0], body1[:, 1], body1[:, 2], color="pink",  linewidth=1, label="body 1")
ax.plot(body2[:, 0], body2[:, 1], body2[:, 2], color="green", linewidth=1, label="body 2")

# mark starting positions
ax.scatter(body0[0, 0], body0[0, 1], body0[0, 2], color="darkblue",  s=40, zorder=5)
ax.scatter(body1[0, 0], body1[0, 1], body1[0, 2], color="red",       s=40, zorder=5)
ax.scatter(body2[0, 0], body2[0, 1], body2[0, 2], color="darkgreen", s=40, zorder=5)

ax.set_xlabel("x [–]")
ax.set_ylabel("y [–]")
ax.set_zlabel("z [–]")
ax.set_title("ovals with flourishes in 3D lower max")
ax.legend()

plt.tight_layout()
plt.show()