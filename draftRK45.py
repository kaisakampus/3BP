# the order is heavility inspired by RK45 code snippet from https://github.com/LBrink05/Project-Period-3D-Simulations-of-Multi-Body-Star-Systems

import numpy as np
from pathlib import Path
from scipy.integrate import RK45
import csv

# CONSTANTS
NUM_BODIES = 3

# setting cwd directory
CWDDIR = Path.cwd()

def Simulate(data_list, precision, duration):
    # extracting the data
    mass = np.array([data_list[1], data_list[4], data_list[7]], dtype=np.float64)
    start_pos = np.array([data_list[0], data_list[3], data_list[6],], dtype=np.float64)
    start_vel = np.array([data_list[2], data_list[5], data_list[8],], dtype=np.float64)

    timestep = float(precision)
    total_steps = int(duration * 24 / timestep) + 1  # ro include t=0

    sample_every = max(1, int(1 / timestep))

    frames, timestep_size_list = position_sampled(
        timestep, total_steps, sample_every,
        NUM_BODIES, start_pos, start_vel, mass
    )

    # save CSV files
    out_dir = CWDDIR / "Simulated_Data"
    out_dir.mkdir(parents=True, exist_ok=True)

    for body in range(NUM_BODIES):
        path = out_dir / f"body{body}.csv"
        np.savetxt(path, frames[body], delimiter=",")

    timestep_path = out_dir / "timestep_sizes.csv"
    np.savetxt(timestep_path, timestep_size_list, delimiter=",")


# some physics

def acceleration_components(pos, body, MASS, NUM_BODIES):
    ax = 0.0
    ay = 0.0
    az = 0.0

    px, py, pz = pos[body]
    '''px = prior_pos[body, 0]
    py = prior_pos[body, 1]
    pz = prior_pos[body, 2]'''

    for other in range(NUM_BODIES):
        if other != body:
            rx, ry, rz = pos[other] - np.array([px, py, pz])
            '''rx = prior_pos[other, 0] - px
            ry = prior_pos[other, 1] - py
            rz = prior_pos[other, 2] - pz'''

            # softening
            r2 = rx * rx + ry * ry + rz * rz + 0.001**2
            r3 = r2 ** 1.5

            ax += MASS[other] * rx / r3
            ay += MASS[other] * ry / r3
            az += MASS[other] * rz / r3

    return ax, ay, az


def ode_system(t, f, MASS, NUM_BODIES):

    #ODE function for scipy's solve_ivp.
    #f contains [pos_flat, vel_flat] for all bodies.

    pos = f[:3 * NUM_BODIES].reshape(NUM_BODIES, 3)
    vel = f[3 * NUM_BODIES:].reshape(NUM_BODIES, 3)

    acc = np.zeros((NUM_BODIES, 3), dtype=np.float64)

    for b in range(NUM_BODIES):
        acc[b] = acceleration_components(pos, b, MASS, NUM_BODIES)
        '''acc[b, 0] = ax
        acc[b, 1] = ay
        acc[b, 2] = az'''

    dydt = np.zeros_like(f)

    # dx/dt = v
    dydt[:3 * NUM_BODIES] = vel.flatten()

    # dv/dt = a
    dydt[3 * NUM_BODIES:] = acc.flatten()

    return dydt

# ACTUAL RK45 PART
# Runs the RK45 integrator and samples every SAMPLE_EVERY steps.
# Returns frames shaped (NUM_BODIES, OUT_STEPS, 6) with [x,y,z,vx,vy,vz].

def position_sampled(TIMESTEP, TOTAL_STEPS, SAMPLE_EVERY, NUM_BODIES, START_POS, START_VEL, MASS):

    # timeline of all integration points
    t0 = 0.0
    t_end = (TOTAL_STEPS - 1) * TIMESTEP

    # Initial state vector
    f0 = np.concatenate([START_POS.flatten(), START_VEL.flatten()])

    solver = RK45(
        fun=lambda t, y: ode_system(t, y, MASS, NUM_BODIES),
        t0=t0,
        y0=f0,
        t_bound=t_end,
        rtol=1e-9,
        atol=1e-12,
        max_step=TIMESTEP # smaller steps than timestep, adaptive
    )

    states = []
    times = []
    step_count = 0

    while solver.status == 'running':
        solver.step()

        # for animaton save every other step
        if step_count % SAMPLE_EVERY == 0:
            states.append(solver.y.copy())
            times.append(solver.t)

        step_count += 1

# first version
    # Extract positions and velocities

    # Convert to arrays
    states = np.array(states)   # (T, 6*N)
    times = np.array(times)

    # Reshape to (NUM_BODIES, T, 6)
    states = states.reshape(-1, NUM_BODIES, 6) # (T, N, 6)
    frames = states.transpose(1, 0, 2) # (N, T, 6)

    '''# from the other version
    # result.y shape: (6*NUM_BODIES, len(t_eval))
    pos = result.y[:3 * NUM_BODIES].reshape(NUM_BODIES, 3, -1).transpose(0, 2, 1)
    vel = result.y[3 * NUM_BODIES:].reshape(NUM_BODIES, 3, -1).transpose(0, 2, 1)

    # Build frames array: (NUM_BODIES, OUT_STEPS, 6)
    actual_out_steps = pos.shape[1] # shape: (time, 6*N)
    frames = np.zeros((NUM_BODIES, actual_out_steps, 6), dtype=np.float64)
    frames[:, :, 0:3] = pos
    frames[:, :, 3:6] = vel'''


    # timestep sizes (important for animation timing)
    timestep_size_list = np.zeros(len(times), dtype=np.float64)

# initial version
    '''timestep_size_list[0] = TIMESTEP * SAMPLE_EVERY  # first frame
    if actual_out_steps > 1:
        timestep_size_list[1:] = np.diff(result.t)'''

# the other version
    if len(times) > 1:
        timestep_size_list[1:] = np.diff(times)
        timestep_size_list[0] = timestep_size_list[1]
    else:
        timestep_size_list[0] = TIMESTEP

    return frames, timestep_size_list

# Convert to Python floats immediately
rt32 = float(np.sqrt(3)/2)
v = float(np.sqrt(1/(5*np.sqrt(3))))
rt32_times_5 = float(rt32 * 5)
v_times_rt32 = float(v * rt32)
v_div_2 = float(v / 2)

# Create the list with pre-computed float values
stable1 = [
    (5, 0, 0),
    1.0,
    (0.0, v, 0.0),
    (-2.5, rt32_times_5, 0.0),
    1.0,
    (-v_times_rt32, -v_div_2, 0.0),
    (-2.5, -rt32_times_5, 0.0),
    1.0,
    (v_times_rt32, -v_div_2, 0.0),
    "Equilateral Triangle"
]

print(stable1)