# the order is heavily inspired by RK45 code snippet from https://github.com/LBrink05/Project-Period-3D-Simulations-of-Multi-Body-Star-Systems
import numpy as np
import time
from pathlib import Path
from scipy.integrate import RK45

eps = 1e-10 # i use this large epsilon because i have dimensionless units and machine epsilon is insignificant in results

# initial conditions https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
#figure8 = [(-1,0,0),1,(0.3471168881,0.5327249454,0),(1,0,0),1,(0.3471168881,0.5327249454,0),(0,0,0),1,(-0.6942337762,-1.0654498908,0)]
#figure8add = [(-1+eps,0,0),1,(0.3471168881,0.5327249454,0),(1,0,0),1,(0.3471168881,0.5327249454,0),(0,0,0),1,(-0.6942337762,-1.0654498908,0)]
#figure8sub = [(-1-eps,0,0),1,(0.3471168881,0.5327249454,0),(1,0,0),1,(0.3471168881,0.5327249454,0),(0,0,0),1,(-0.6942337762,-1.0654498908,0)]
brouckeA1 = [(-0.9892620043,0,0),1,(0,1.9169244185,0),(2.2096177241,0,0),1,(0,0.1910268738,0),(-1.2203557197,0,0),1,(0,-2.1079512924,0)]
brouckeA1add = [((-0.9892620043 + eps),0,0),1,(0,1.9169244185,0),(2.2096177241,0,0),1,(0,0.1910268738,0),(-1.2203557197,0,0),1,(0,-2.1079512924,0)]
brouckeA1sub = [((-0.9892620043 - eps),0,0),1,(0,1.9169244185,0),(2.2096177241,0,0),1,(0,0.1910268738,0),(-1.2203557197,0,0),1,(0,-2.1079512924,0)]
# initial conditions from https://arxiv.org/pdf/1303.0181
butterflyI = [(-1,0,0),1,(0.30689,0.12551,0.0),(1,0,0),1,(0.30689,0.12551,0.0),(0,0,0),1,(-0.61378, -0.25102, 0)]
# initial conditions from https://numericaltank.sjtu.edu.cn/three-body/three-body.htm
orbit_O2 = [(-1,0,0),1,(-0.272600007460296,-0.432093711947155,0.629473407171139),(1,0,0),1,(-0.272600007460296,-0.432093711947155,-0.629473407171139),(0,0,1.02200578272669),1.2,(0.454333345767160,0.720156186578592,0.0)]
orbit_O3 = [(-1,0,0),1,(0.402136910074724,0.180356951286259,0.210445128137873),(1,0,0),1,(0.402136910074724,0.180356951286259,-0.210445128137873),(0,0,0.476878264280312),1,(-0.804273820149448,-0.360713902572518,0.0)]

#MORE POSSIBLE 3D https://link.springer.com/article/10.1007/BF01595390
NUM_BODIES = 3

def Simulate(data_list, precision, run_name):
    # extracting the initial coniditons from the configuration line
    # with float64 no calculation can be more precise than 16 decimal digits
    mass = np.array([data_list[1], data_list[4], data_list[7]], dtype=np.float64)
    start_pos = np.array([data_list[0], data_list[3], data_list[6],], dtype=np.float64)
    start_vel = np.array([data_list[2], data_list[5], data_list[8],], dtype=np.float64)

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
            r2 = rx * rx + ry * ry + rz * rz #+ 0.01**2
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

    solver = RK45(
        fun=lambda t, y: ode_system(t, y, MASS, NUM_BODIES),
        t0=t0,
        y0=f0,
        t_bound=10000, # used to be np.inf and 50
        rtol=3.162e-12, #1e-9
        atol=1e-12, #1e-13 can be both when fixed
        max_step=np.inf # adaptive timestep
    )

    states = []
    times = []
    step_count = 0

    COLLISION_THRESHOLD = 0.0001   # bodies too close
    ESCAPE_THRESHOLD = 100.0     # bodies too far apart

    while solver.status == 'running':
        solver.step()

        # enforce planar orbit - zero out z drift (numerical artifact)
        '''y = solver.y.copy()
        for b in range(NUM_BODIES):
            y[b * 3 + 2] = 0.0                      # z position
            y[3 * NUM_BODIES + b * 3 + 2] = 0.0    # z velocity
        solver._y = y'''

        # print progress every 1000 steps
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

# first version
    # Extract positions and velocities

    # Convert to arrays
    states = np.array(states)   # (T, 6*N)
    times = np.array(times)

#chatgpt begins
    T = len(states)

    pos = states[:, :3*NUM_BODIES].reshape(T, NUM_BODIES, 3)
    vel = states[:, 3*NUM_BODIES:].reshape(T, NUM_BODIES, 3)

    frames = np.concatenate([pos, vel], axis=2)   # (T, N, 6)
    frames = frames.transpose(1, 0, 2)            # (N, T, 6)

#chatgpt ends
# the original is lines 191-192
    # Reshape to (NUM_BODIES, T, 6)
    #states = states.reshape(-1, NUM_BODIES, 6) # (T, N, 6)
    #frames = states.transpose(1, 0, 2) # (N, T, 6)

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

print(f"O2")
start = time.time()
# 1 simulation time unit is like 200 internal steps with dt=0.005
frames, timesteps = Simulate(orbit_O2, 0.005, "orbit_O2")
end = time.time()

#path = Path.cwd() / "Simulated_Data"
path = Path(r"C:\Users\kaisa\My Drive\Simulated_Data")

sim_data = read_phase_space(NUM_BODIES, path, "orbit_O2")
print(f"Simulation computations lasted {end - start:.2f} s")
print(f"Total timesteps: {len(timesteps)}")

print("\n output of 10 rows for each body")
for body in range(NUM_BODIES):
    print(f"\norbit_O2_Body {body}:")
    print(frames[body][:10])

print("\n output of 10 rows of timestep sizes")
timestep_path = path / "orbit_O2_timestep_sizes.csv"
with open(timestep_path, "r") as f:
    for i, line in enumerate(f):
        if i >= 10:
            break
        print(line, end="")

print(f"O3")
start = time.time()
frames, timesteps = Simulate(orbit_O3, 0.005, "orbit_O3")
end = time.time()

#path = Path.cwd() / "Simulated_Data"

sim_data = read_phase_space(NUM_BODIES, path, "orbit_O3")
print(f"Simulation computations lasted {end - start:.2f} s")
print(f"Total timesteps: {len(timesteps)}")

print("\n output of 10 rows for each body")
for body in range(NUM_BODIES):
    print(f"\norbit_O3_Body {body}:")
    print(frames[body][:10])

print("\n output of 10 rows of timestep sizes")
timestep_path = path / "orbit_O3_timestep_sizes.csv"
with open(timestep_path, "r") as f:
    for i, line in enumerate(f):
        if i >= 10:
            break
        print(line, end="")

'''print(f"broucke A1 subtracted perturbation")
start = time.time()
frames, timesteps = Simulate(brouckeA1sub, 0.005, "brouckeA1sub")
end = time.time()

#path = Path.cwd() / "Simulated_Data"

sim_data = read_phase_space(NUM_BODIES, path, "brouckeA1sub")
print(f"Simulation computations lasted {end - start:.2f} s")
print(f"Total timesteps: {len(timesteps)}")

print("\n output of 10 rows for each body")
for body in range(NUM_BODIES):
    print(f"\nbrouckeA1sub_Body {body}:")
    print(frames[body][:10])

print("\n output of 10 rows of timestep sizes")
timestep_path = path / "brouckeA1sub_timestep_sizes.csv"
with open(timestep_path, "r") as f:
    for i, line in enumerate(f):
        if i >= 10:
            break
        print(line, end="")'''