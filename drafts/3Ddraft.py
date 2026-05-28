import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.widgets import Button

base = r"C:\Users\kaisa\My Drive\Simulated_Data\loopendedtriangleslowermax"
body0 = np.loadtxt(base + "_body0.csv", delimiter=",")
body1 = np.loadtxt(base + "_body1.csv", delimiter=",")
body2 = np.loadtxt(base + "_body2.csv", delimiter=",")

TRAIL = 150
STEP  = 3

fig = plt.figure(figsize=(11, 9))
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

N = min(len(body0), len(body1), len(body2))
step_text = fig.text(0.78, 0.88, "step: 0 / {}".format(N),
                     fontsize=11, ha='left', va='top',
                     bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                               edgecolor='gray', alpha=0.8))

# animated trails
trail0, = ax.plot([], [], [], color="blue",     lw=1.5, label="body 0")
trail1, = ax.plot([], [], [], color="deeppink", lw=1.5, label="body 1")
trail2, = ax.plot([], [], [], color="green",    lw=1.5, label="body 2")

# animated dots
dot0, = ax.plot([], [], [], 'o', color="darkblue",  ms=8, zorder=6)
dot1, = ax.plot([], [], [], 'o', color="red",        ms=8, zorder=6)
dot2, = ax.plot([], [], [], 'o', color="darkgreen",  ms=8, zorder=6)

ax.legend(loc="upper left")

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

    step_text.set_text("step: {} / {}".format(f, N))
    state["frame"] = (f + STEP) % N
    return trail0, trail1, trail2, dot0, dot1, dot2

def on_scroll(event):
    scale = 0.9 if event.button == 'up' else 1.1
    xlim = ax.get_xlim3d()
    ylim = ax.get_ylim3d()
    zlim = ax.get_zlim3d()
    cx = (xlim[0] + xlim[1]) / 2
    cy = (ylim[0] + ylim[1]) / 2
    cz = (zlim[0] + zlim[1]) / 2
    ax.set_xlim3d([cx + (x - cx) * scale for x in xlim])
    ax.set_ylim3d([cy + (y - cy) * scale for y in ylim])
    ax.set_zlim3d([cz + (z - cz) * scale for z in zlim])
    fig.canvas.draw_idle()

fig.canvas.mpl_connect('scroll_event', on_scroll)

# buttons
ax_pause   = fig.add_axes([0.25, 0.04, 0.12, 0.05])
ax_restart = fig.add_axes([0.39, 0.04, 0.12, 0.05])
ax_save    = fig.add_axes([0.53, 0.04, 0.12, 0.05])
ax_quit    = fig.add_axes([0.67, 0.04, 0.12, 0.05])

btn_pause   = Button(ax_pause,   "Pause")
btn_restart = Button(ax_restart, "Restart")
btn_save    = Button(ax_save,    "Save video")
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

def on_save(event):
    state["paused"] = True
    btn_pause.label.set_text("Resume")
    btn_save.label.set_text("Saving...")
    fig.canvas.draw_idle()

    def save_update(f):
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
        step_text.set_text("step: {} / {}".format(f, N))

    save_ani = FuncAnimation(fig, save_update, frames=range(0, N, STEP), blit=False)
    writer   = FFMpegWriter(fps=30, bitrate=1800)
    outpath  = base + "_simulation.mp4"
    save_ani.save(outpath, writer=writer)
    btn_save.label.set_text("Saved!")
    fig.canvas.draw_idle()

def on_quit(event):
    plt.close(fig)

btn_pause.on_clicked(on_pause)
btn_restart.on_clicked(on_restart)
btn_save.on_clicked(on_save)
btn_quit.on_clicked(on_quit)

ani = FuncAnimation(fig, update, frames=N, interval=10, blit=False, repeat=True)

plt.show(block=True)