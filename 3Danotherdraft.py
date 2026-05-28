import matplotlib
matplotlib.use('TkAgg')   # separate popup window — install with: pip install pyqt5

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

base = r"C:\Users\kaisa\My Drive\Simulated_Data\ovalswithflourisheslowermax"
body0 = np.loadtxt(base + "_body0.csv", delimiter=",")
body1 = np.loadtxt(base + "_body1.csv", delimiter=",")
body2 = np.loadtxt(base + "_body2.csv", delimiter=",")

TRAIL = 150
STEP  = 3

fig = plt.figure(figsize=(10, 9))
ax  = fig.add_subplot(111, projection='3d')
fig.subplots_adjust(bottom=0.15)

all_x = np.concatenate([body0[:, 0], body1[:, 0], body2[:, 0]])
all_y = np.concatenate([body0[:, 1], body1[:, 1], body2[:, 1]])
xpad  = (all_x.max() - all_x.min()) * 0.1
ypad  = (all_y.max() - all_y.min()) * 0.1

ax.set_xlim(all_x.min() - xpad, all_x.max() + xpad)
ax.set_ylim(all_y.min() - ypad, all_y.max() + ypad)
ax.set_zlim(-1, 1)
ax.set_xlabel("x [–]")
ax.set_ylabel("y [–]")
ax.set_zlabel("z [–]")
ax.set_title("loopended triangles — 3D simulation")
ax.view_init(elev=25, azim=45)

# faint ghost of full orbit
ax.plot(body0[:, 0], body0[:, 1], body0[:, 2], color="blue",     lw=0.4, alpha=0.2)
ax.plot(body1[:, 0], body1[:, 1], body1[:, 2], color="deeppink", lw=0.4, alpha=0.2)
ax.plot(body2[:, 0], body2[:, 1], body2[:, 2], color="green",    lw=0.4, alpha=0.2)

# starting position markers
ax.scatter(body0[0, 0], body0[0, 1], body0[0, 2], color="darkblue",  s=60, marker='^', label="start 0")
ax.scatter(body1[0, 0], body1[0, 1], body1[0, 2], color="red",        s=60, marker='^', label="start 1")
ax.scatter(body2[0, 0], body2[0, 1], body2[0, 2], color="darkgreen",  s=60, marker='^', label="start 2")

# animated trails
trail0, = ax.plot([], [], [], color="blue",     lw=1.5, label="body 0")
trail1, = ax.plot([], [], [], color="deeppink", lw=1.5, label="body 1")
trail2, = ax.plot([], [], [], color="green",    lw=1.5, label="body 2")

# animated dots
dot0, = ax.plot([], [], [], 'o', color="darkblue",  ms=8, zorder=6)
dot1, = ax.plot([], [], [], 'o', color="red",        ms=8, zorder=6)
dot2, = ax.plot([], [], [], 'o', color="darkgreen",  ms=8, zorder=6)

ax.legend(loc="upper left")

N     = min(len(body0), len(body1), len(body2))
state = {"frame": 0, "paused": False}

def update(frame):
    if state["paused"]:
        return trail0, trail1, trail2, dot0, dot1, dot2

    f     = state["frame"]
    start = max(0, f - TRAIL)

    for trail, dot, body in [
        (trail0, dot0, body0),
        (trail1, dot1, body1),
        (trail2, dot2, body2),
    ]:
        trail.set_data(body[start:f, 0], body[start:f, 1])
        trail.set_3d_properties(body[start:f, 2])
        dot.set_data([body[f, 0]], [body[f, 1]])
        dot.set_3d_properties([body[f, 2]])

    state["frame"] = (f + STEP) % N
    return trail0, trail1, trail2, dot0, dot1, dot2

# buttons
ax_pause   = fig.add_axes([0.35, 0.04, 0.12, 0.05])
ax_restart = fig.add_axes([0.49, 0.04, 0.12, 0.05])
ax_quit    = fig.add_axes([0.63, 0.04, 0.12, 0.05])

btn_pause   = Button(ax_pause,   "Pause")
btn_restart = Button(ax_restart, "Restart")
btn_quit    = Button(ax_quit,    "Quit")

def on_pause(event):
    state["paused"] = not state["paused"]
    btn_pause.label.set_text("Resume" if state["paused"] else "Pause")
    fig.canvas.draw_idle()

def on_restart(event):
    state["frame"]  = 0
    state["paused"] = False
    btn_pause.label.set_text("Pause")
    fig.canvas.draw_idle()

def on_quit(event):
    plt.close(fig)

btn_pause.on_clicked(on_pause)
btn_restart.on_clicked(on_restart)
btn_quit.on_clicked(on_quit)

ani = FuncAnimation(fig, update, frames=N, interval=10, blit=False, repeat=True)

plt.show(block=True)