import numpy as np
import matplotlib.pyplot as plt

BASE_PATH = r"C:\Users\kaisa\My Drive\Simulated_Data"

orbits = [
    ("yinyang",   "yinyang III.A.a ±ε=1e-4",  "yinyang",        "yinyangadd",         "yinyangsub"),
        ("yinyang312ABeta",   "yinyang III 12.A.b ±ε=1e-4",  "yinyang312ABeta",        "yinyang312ABetaadd",         "yinyang312ABetasub"),
    ("orbit_O3",      "O3 ±ε=1e-4",       "orbit_O3",           "orbit_O3add",           "orbit_O3sub"),
        ("orbit_O26",      "O26 ±ε=1e-4",       "orbit_O26",           "orbit_O26add",           "orbit_O26sub"),
    ("figure8",   "figure 8 ±ε=1e-4",  "figure8",        "figure8add",         "figure8sub"),
    ("yarn",      "yarn ±ε=1e-4",       "yarn",           "yarn_add",           "yarn_sub"),
    ("butterflyI", "butterfly I ±ε=1e-4", "butterflyI",      "butterflyIadd",       "butterflyIsub"),
        ("brouckeA1", "broucke A1 ±ε=1e-4", "brouckeA1",      "brouckeA1add",       "brouckeA1sub"),
            ("brouckeA7", "broucke A7 ±ε=1e-4", "brouckeA7",      "brouckeA7add",       "brouckeA7sub"),
                ("brouckeA11", "broucke A11 ±ε=1e-4", "brouckeA11",      "brouckeA11add",       "brouckeA11sub"),
    #("panio_trio_O50_04",     "O50 ±ε=1e-4", "panio_trio_O50_04", "panio_trio_O50_04_add", "panio_trio_O50_04_sub"),
]

def load(main_name, sub_name, add_name):
    def ts(n):
        t = np.loadtxt(f"{BASE_PATH}\\{n}_LAST_timestep_sizes.csv")
        return t, np.cumsum(t)
    return {v: ts(n) for v, n in [("main", main_name), ("sub", sub_name), ("add", add_name)]}

for name, title, main_n, sub_n, add_n in orbits:
    print(f"Plotting {name}...")
    d = load(main_n, sub_n, add_n)

    plt.figure(figsize=(10, 4))
    plt.plot(d["sub"][1][1:],  d["sub"][0][1:],  color="turquoise", linewidth=1, label=f"{name} (r1_x−ε)")
    plt.plot(d["add"][1][1:],  d["add"][0][1:],  color="lime",      linewidth=1, label=f"{name} (r1_x+ε)")
    plt.plot(d["main"][1][1:], d["main"][0][1:], color="deeppink",  linewidth=1, label=f"{name} r1_x")

    plt.xlim(left=0)
    plt.xlabel("simulation time")
    plt.ylabel("adaptive timestep size dt")
    plt.title(title)
    plt.legend()
    plt.xticks([t for t in plt.xticks()[0] if t != 50])
    plt.tight_layout()
    plt.savefig(f"{BASE_PATH}\\{name}_timesteps.png", dpi=150)
    plt.show()

print("Done.")