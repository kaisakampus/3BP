import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.widgets import Button
from matplotlib.lines import Line2D
import time

base = r"C:\Users\kaisa\My Drive\Simulated_Data\loopendedtriangleslowermax"
body0 = np.loadtxt(base + "_body0.csv", delimiter=",")
body1 = np.loadtxt(base + "_body1.csv", delimiter=",")
body2 = np.loadtxt(base + "_body2.csv", delimiter=",")

TRAIL = 80
N_SEG = 30

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
ax.set_title("loopended triangles in 3D simulation")
ax.view_init(elev=25, azim=45)

N = min(len(body0), len(body1), len(body2))

info_text = fig.text(0.76, 0.88,
                     "step:  0 / {}\nT    = 0.00s\nspeed = 3".format(N),
                     fontsize=11, ha='left', va='top', family='monospace',
                     bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                               edgecolor='gray', alpha=0.8))

# fading trail segments
trail_segs0 = [ax.plot([], [], [], color="turquoise",     lw=1, alpha=(i+1)/N_SEG)[0] for i in range(N_SEG)]
trail_segs1 = [ax.plot([], [], [], color="deeppink", lw=1, alpha=(i+1)/N_SEG)[0] for i in range(N_SEG)]
trail_segs2 = [ax.plot([], [], [], color="lime",    lw=1, alpha=(i+1)/N_SEG)[0] for i in range(N_SEG)]

# animated dots
dot0, = ax.plot([], [], [], 'o', color="deepskyblue",  ms=4, zorder=6)
dot1, = ax.plot([], [], [], 'o', color="red",        ms=4, zorder=6)
dot2, = ax.plot([], [], [], 'o', color="lightgreen",  ms=4, zorder=6)

# legend
legend_elements = [
    Line2D([0], [0], color='turquoise',     lw=1.5, label='body 0'),
    Line2D([0], [0], color='deeppink', lw=1.5, label='body 1'),
    Line2D([0], [0], color='lime',    lw=1.5, label='body 2'),
]
ax.legend(handles=legend_elements, loc="upper left", fontsize=9)

# state
state          = {"frame": 0, "paused": False, "step": 3}
sim_start_time = None
pause_start    = None
total_paused   = 0.0

def update(frame):
    global sim_start_time, pause_start, total_paused

    if state["paused"]:
        return []

    if sim_start_time is None:
        sim_start_time = time.time()

    f       = state["frame"]
    start   = max(0, f - TRAIL)
    seg_len = max(1, (f - start) // N_SEG)
    elapsed = time.time() - sim_start_time - total_paused

    for segs, dot, body in [
        (trail_segs0, dot0, body0),
        (trail_segs1, dot1, body1),
        (trail_segs2, dot2, body2),
    ]:
        for i, seg in enumerate(segs):
            s = start + i * seg_len
            e = start + (i + 1) * seg_len + 1
            if s >= f:
                seg.set_data([], [])
                seg.set_3d_properties([])
            else:
                seg.set_data(body[s:e, 0], body[s:e, 1])
                seg.set_3d_properties(body[s:e, 2])

        dot.set_data([body[f, 0]], [body[f, 1]])
        dot.set_3d_properties([body[f, 2]])

    info_text.set_text("step: {:>6} / {}\nT    = {:.2f}s\nspeed = {}".format(
        f, N, elapsed, state["step"]))

    state["frame"] = (f + state["step"]) % N
    return []

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
#ax_slower  = fig.add_axes([0.11, 0.04, 0.12, 0.05])
#ax_faster  = fig.add_axes([0.25, 0.04, 0.12, 0.05])
ax_pause   = fig.add_axes([0.39, 0.04, 0.12, 0.05])
ax_restart = fig.add_axes([0.53, 0.04, 0.12, 0.05])
ax_save    = fig.add_axes([0.67, 0.04, 0.12, 0.05])
#ax_quit    = fig.add_axes([0.81, 0.04, 0.12, 0.05])

#btn_slower  = Button(ax_slower,  "Slow")
#btn_faster  = Button(ax_faster,  "Fast")
btn_pause   = Button(ax_pause,   "Pause")
btn_restart = Button(ax_restart, "Restart")
btn_save    = Button(ax_save,    "Save")
#btn_quit    = Button(ax_quit,    "Quit")

def on_slower(event):
    state["step"] = max(1, state["step"] - 5)
    fig.canvas.draw_idle()

def on_faster(event):
    state["step"] = min(20, state["step"] + 1)
    fig.canvas.draw_idle()

def on_pause(event):
    global pause_start, total_paused
    state["paused"] = not state["paused"]
    if state["paused"]:
        pause_start = time.time()
        btn_pause.label.set_text("Resume")
    else:
        if pause_start is not None:
            total_paused += time.time() - pause_start
        btn_pause.label.set_text("Pause")
    fig.canvas.draw_idle()

def on_restart(event):
    global sim_start_time, pause_start, total_paused
    state["frame"]  = 0
    state["paused"] = False
    state["step"]   = 3
    sim_start_time  = None
    pause_start     = None
    total_paused    = 0.0
    btn_pause.label.set_text("Pause")
    fig.canvas.draw_idle()

def on_save(event):
    global pause_start, total_paused
    state["paused"] = True
    pause_start     = time.time()
    btn_pause.label.set_text("Resume")
    btn_save.label.set_text("Saving...")
    fig.canvas.draw_idle()

    def save_update(f):
        start   = max(0, f - TRAIL)
        seg_len = max(1, (f - start) // N_SEG)
        for segs, dot, body in [
            (trail_segs0, dot0, body0),
            (trail_segs1, dot1, body1),
            (trail_segs2, dot2, body2),
        ]:
            for i, seg in enumerate(segs):
                s = start + i * seg_len
                e = start + (i + 1) * seg_len + 1
                if s >= f:
                    seg.set_data([], [])
                    seg.set_3d_properties([])
                else:
                    seg.set_data(body[s:e, 0], body[s:e, 1])
                    seg.set_3d_properties(body[s:e, 2])
            dot.set_data([body[f, 0]], [body[f, 1]])
            dot.set_3d_properties([body[f, 2]])
        info_text.set_text("step: {:>6} / {}\nT    = saving...\nspeed = {}".format(
            f, N, state["step"]))

    save_ani = FuncAnimation(fig, save_update, frames=range(0, N, state["step"]), blit=False)
    writer   = FFMpegWriter(fps=30, bitrate=1800)
    outpath  = base + "_simulation.mp4"
    save_ani.save(outpath, writer=writer)
    btn_save.label.set_text("Saved!")
    fig.canvas.draw_idle()

def on_quit(event):
    plt.close(fig)

#btn_slower.on_clicked(on_slower)
#btn_faster.on_clicked(on_faster)
btn_pause.on_clicked(on_pause)
btn_restart.on_clicked(on_restart)
btn_save.on_clicked(on_save)
#btn_quit.on_clicked(on_quit)

ani = FuncAnimation(fig, update, frames=N, interval=400, blit=False, repeat=True)

plt.show(block=True)