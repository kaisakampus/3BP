import matplotlib
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib import colors as mcolors
matplotlib.use("tkagg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

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

'''def calculate_totE(phase_space_data, masses, G=1.0, softening=SOFTENING): # Uses Plummer softening: phi = -Gm/sqrt(r^2 + eps^2)
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

def calculate_totE_error(simulated_data, masses, initial_H, frame_idx, G=1.0, softening=SOFTENING):
    current_state = []
    for body_data in simulated_data:
        if frame_idx < len(body_data):
            current_state.append(body_data[frame_idx])
        else:
            return float('inf')
    
    H_current = calculate_totE(current_state, masses, G, softening)
    delta_H = abs(H_current - initial_H)
    
    if abs(initial_H) < 1e-10:
        return float('inf')
    
    return (delta_H / abs(initial_H)) * 100.0'''

    # make sure that body.csv has been created for simulation data
    # visualisation of 3 body configuration simulation
    # stepsize vs time plot
    # original vs perturbation trajectory accuracy plot
    # energy fluctuations: When comparing perturbations, plot delta E relative to the original system

# GUI theme
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")
print(" \nCreating The Window\n")

class app(customtkinter.CTk):
    def __init__(self): # app self initiation process
        customtkinter.CTk.__init__(self)
        self.anim = None # lets animation run
        self.current_fig = None # lets plots appear in the window
        self.last_simulation_data = None  # stores last simulation info

        def on_closing(): # protocol to stop animation
            if self.anim is not None:
                self.anim.event_source.stop() #stops matplotlib plots from running in loop

            if self.current_fig is not None:
                plt.close(self.current_fig) # closing matplotlib figures

            plt.close('all')  # close any remaining figures

            # closing the window
            print("\nClosing The Window\n")
            self.quit()
            self.destroy()

        # protocol for closing the app
        self.protocol("WM_DELETE_WINDOW", on_closing)

        def get_path(body):
            if body == -1:
                path = Path(str(CWDDIR)) / "Simulated_Data"  # directory to body file(s)
            else:
                path = Path(str(CWDDIR)) / "Simulated_Data" / f"body{body}.csv"  # individual csv for each body
            return path

# simulation plot function
        def show_animation(duration):
            # CONSTANTS
            NUM_BODIES = len([f for f in os.listdir(get_path(-1)) if f.startswith('body') and f.endswith('.csv')])
            TRAIL = 200
            # length of timeline
            # TIMESTEP = 0.001 to 0.1
            with open(get_path(0), encoding="utf-8") as f:
                row_count = sum(1 for _ in f)

            TIMELINE = np.linspace(0, row_count, row_count)
            # read body positions for every frame from seperate csv files, one for each body
            frames = np.empty((NUM_BODIES, TIMELINE.size, 3), dtype=float)
            for body in range(0, NUM_BODIES):
                path = get_path(body)
                frames[body] = np.genfromtxt(path, delimiter=',')[:, :3]

            # plotting the data
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

            # showing time in animation
            plottime = 0
            timetext = ax.text2D(-0.30, 0.955, " t=" + str(plottime), transform=ax.transAxes, fontsize=24,
                                 color='black')

            # animation of trails & points (The fading trail was coded using ChatGPT)
            trail_cols = []
            trail_rgbs = []
            points = []

            for body in range(len(frames)):
                # make one fading trail collection per body
                lc = Line3DCollection([], linewidths=2)
                ax.add_collection3d(lc, autolim=False)
                trail_cols.append(lc)

                # store a per-body base color (use default cycle)
                base_color = ax._get_lines.get_next_color()
                trail_rgbs.append(mcolors.to_rgb(base_color))

                # head point (same color as trail)
                points.append(ax.plot([], [], [], 'o', markersize=4, color='red')[0])

            def update_data(frame):
                # go through every E.O.M frame by frame (motion has already been calculated)
                for body in range(len(frames)):
                    start = max(0, frame - TRAIL)
                    xyz = frames[body, start:frame + 1, :]  # (k,3)

                    if xyz.shape[0] < 2:
                        trail_cols[body].set_segments([])
                    else:
                        # segments: (k-1, 2, 3)
                        segs = np.stack([xyz[:-1], xyz[1:]], axis=1)
                        trail_cols[body].set_segments(segs)

                        nseg = segs.shape[0]
                        # alpha from old -> new (0 -> 1)
                        alphas = np.linspace(0.0, 1.0, nseg) ** (3 / 2)

                        r, g, b = trail_rgbs[body]
                        rgba = np.column_stack([np.full(nseg, r), np.full(nseg, g), np.full(nseg, b), alphas])
                        trail_cols[body].set_color(rgba)

                    # head point
                    points[body].set_data([frames[body, frame, 0]], [frames[body, frame, 1]])
                    points[body].set_3d_properties([frames[body, frame, 2]])

                # getting time passed per frame within simulation
                plottime = float("%.2f" % (frame / 24))
                timetext.set_text("t=" + str(plottime))
                return trail_cols, points, timetext

            axis_dim = 10
            ax.set_xlim(-axis_dim, axis_dim)
            ax.set_ylim(-axis_dim, axis_dim)
            ax.set_zlim(-axis_dim, axis_dim)

            ax.set_xlabel('X axis')
            ax.set_ylabel('Y axis')
            ax.set_zlabel('Z axis')

            self.anim = FuncAnimation(fig, update_data, frames=TIMELINE.size, interval=10, blit=False)
            #self.anim.save((Path(str(CWDDIR)) / "Statistics" / (str(self.dropdown1.get())+'animation.mp4')), writer='ffmpeg', fps=24)

            # destroy the old animation if ran multiple times
            for widget in self.animation_frame.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(fig, self.animation_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill="both", expand=True)

            canvas.draw()

# SUS
        def show_statistics(duration, precision, selection):
            # constants
            NUM_BODIES = len([f for f in os.listdir(get_path(-1)) if f.startswith('body') and f.endswith('.csv')])

            # opening reference data and simulation data
            path_reference = Path(str(CWDDIR)) / 'Reference_Data' / (
                        (str(selection).split(' - ')[1]) + "_IAS15_dT_" + "0.0005")
            path_simulation = get_path(-1)

            # Check if reference data exists
            if not path_reference.exists():
                print("\n" + "#" * 60)
                print("ERROR: Reference data not found!")
                print("#" * 60)
                print(f"\nMissing: {path_reference}")
                print("\nPlease run the reference simulation first before")
                print("comparing results. Select IAS15 as the integrator and")
                print("run a simulation with precision 0.0005 to generate reference data.")
                return

            # Read phase space data
            reference_data = data_analysis.read_phase_space(NUM_BODIES, path_reference)
            simulated_data = data_analysis.read_phase_space(NUM_BODIES, path_simulation)

            # Extract masses from configuration
            if selection.startswith('S'):
                num = int(selection.split('-')[0].strip().split(' ')[1]) - 1
                masses = [initialconditions[num][1], initialconditions[num][4], initialconditions[num][7]]
            else:
                num = int(selection.split('-')[0].strip().split(' ')[1]) - 1
                masses = [customs[num][1], customs[num][4], customs[num][7]]

            # Create error function
            error_func = data_analysis.error_function(reference_data, simulated_data, masses)

            # count frames - use minimum length between reference and simulation
            min_frames = min(len(simulated_data[0]), len(reference_data[0]))

            # timeline: 1 time unit = 24 frames
            frames = np.arange(min_frames)
            TIMELINE = frames / 24

            # Calculate errors at each time point
            trajectory_errors = []
            totE_errors = []

            for frame in frames:
                traj_err, E_err = error_func(frame)
                trajectory_errors.append(traj_err)
                totE_errors.append(E_err)

            # Calculate max errors
            traj_max = data_analysis.calculate_max_error(trajectory_errors, dt=1.0 / 24.0)
            E_max = data_analysis.calculate_max_error(totE_errors, dt=1.0 / 24.0)

            # Create plot with two subplots
            fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

            n = len(trajectory_errors)

            # Trajectory Error Plot
            ax1.plot(TIMELINE[1:n], trajectory_errors[1:n], linewidth=2, color='red', label='Trajectory Error')
            ax1.axhline(y=traj_max, color='darkred', linestyle='--', linewidth=1.5,
                        label=f'%_MAX = {traj_max:.2e}%')
            ax1.set_xlabel('Time', fontsize=11)
            ax1.set_ylabel('Trajectory Error E_% (%)', fontsize=11)
            ax1.set_title('Phase Space Trajectory Error vs Time', fontsize=12, fontweight='bold')
            ax1.grid(True, alpha=0.3, which='both')
            ax1.legend(loc='upper right')

            # Energy Error Plot
            ax2.plot(TIMELINE, totE_errors, linewidth=2, color='blue', label='Total Energy Error')
            ax2.axhline(y=E_max, color='darkblue', linestyle='--', linewidth=1.5,
                        label=f'E_MAX = {ham_max:.2e}%')
            ax2.set_xlabel('Time', fontsize=11)
            ax2.set_ylabel('Total Energy Error E_H% (%)', fontsize=11)
            ax2.set_title('Energy Conservation Error vs Time', fontsize=12, fontweight='bold')
            ax2.grid(True, alpha=0.3, which='both')
            ax2.legend(loc='upper right')

            plt.tight_layout()
            dt_str = f"{precision:g}".replace(".", "p")  # 0.065 -> "0p065"
            out = Path(str(CWDDIR)) / "Statistics" / f"{self.dropdown1.get()}_Simulated_data_dT_{dt_str}.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(out, dpi=300, bbox_inches="tight")

            # Destroy old statistics plot if it exists
            for widget in self.statistics_frame.winfo_children():
                widget.destroy()

            # Embed in GUI
            canvas2 = FigureCanvasTkAgg(fig2, self.statistics_frame)
            canvas_widget2 = canvas2.get_tk_widget()
            canvas_widget2.pack(fill="both", expand=True)
            canvas2.draw()

            # Print summary statistics to console
            print("\n" + "#" * 60)
            print(f"ERROR ANALYSIS: ")
            print("#" * 60 + "\n")
            print(f"Total frames analyzed: {min_frames}")
            print(f"Max Trajectory Error: {traj_max:.4e}%")
            print(f"Max Total Energy Error: {ham_max:.4e}%\n")

            # Create visualization
            fig3 = plt.figure(figsize=(12, 10))

def update():
    submission_time = datetime.datetime.now()

    try:
        selection = self.dropdown1.get()
        duration = int(self.durationVariable.get())

        # --- precision ---
        if self.var2.get() == 0:
            precision = round(self.precision.get(), 4)
        else:
            precision = float(self.precisionoverride.get())

        # --- get config index ---
        num = int(selection.split('-')[0].split()[1]) - 1

        # --- get data ---
        if self.var1.get() == 1:
            # manual input mode
            try:
                data = [
                    ast.literal_eval(self.position1.get()), float(self.mass1.get()), ast.literal_eval(self.velocity1.get()),
                    ast.literal_eval(self.position2.get()), float(self.mass2.get()), ast.literal_eval(self.velocity2.get()),
                    ast.literal_eval(self.position3.get()), float(self.mass3.get()), ast.literal_eval(self.velocity3.get())
                ]
            except Exception:
                show_error("Invalid input format. Use (x, y, z) for vectors.")
                return
        else:
            # preset from CSV
            data = configs[num]

        # --- extract masses ---
        masses = [data[1], data[4], data[7]]

        print(f"\nRunning RK45 simulation")
        print(f"Precision: {precision}")
        print(f"Duration: {duration}\n")

        # --- run simulation ---
        Simulate(data, precision, duration)

        # --- visualization ---
        show_animation(duration)
        show_statistics(duration, precision, selection)

        # --- timing ---
        elapsed = datetime.datetime.now() - submission_time
        print(f"Processing time: {elapsed}\n")

        # --- store last run ---
        self.last_simulation_data = {
            'num_bodies': 3,
            'masses': masses,
            'precision': precision,
            'duration': duration,
            'selection': selection
        }

    except Exception as e:
        show_error(e)

                rendering_time = datetime.datetime.now()
                time_elapsed = rendering_time - submission_time
                print("Processing time of simulation: " + str(time_elapsed) + "\n")

                # Store simulation data for Lyapunov analysis
                NUM_BODIES = 3
                self.last_simulation_data = {
                    'num_bodies': NUM_BODIES,
                    'masses': masses,
                    'precision': precision,
                    'duration': int(self.durationVariable.get()),
                    'selection': selection
                }

                show_statistics(int(self.durationVariable.get()), precision, selection)
            except Exception as e:
                show_error(e)

        def override():
            if self.var2.get() == 1:
                self.precisionoverride.configure(state="normal")
            else:
                self.precisionoverride.configure(state="disabled")

        def save():
            if self.var1.get() != 1:
                return

            def submit():
                new = list((ast.literal_eval(self.position1.get()), eval(self.mass1.get()), eval(self.velocity1.get()),
                            eval(self.position2.get()), eval(self.mass2.get()), eval(self.velocity2.get()),
                            eval(self.position3.get()), eval(self.mass3.get()), eval(self.velocity3.get()),
                            self.popup.name.get().split('- ')[-1]))
                if self.popup.new_save.get():
                    presets = open("data_list.csv", "a")
                    customs.append(new)
                    presets.write(str(new) + '\n')

                    full.append(f'Custom {len(full) - len(initialconditions) + 1} - {new[-1]}')
                    self.dropdown1.set(full[-1])
                    presets.close()
                else:
                    if self.dropdown1.get().startswith("S"):
                        print("Can not edit stable orbits")
                        return
                    index = int(self.dropdown1.get().split('-')[0].strip().split(' ')[1]) - 1
                    customs[index] = new
                    presets = open("data_list.csv", "w")
                    presets.write('\n')
                    for i in customs:
                        presets.write(str(i) + '\n')

                    full[len(initialconditions) + index] = f'Custom {index + 1} - {new[-1]}'
                    self.dropdown1.set(full[len(initialconditions) + index])

                self.dropdown1.configure(values=full)

                self.popup.destroy()
                self.popup.update()
                return

            self.popup = customtkinter.CTkToplevel(self)
            self.popup.title("Name Config")
            self.popup.geometry("400x200")
            self.popup.resizable(False, False)
            self.popup.attributes("-topmost", True)

            self.popup.grid_columnconfigure(1, weight=1)
            self.popup.grid_rowconfigure(1, weight=1)

            self.popup.frame = customtkinter.CTkFrame(self.popup)
            self.popup.frame.grid(row=1, column=1, rowspan=2, columnspan=2, pady=0, padx=0, sticky="nsew")
            self.popup.new_save = customtkinter.CTkCheckBox(self.popup.frame, text="New Save", onvalue=1, offvalue=0,
                                                            command=check)
            self.popup.new_save.pack(side="left", padx=(40, 5), pady=5)
            self.popup.name = customtkinter.CTkEntry(self.popup.frame, placeholder_text="Save Name")
            self.popup.name.insert(0, self.dropdown1.get())
            self.popup.name.configure(state="disabled")
            self.popup.name.pack(side="right", padx=(5, 40), pady=5)

            self.popup.submit = customtkinter.CTkButton(self.popup.frame, text="Submit", command=submit)
            self.popup.submit.pack(side="bottom", padx=5, pady=(5, 20))

        def check():
            if self.popup.new_save.get():
                self.popup.name.configure(state="normal")

                self.popup.name.delete(0, "end")
            else:
                self.popup.name.delete(0, "end")
                self.popup.name.insert(0, self.dropdown1.get())
                self.popup.name.configure(state="disabled")

        # lists of configurations
        initialconditions = list()
        full = list()

        with open("data_list.csv", "r") as presets:
            for x in presets:
                line = x.strip()
                if line:
                    initialconditions.append(ast.literal_eval(line))

        for i, stable in enumerate(initialconditions):
            full.append(f'Stable {i + 1} - {stable[-1]}')

        # Window configuration
        self.title("Three Body Problem Simulator")
        self.geometry("1400x1000")

        # configure grid layout (4x4)
        self.grid_columnconfigure((1), weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3), weight=1)

        # Submit button and hidden textfield for error popups
        self.submitframe = customtkinter.CTkFrame(self)
        self.submitframe.grid(column=2, row=3, pady=(0, 20), padx=20, sticky="nsew")
        self.save = customtkinter.CTkButton(self.submitframe, height=20, width=150, text="Save Configuration",
                                            command=save)
        self.save.pack(pady=(5, 5), side="top")
        self.slidertext = customtkinter.CTkLabel(self.submitframe, height=20, width=300, text="")
        self.slidertext.pack(pady=(20, 5), side="top")
        self.precision = customtkinter.CTkSlider(self.submitframe, from_=0.1, to=0.0005, width=200,
                                                 command=lambda value: self.slidertext.configure(
                                                     text="Precision: " + str(round(value,
                                                                                    4)) + " (size of timesteps, lower is more accurate)"),
                                                 number_of_steps=100)
        self.precision.pack(pady=(5, 20), padx=20, side="top")
        self.precision.set(0.01)
        self.slidertext.configure(
            text="Precision: " + str(round(self.precision.get(), 4)) + " (size of timesteps, lower is more accurate)")
        self.durationVariable = customtkinter.CTkEntry(self.submitframe, width=200,
                                                       placeholder_text="Simulation duration (s)")
        self.durationVariable.pack(pady=10, padx=20, side="top")
        self.submit = customtkinter.CTkButton(self.submitframe, text="Simulate", command=update)
        self.submit.pack(pady=10, padx=20, side="top")
        self.textfield = customtkinter.CTkLabel(self.submitframe, height=20, width=300, text="")
        self.textfield.pack(pady=10, side="top")
        self.var2 = IntVar()

        # frame for simulation animation
        self.animation_frame = customtkinter.CTkFrame(self.simtabs.tab("Simulation"), height=500)
        self.animation_frame.grid(column=0, row=0, rowspan=2, columnspan=2, padx=20, pady=20, sticky="nsew")

        # frame for statistics plot
        self.statistics_frame = customtkinter.CTkFrame(self.simtabs.tab("Simulation"), height=300)
        self.statistics_frame.grid(column=0, row=2, rowspan=2, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")

        integrator("rk45")
        stableOrbits("Stable 1 - Equilateral Triangle")


app().mainloop()