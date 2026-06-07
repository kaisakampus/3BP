import numpy as np
import matplotlib.pyplot as plt

# load timestep sizes
#timesteps = np.loadtxt(r"C:\Users\kaisa\My Drive\Simulated_Data\brouckeA11_timestep_sizes.csv")

# cumulative time axis
#cumulative_time = np.cumsum(timesteps)

#plt.figure(figsize=(10, 4))
#plt.plot(cumulative_time, timesteps, color="pink", linewidth=1)
#plt.xlabel("simulation time [-]")
#plt.ylabel("adaptive timestep size (dt) [-]")
#plt.title("broucke A2")
#plt.tight_layout()
#plt.show()

# load timestep sizes
timesteps_main = np.loadtxt(r"C:\Users\kaisa\My Drive\Simulated_Data\yinyang_NEW_timestep_sizes.csv")
timesteps_sub  = np.loadtxt(r"C:\Users\kaisa\My Drive\Simulated_Data\yinyangadd_NEW_timestep_sizes.csv")
timesteps_add  = np.loadtxt(r"C:\Users\kaisa\My Drive\Simulated_Data\yinyangsub_NEW_timestep_sizes.csv")

# cumulative time axis
cumulative_time_main = np.cumsum(timesteps_main)
cumulative_time_sub  = np.cumsum(timesteps_sub)
cumulative_time_add  = np.cumsum(timesteps_add)

# plotting
plt.figure(figsize=(10, 4))
#plt.plot(cumulative_time_main[1:], timesteps_main[1:], color="deeppink",         linewidth=1, label=" I")
#plt.plot(cumulative_time_sub[1:],  timesteps_sub[1:],  color="turquoise", linewidth=1, label="butterfly I (r1_x-ε)")
#plt.plot(cumulative_time_add[1:],  timesteps_add[1:],  color="lime",    linewidth=1, label="butterfly I (r1_x+ε)")
#plt.plot(cumulative_time_main[1:], timesteps_main[1:], color="deeppink",         linewidth=1, label="yarn r1_x")
#plt.plot(cumulative_time_sub[1:],  timesteps_sub[1:],  color="turquoise", linewidth=1, label="yarn (r1_x-ε)")
#plt.plot(cumulative_time_add[1:],  timesteps_add[1:],  color="lime",    linewidth=1, label="yarn (r1_x+ε)")
plt.plot(cumulative_time_sub[1:],  timesteps_sub[1:],  color="turquoise", linewidth=1, label="yinyang (r1_x-ε)")
plt.plot(cumulative_time_add[1:],  timesteps_add[1:],  color="lime",      linewidth=1, label="yinyang (r1_x+ε)")
plt.plot(cumulative_time_main[1:], timesteps_main[1:], color="deeppink",  linewidth=1, label="yinyang r1_x")  # last = on top
#plt.xlim(left=110)
x_max = max(cumulative_time_main[-1], cumulative_time_sub[-1], cumulative_time_add[-1])
#plt.xlim(left=110, right=x_max * 1.02)

#plt.axvline(x=55, color="black", linewidth=1, linestyle="--")
plt.xlabel("simulation time")
plt.ylabel("adaptive timestep size dt")
plt.title("yinyang ±ε=1e-4")
plt.legend()
ticks = [t for t in plt.xticks()[0] if t != 50]
#ticks = sorted(ticks + [55])
plt.xticks(ticks)
plt.tight_layout()
plt.show()