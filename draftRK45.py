# the order is heavily inspired by RK45 code snippet from https://github.com/LBrink05/Project-Period-3D-Simulations-of-Multi-Body-Star-Systems

import numpy as np
from pathlib import Path
from scipy.integrate import RK45

# initial conditions
figure8 = [(2.57429,0,0),1,(0.216343,0.332029,0),(-2.57429,0,0),1,(0.216343,0.332029,0),(0,0,0),1,(-0.432686,-0.664058,0)]
yarn = [(-7.17921,0,0),1,(0.208677,0.130401,0),(7.17921,0,0),1,(0.208677,0.130401,0),(0,0,0),1,(-0.417354,-0.260802,0)]
yinyang = [(-8.57406,0,0),1,(0.175521,0.104039,0),(8.57406,0,0),1,(0.175521,0.104039,0),(0,0,0),1,(-0.351042,-0.208078,0)]

NUM_BODIES = 3
# Output interval from simulation - frames are saved at fixed intervals of out_dt
OUTPUT_DT = 1.0  # simulation time units between output frames

def Simulate(data_list, precision, duration):
    # extracting the data
    mass = np.array([data_list[1], data_list[4], data_list[7]], dtype=np.float64)
    start_pos = np.array([data_list[0], data_list[3], data_list[6],], dtype=np.float64)
    start_vel = np.array([data_list[2], data_list[5], data_list[8],], dtype=np.float64)

    timestep = float(precision)
    total_steps = int(duration * 24 / timestep) + 1  # to include t=0

    sample_every = max(1, int(1 / timestep))

    frames, timestep_size_list = position_sampled(
        timestep, total_steps, sample_every,
        NUM_BODIES, start_pos, start_vel, mass
    )

    # save CSV files to github repository kaisakampus/3BP
    PATH_FILES = Path.cwd()
    my_dir = PATH_FILES / "Simulated_Data"
    my_dir.mkdir(parents=True, exist_ok=True)

    for body in range(NUM_BODIES):
        path = my_dir / f"body{body}.csv"
        np.savetxt(path, frames[body], delimiter=",")

    timestep_path = my_dir / "timestep_sizes.csv"
    np.savetxt(timestep_path, timestep_size_list, delimiter=",")

    return frames, timestep_size_list


# some physics
def acceleration_components(pos, body, MASS, NUM_BODIES):
    ax = 0.0
    ay = 0.0
    az = 0.0

    px = pos[body, 0]
    py = pos[body, 1]
    pz = pos[body, 2]

    for other in range(NUM_BODIES):
        if other != body:
            rx = pos[other, 0] - px
            ry = pos[other, 1] - py
            rz = pos[other, 2] - pz

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
        max_step=np.inf # adaptive
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

    # timestep sizes (important for animation timing)
    timestep_size_list = np.arange(1, len(times) + 1)

    #timestep_size_list = np.zeros(len(times), dtype=np.float64)

# the other version - WHAT IN THE WORLD IS HAPPENING HERE
    #if len(times) > 1:
        #timestep_size_list[1:] = np.diff(times)
        #timestep_size_list[0] = timestep_size_list[1]
    #else:
        #timestep_size_list[0] = TIMESTEP

    return frames, timestep_size_list

# structuring the data in body files
def read_phase_space(NUM_BODIES, path):
    
    phase_space_data = []
    
    for b in range(NUM_BODIES):
        path_b = str(path) + f"/body{b}.csv"
        body_data = []
        
        with open(path_b, "r") as data:
            for line in data:
                values = line.strip().split(",")
                if len(values) >= 6:
                    # [x, y, z, vx, vy, vz]
                    body_data.append([
                        float(values[0]), float(values[1]), float(values[2]),
                        float(values[3]), float(values[4]), float(values[5])
                    ])
        
        phase_space_data.append(np.array(body_data))
    
    return phase_space_data

frames, timesteps = Simulate(figure8, 0.005, 100)
path = Path.cwd() / "Simulated_Data"
sim_data = read_phase_space(NUM_BODIES, path)

print("\n output of 10 rows for each body")
for body in range(NUM_BODIES):
    print(f"\nBody {body}:")
    print(frames[body][:10])