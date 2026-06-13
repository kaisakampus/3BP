import numpy as np
import matplotlib.pyplot as plt
# to produce these systematically, I used ai to save time
BASE_PATH = r"C:\Users\kaisa\My Drive\Simulated_Data"
orbits = [
    ("orbit_O3","O3 ±ε=1e-4","orbit_O3","orbit_O3add","orbit_O3sub"),
]
ranges = [(0, 5000), (5000,7500), (7500,10000)] 
def load(main_name, sub_name, add_name):
    def ts(n):
        t = np.loadtxt(f"{BASE_PATH}\\{n}_LAST_timestep_sizes.csv")
        return t, np.cumsum(t)
    return {v: ts(n) for v, n in [("main", main_name), ("sub", sub_name), ("add", add_name)]}
for name, title, main_n, sub_n, add_n in orbits:
    print(f"{name}")
    d = load(main_n, sub_n, add_n)
    for i, (lo, hi) in enumerate(ranges):
        plt.figure(figsize=(14, 4))
        plt.plot(d["sub"][1][1:],  d["sub"][0][1:],  color="turquoise", linewidth=1, label=f"{name} (r1_x−ε)")
        plt.plot(d["add"][1][1:],  d["add"][0][1:],  color="lime",      linewidth=1, label=f"{name} (r1_x+ε)")
        plt.plot(d["main"][1][1:], d["main"][0][1:], color="deeppink",  linewidth=1, label=f"{name} r1_x") # last = on top
        plt.xlim(lo, hi)
        plt.xlabel("simulation time")
        plt.ylabel("adaptive timestep size dt")
        plt.title(title)
        plt.legend()
        plt.xticks([t for t in plt.xticks()[0] if t != 50])
        plt.tight_layout()
        plt.savefig(f"{BASE_PATH}\\{name}_timesteps_part{i+1}.png", dpi=150)
        plt.show()
print("complete")