import numpy as np

# Softening constant - MUST match the simulation (see acceleration_components)
SOFTENING = 0.001

# Output interval from simulation - frames are saved at fixed intervals of out_dt
OUTPUT_DT = 1.0  # simulation time units between output frames


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

def calculate_trajectory_error(reference_data, simulated_data, frame_idx):
    ref_vec = []
    sim_vec = []
    
    for ref_body, sim_body in zip(reference_data, simulated_data):
        if frame_idx < len(ref_body) and frame_idx < len(sim_body):
            ref_vec.extend(ref_body[frame_idx])
            sim_vec.extend(sim_body[frame_idx])
    
    ref_vec = np.array(ref_vec)
    sim_vec = np.array(sim_vec)
    
    ref_norm = np.linalg.norm(ref_vec)
    if ref_norm == 0:
        return float('inf')
    
    diff_norm = np.linalg.norm(ref_vec - sim_vec)
    return (diff_norm / ref_norm) * 100.0


def calculate_hamiltonian(phase_space_data, masses, G=1.0, softening=SOFTENING):
    """
    Calculate the Hamiltonian (total energy) of the system.
    Uses Plummer softening: phi = -Gm/sqrt(r^2 + eps^2)
    This MUST match the simulation's force law.
    """
    num_bodies = len(phase_space_data)
    
    # Kinetic energy: T = (1/2) * sum m_i * v_i^2
    T = 0.0
    for i in range(num_bodies):
        pos_vel = phase_space_data[i]
        vx, vy, vz = pos_vel[3], pos_vel[4], pos_vel[5]
        v_squared = vx**2 + vy**2 + vz**2
        T += 0.5 * masses[i] * v_squared
    
    # Potential energy with softening
    V = 0.0
    eps2 = softening * softening
    for i in range(num_bodies):
        for j in range(i + 1, num_bodies):
            xi, yi, zi = phase_space_data[i][0], phase_space_data[i][1], phase_space_data[i][2]
            xj, yj, zj = phase_space_data[j][0], phase_space_data[j][1], phase_space_data[j][2]
            
            dx = xj - xi
            dy = yj - yi
            dz = zj - zi
            
            r_soft = np.sqrt(dx**2 + dy**2 + dz**2 + eps2)
            V -= G * masses[i] * masses[j] / r_soft
    
    return T + V


def calculate_hamiltonian_error(simulated_data, masses, initial_H, frame_idx, G=1.0, softening=SOFTENING):
    current_state = []
    for body_data in simulated_data:
        if frame_idx < len(body_data):
            current_state.append(body_data[frame_idx])
        else:
            return float('inf')
    
    H_current = calculate_hamiltonian(current_state, masses, G, softening)
    delta_H = abs(H_current - initial_H)
    
    if abs(initial_H) < 1e-10:
        return float('inf')
    
    return (delta_H / abs(initial_H)) * 100.0


'''def error_function(reference_data, simulated_data, masses):
    initial_state = [body_data[0] for body_data in simulated_data]
    initial_H = calculate_hamiltonian(initial_state, masses)
    
    def error_at_time(t):
        frame_idx = int(t)
        traj_error = calculate_trajectory_error(reference_data, simulated_data, frame_idx)
        ham_error = calculate_hamiltonian_error(simulated_data, masses, initial_H, frame_idx)
        return traj_error, ham_error
    
    return error_at_time


def calculate_max_error(errors, dt=1.0):
    errors_array = np.array(errors)
    finite_errors = errors_array[np.isfinite(errors_array)]
    
    if len(finite_errors) == 0:
        return float('inf')
    
    return finite_errors.max()'''