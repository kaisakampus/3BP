import numpy as np
import time
from pathlib import Path
from scipy.integrate import RK45

# initial conditions from https://arxiv.org/pdf/1303.0181
yarn = [(-1,0,0), 1, (0.55906, 0.34919, 0),(1,0,0),  1, (0.55906, 0.34919, 0),(0,0,0),  1, (-1.11812, -0.69838, 0)]

NUM_BODIES = 3

def Simulate(data_list, precision, run_name):
    # extracting the initial coniditons from the configuration line
    # with float64 no calculation can be more precise than 16 decimal digits
    mass = np.array([data_list[1], data_list[4], data_list[7]], dtype=np.float64)
    start_pos = np.array([data_list[0], data_list[3], data_list[6],], dtype=np.float64)
    start_vel = np.array([data_list[2], data_list[5], data_list[8],], dtype=np.float64)

    print("mass:", mass)
    print("start_pos:", start_pos)
    print("start_vel:", start_vel)

    # conditions for time and frames
    timestep = float(precision)
    #total_steps = int(duration * 24 / timestep) + 1  # to include t=0
    sample_every = max(1, int(1 / timestep))

    # the saved frames should correspond to the sampled position
    frames, timestep_size_list = position_sampled(
        sample_every, NUM_BODIES, start_pos, start_vel, mass)

    # save CSV files to computer folder Simulated_Data
    PATH_FILES = Path(r"C:\Users\kaisa\My Drive")
    my_dir = PATH_FILES / "Simulated_Data"
    my_dir.mkdir(parents=True, exist_ok=True)

    # all sampled coordinates of each body are stored
    for body in range(NUM_BODIES):
        path = my_dir / f"{run_name}_body{body}.csv"
        np.savetxt(path, frames[body], delimiter=",")
    # all sampled timesteps are stored
    timestep_path = my_dir / f"{run_name}_timestep_sizes.csv"
    np.savetxt(timestep_path, timestep_size_list, delimiter=",")
    
    return frames, timestep_size_list


# some physics
def acceleration_components(pos, body, MASS, NUM_BODIES):
    ax = 0.0
    ay = 0.0
    az = 0.0

    # position vector
    px = pos[body, 0]
    py = pos[body, 1]
    pz = pos[body, 2]

    for other in range(NUM_BODIES):
        if other != body: # change in position
            rx = pos[other, 0] - px
            ry = pos[other, 1] - py
            rz = pos[other, 2] - pz

            # softening because another code had it
            # i suppose this is to better regulate close encounters
            r2 = rx * rx + ry * ry + rz * rz #+ 0.001**2
            r3 = r2 ** 1.5

            # new acceleration
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

def position_sampled(SAMPLE_EVERY, NUM_BODIES, START_POS, START_VEL, MASS):

    # timeline of all integration points
    t0 = 0.0
    # fixed timestep
    # t_end = (TOTAL_STEPS - 1) * TIMESTEP

    # Initial state vector
    f0 = np.concatenate([START_POS.flatten(), START_VEL.flatten()])
    print("f0:", f0)
    print("f0 shape:", f0.shape)

    solver = RK45(
        fun=lambda t, y: ode_system(t, y, MASS, NUM_BODIES),
        t0=t0,
        y0=f0,
        t_bound=np.inf,
        rtol=1e-9,
        atol=1e-12,
        max_step=np.inf # adaptive timestep
    )

    states = []
    times = []
    step_count = 0

    COLLISION_THRESHOLD = 0.001   # bodies too close
    ESCAPE_THRESHOLD = 50.0     # bodies too far apart

    while solver.status == 'running':
        solver.step()

        if step_count == 0:
            print("solver.y at step 0:", solver.y)

        # print progress every x steps
        if step_count % 1000000 == 0:
            print(f"Step NR. {step_count}, time of run thus far = {solver.t:.4f}, timestep = {solver.h_abs:.6f}")
        
        pos = solver.y[:3 * NUM_BODIES].reshape(NUM_BODIES, 3)

        # check encounters between all pairs
        collapsed = False
        for i in range(NUM_BODIES):
            for j in range(i + 1, NUM_BODIES):
                dist = np.linalg.norm(pos[i] - pos[j])
                if dist < COLLISION_THRESHOLD:
                    print(f"Collision between body {i} and {j} at t={solver.t:.3f}")
                    collapsed = True
                if dist > ESCAPE_THRESHOLD:
                    print(f"Body {i} and {j} escaped at t={solver.t:.3f}")
                    collapsed = True

        if collapsed:
            break

        # for animaton save every other step
        if step_count % SAMPLE_EVERY == 0:
            states.append(solver.y.copy())
            times.append(solver.t)

        step_count += 1

    # Extract positions and velocities

    # Convert to arrays
    states = np.array(states)   # (T, 6*N)
    times = np.array(times)

    # Reshape to (NUM_BODIES, T, 6)
    # states = states.reshape(-1, NUM_BODIES, 6) # (T, N, 6)
    # frames = states.transpose(1, 0, 2) # (N, T, 6)

    pos_all = states[:, :9].reshape(-1, NUM_BODIES, 3)    # (T, N, 3)
    vel_all = states[:, 9:].reshape(-1, NUM_BODIES, 3)    # (T, N, 3)
    combined = np.concatenate([pos_all, vel_all], axis=2)  # (T, N, 6)
    frames = combined.transpose(1, 0, 2)                   # (N, T, 6)

# difference (adaptive timestep)= times[i] - times[i-1]
# step sizes chosen control its step size to maintain
# the error tolerances rtol=1e-9, atol=1e-12
    # timestep sizes (important for animation timing)
    timestep_size_list = np.concatenate([[0], np.diff(times)])

    return frames, timestep_size_list

# structuring the data in body files
def read_phase_space(NUM_BODIES, path, run_name):
    
    phase_space_data = []
    
    for b in range(NUM_BODIES):
        path_b = str(path) + f"/{run_name}_body{b}.csv"
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

print(f"yarn")
start = time.time()
# 1 simulation time unit is like 200 internal steps with dt=0.005
frames, timesteps = Simulate(yarn, 0.005, "yarn")
end = time.time()

#path = Path.cwd() / "Simulated_Data"
path = Path(r"C:\Users\kaisa\My Drive\Simulated_Data")

sim_data = read_phase_space(NUM_BODIES, path, "yarn")
print(f"Simulation computations lasted {end - start:.2f} s")
print(f"Total timesteps: {len(timesteps)}")

print("\n output of 10 rows for each body")
for body in range(NUM_BODIES):
    print(f"\nyarn_Body {body}:")
    print(frames[body][:10])

print("\n output of 10 rows of timestep sizes")
timestep_path = path / "yarn_timestep_sizes.csv"
with open(timestep_path, "r") as f:
    for i, line in enumerate(f):
        if i >= 10:
            break
        print(line, end="")