# the order is heavily inspired by RK45 code snippet from https://github.com/LBrink05/Project-Period-3D-Simulations-of-Multi-Body-Star-Systems
# great history story of 3BP: https://thevarsity.ca/2025/02/23/is-the-three-body-problem-unpredictable/
# cool stuff https://gminton.org/#choreo
# check the example gif configuration names https://screenager.dev/blog/2025/the-three-body-problem

import numpy as np
import time
from pathlib import Path
from scipy.integrate import RK45

eps = 1e-4 # i use this large epsilon because i have dimensionless units and machine epsilon is insignificant in results

#2D configurations (14 total)

#easy configurations
# initial conditions https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
figure8 = [(-1,0,0),1,(0.3471168881,0.5327249454,0),(1,0,0),1,(0.3471168881,0.5327249454,0),(0,0,0),1,(-0.6942337762,-1.0654498908,0)]
figure8add = [(-1+eps,0,0),1,(0.3471168881,0.5327249454,0),(1,0,0),1,(0.3471168881,0.5327249454,0),(0,0,0),1,(-0.6942337762,-1.0654498908,0)]
figure8sub = [(-1-eps,0,0),1,(0.3471168881,0.5327249454,0),(1,0,0),1,(0.3471168881,0.5327249454,0),(0,0,0),1,(-0.6942337762,-1.0654498908,0)]

# initial conditions from https://arxiv.org/pdf/1303.0181
butterflyI = [(-1,0,0),1,(0.30689,0.12551,0.0),(1,0,0),1,(0.30689,0.12551,0.0),(0,0,0),1,(-0.61378, -0.25102, 0)]
butterflyIadd = [(-1+eps,0,0),1,(0.30689,0.12551,0.0),(1,0,0),1,(0.30689,0.12551,0.0),(0,0,0),1,(-0.61378, -0.25102, 0)]
butterflyIsub = [(-1-eps,0,0),1,(0.30689,0.12551,0.0),(1,0,0),1,(0.30689,0.12551,0.0),(0,0,0),1,(-0.61378, -0.25102, 0)]

# initial conditions from https://arxiv.org/pdf/1303.0181
yinyangadd = [(-1+eps,0,0),1,(0.513938,0.304736,0),(1,0,0),1,(0.513938,0.304736,0),(0,0,0),1,(-1.027876,-0.609472,0)]
yinyangsub = [(-1-eps,0,0),1,(0.513938,0.304736,0),(1,0,0),1,(0.513938,0.304736,0),(0,0,0),1,(-1.027876,-0.609472,0)]
yinyang = [(-1,0,0),1,(0.513938,0.304736,0),(1,0,0),1,(0.513938,0.304736,0),(0,0,0),1,(-1.027876,-0.609472,0)]

# initial conditions https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
brouckeA1 = [(-0.9892620043,0,0),1,(0,1.9169244185,0),(2.2096177241,0,0),1,(0,0.1910268738,0),(-1.2203557197,0,0),1,(0,-2.1079512924,0)]
brouckeA1add = [((-0.9892620043+eps),0,0),1,(0,1.9169244185,0),(2.2096177241,0,0),1,(0,0.1910268738,0),(-1.2203557197,0,0),1,(0,-2.1079512924,0)]
brouckeA1sub = [((-0.9892620043-eps),0,0),1,(0,1.9169244185,0),(2.2096177241,0,0),1,(0,0.1910268738,0),(-1.2203557197,0,0),1,(0,-2.1079512924,0)]

# initial conditions from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
brouckeA7 = [(-0.1095519101,0,0),1,(0,0.9913358338,0),(1.6613533905,0,0),1,(0,-0.1569959746,0),(-1.5518014804,0,0),1,(0,-0.8343398592,0)]
brouckeA7add = [(-0.1095519101+eps,0,0),1,(0,0.9913358338,0),(1.6613533905,0,0),1,(0,-0.1569959746,0),(-1.5518014804,0,0),1,(0,-0.8343398592,0)]
brouckeA7sub = [(-0.1095519101-eps,0,0),1,(0,0.9913358338,0),(1.6613533905,0,0),1,(0,-0.1569959746,0),(-1.5518014804,0,0),1,(0,-0.8343398592,0)]

#intermediate configurations
# initial conditions from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
brouckeA2 = [(0.336130095,0,0),1,(0,1.532431537,0),(0.7699893804,0,0),1,(0,-0.6287350978,0),(-1.1061194753,0,0),1,(0,-0.9036964391,0)]
brouckeA2add = [(0.336130095+eps,0,0),1,(0,1.532431537,0),(0.7699893804,0,0),1,(0,-0.6287350978,0),(-1.1061194753,0,0),1,(0,-0.9036964391,0)]
brouckeA2sub = [(0.336130095-eps,0,0),1,(0,1.532431537,0),(0.7699893804,0,0),1,(0,-0.6287350978,0),(-1.1061194753,0,0),1,(0,-0.9036964391,0)]

# initial conditions from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
yinyang312ABeta = [(-1,0,0),1,(0.417343,0.3131,0),(1,0,0),1,(0.417343,0.3131,0),(0,0,0),1,(-0.834686,-0.6262,0)]
yinyang312ABetaadd = [(-1+eps,0,0),1,(0.417343,0.3131,0),(1,0,0),1,(0.417343,0.3131,0),(0,0,0),1,(-0.834686,-0.6262,0)]
yinyang312ABetasub = [(-1-eps,0,0),1,(0.417343,0.3131,0),(1,0,0),1,(0.417343,0.3131,0),(0,0,0),1,(-0.834686,-0.6262,0)]

# initial conditions from https://arxiv.org/pdf/2109.07013
pythagorean = [(1,3,0),3,(0,0,0),(-2,-1,0),4,(0,0,0),(1,-1,0),5,(0,0,0)]
pythagoreanadd = [(1+eps,3,0),3,(0,0,0),(-2,-1,0),4,(0,0,0),(1,-1,0),5,(0,0,0)]
pythagoreansub = [(1-eps,3,0),3,(0,0,0),(-2,-1,0),4,(0,0,0),(1,-1,0),5,(0,0,0)]

# initial conditions from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
oval_catface_starship = [(0.536387073390,0.054088605008,0),1,(-0.569379585581,1.255291102531,0),(-0.252099126491,0.694527327749,0),1,(0.079644615252,-0.458625997341,0),(-0.275706601688,-0.335933589318,0),1,(0.489734970329,-0.796665105189,0),]
oval_catface_starship_add = [(0.536387073390+eps,0.054088605008,0),1,(-0.569379585581,1.255291102531,0),(-0.252099126491,0.694527327749,0),1,(0.079644615252,-0.458625997341,0),(-0.275706601688,-0.335933589318,0),1,(0.489734970329,-0.796665105189,0),]
oval_catface_starship_sub = [(0.536387073390-eps,0.054088605008,0),1,(-0.569379585581,1.255291102531,0),(-0.252099126491,0.694527327749,0),1,(0.079644615252,-0.458625997341,0),(-0.275706601688,-0.335933589318,0),1,(0.489734970329,-0.796665105189,0),]

#complex configurations listed by Sheen
# initial conditions from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
loopendedtriangles = [(0.6661637520772179,0.081921852656887,0),1,(0.84120297540307,0.029746212757039,0),(-0.025192663684493022,0.45444857588251897,0),1,(0.142642469612081,-0.492315648524683,0),(-0.10301329374224,-0.765806200083609,0),1,(-0.98384544501151,0.462569435774018,0)]
loopendedtrianglesadd = [(0.6661637520772179+eps,0.081921852656887,0),1,(0.84120297540307,0.029746212757039,0),(-0.025192663684493022,0.45444857588251897,0),1,(0.142642469612081,-0.492315648524683,0),(-0.10301329374224,-0.765806200083609,0),1,(-0.98384544501151,0.462569435774018,0)]
loopendedtrianglessub = [(0.6661637520772179-eps,0.081921852656887,0),1,(0.84120297540307,0.029746212757039,0),(-0.025192663684493022,0.45444857588251897,0),1,(0.142642469612081,-0.492315648524683,0),(-0.10301329374224,-0.765806200083609,0),1,(-0.98384544501151,0.462569435774018,0)]

# initial conditions from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
ovalswithflourishes = [(0.716248295713,0.384288553041,0),1,(1.245268230896,2.444311951777,0),(0.086172594591,1.342795868577,0),1,(-0.67522432369,-0.96287961363,0),(0.538777980808,0.481049882656,0),1,(-0.570043907206,-1.481432338147,0)]
ovalswithflourishesadd = [(0.716248295713+eps,0.384288553041,0),1,(1.245268230896,2.444311951777,0),(0.086172594591,1.342795868577,0),1,(-0.67522432369,-0.96287961363,0),(0.538777980808,0.481049882656,0),1,(-0.570043907206,-1.481432338147,0)]
ovalswithflourishessub = [(0.716248295713-eps,0.384288553041,0),1,(1.245268230896,2.444311951777,0),(0.086172594591,1.342795868577,0),1,(-0.67522432369,-0.96287961363,0),(0.538777980808,0.481049882656,0),1,(-0.570043907206,-1.481432338147,0)]

# initial conditions from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
brouckeA11 = [(0.0132604844,0,0),1,(0,1.054151921,0),(1.4157286016,0,0),1,(0,-0.2101466639,0),(-1.4289890859,0,0),1,(0,-0.8440052572,0)]
brouckeA11add = [(0.0132604844+eps,0,0),1,(0,1.054151921,0),(1.4157286016,0,0),1,(0,-0.2101466639,0),(-1.4289890859,0,0),1,(0,-0.8440052572,0)]
brouckeA11sub = [(0.0132604844-eps,0,0),1,(0,1.054151921,0),(1.4157286016,0,0),1,(0,-0.2101466639,0),(-1.4289890859,0,0),1,(0,-0.8440052572,0)]

# initial conditions from https://arxiv.org/pdf/1303.0181
yarn_add = [(-1+eps,0,0), 1, (0.55906, 0.34919, 0),(1,0,0),  1, (0.55906, 0.34919, 0),(0,0,0),  1, (-1.11812, -0.69838, 0)]
yarn_sub = [(-1-eps,0,0), 1, (0.55906, 0.34919, 0),(1,0,0),  1, (0.55906, 0.34919, 0),(0,0,0),  1, (-1.11812, -0.69838, 0)]
yarn = [(-1,0,0), 1, (0.55906, 0.34919, 0),(1,0,0),  1, (0.55906, 0.34919, 0),(0,0,0),  1, (-1.11812, -0.69838, 0)]

# initial conditions from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
gear_inside_oval = [(0.335476420318203,-0.243208301824394,0),1,(1.047838171160758,0.817404215288346,0),(0.010021708193205,0.363104062311693,0),1,(-0.847200907807940,-0.235749148338353,0),(0.030978712523174,0.423035485079015,0),1,(-0.200636552532016,-0.581655492859626,0),]
gear_inside_oval_add = [(0.335476420318203+eps,-0.243208301824394,0),1,(1.047838171160758,0.817404215288346,0),(0.010021708193205,0.363104062311693,0),1,(-0.847200907807940,-0.235749148338353,0),(0.030978712523174,0.423035485079015,0),1,(-0.200636552532016,-0.581655492859626,0),]
gear_inside_oval_sub = [(0.335476420318203-eps,-0.243208301824394,0),1,(1.047838171160758,0.817404215288346,0),(0.010021708193205,0.363104062311693,0),1,(-0.847200907807940,-0.235749148338353,0),(0.030978712523174,0.423035485079015,0),1,(-0.200636552532016,-0.581655492859626,0),]

# extra

# initial conditions from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
brouckeR1 = [(0.808310623,0,0),1,(0,0.9901979166,0),(-0.4954148566,0,0),1,(0,-2.7171431768,0),(-0.3128957664,0,0),1,(0,1.7269452602,0)]
brouckeR1add = [(0.808310623+eps,0,0),1,(0,0.9901979166,0),(-0.4954148566,0,0),1,(0,-2.7171431768,0),(-0.3128957664,0,0),1,(0,1.7269452602,0)]
brouckeR1sub = [(0.808310623-eps,0,0),1,(0,0.9901979166,0),(-0.4954148566,0,0),1,(0,-2.7171431768,0),(-0.3128957664,0,0),1,(0,1.7269452602,0)]

# initial conditions from https://observablehq.com/@rreusser/periodic-planar-three-body-orbits
brouckeA10 = [(-0.5426216182,0,0),1,(0,0.8750200467,0),(2.5274928067,0,0),1,(0,-0.0526955841,0),(-1.9848711885,0,0),1,(0,-0.8223244626,0)]
brouckeA10add = [(-0.5426216182+eps,0,0),1,(0,0.8750200467,0),(2.5274928067,0,0),1,(0,-0.0526955841,0),(-1.9848711885,0,0),1,(0,-0.8223244626,0)]
brouckeA10sub = [(-0.5426216182-eps,0,0),1,(0,0.8750200467,0),(2.5274928067,0,0),1,(0,-0.0526955841,0),(-1.9848711885,0,0),1,(0,-0.8223244626,0)]

#3D configurations (5 total), all complex

# initial conditions from https://numericaltank.sjtu.edu.cn/three-body/three-body.htm
orbit_O2 = [(-1,0,0),1,(-0.272600007460296,-0.432093711947155,0.629473407171139),(1,0,0),1,(-0.272600007460296,-0.432093711947155,-0.629473407171139),(0,0,1.02200578272669),1.2,(0.454333345767160,0.720156186578592,0.0)]
orbit_O2add = [(-1+eps,0,0),1,(-0.272600007460296,-0.432093711947155,0.629473407171139),(1,0,0),1,(-0.272600007460296,-0.432093711947155,-0.629473407171139),(0,0,1.02200578272669),1.2,(0.454333345767160,0.720156186578592,0.0)]
orbit_O2sub = [(-1-eps,0,0),1,(-0.272600007460296,-0.432093711947155,0.629473407171139),(1,0,0),1,(-0.272600007460296,-0.432093711947155,-0.629473407171139),(0,0,1.02200578272669),1.2,(0.454333345767160,0.720156186578592,0.0)]

# initial conditions from https://numericaltank.sjtu.edu.cn/three-body/three-body.htm
orbit_O3 = [(-1,0,0),1,(0.402136910074724,0.180356951286259,0.210445128137873),(1,0,0),1,(0.402136910074724,0.180356951286259,-0.210445128137873),(0,0,0.476878264280312),1,(-0.804273820149448,-0.360713902572518,0.0)]
orbit_O3add = [(-1+eps,0,0),1,(0.402136910074724,0.180356951286259,0.210445128137873),(1,0,0),1,(0.402136910074724,0.180356951286259,-0.210445128137873),(0,0,0.476878264280312),1,(-0.804273820149448,-0.360713902572518,0.0)]
orbit_O3sub = [(-1-eps,0,0),1,(0.402136910074724,0.180356951286259,0.210445128137873),(1,0,0),1,(0.402136910074724,0.180356951286259,-0.210445128137873),(0,0,0.476878264280312),1,(-0.804273820149448,-0.360713902572518,0.0)]

# initial conditions from https://numericaltank.sjtu.edu.cn/three-body/three-body.htm
orbit_O26 = [(-1,0,0), 1, (0.402136910074724, 0.180356951286259, 0.210445128137873), (1,0,0), 1, (0.402136910074724, 0.180356951286259, -0.210445128137873), (0,0,6.17172796472047e-01), 1, (-0.804273820149448, -0.360713902572518, 0)]
orbit_O26add = [(-1+eps,0,0), 1, (0.402136910074724, 0.180356951286259, 0.210445128137873), (1,0,0), 1, (0.402136910074724, 0.180356951286259, -0.210445128137873), (0,0,6.17172796472047e-01), 1, (-0.804273820149448, -0.360713902572518, 0)]
orbit_O26sub = [(-1-eps,0,0), 1, (0.402136910074724, 0.180356951286259, 0.210445128137873), (1,0,0), 1, (0.402136910074724, 0.180356951286259, -0.210445128137873), (0,0,6.17172796472047e-01), 1, (-0.804273820149448, -0.360713902572518, 0)]

# initial conditions from https://numericaltank.sjtu.edu.cn/three-body/three-body.htm
panio_trio_O50_04 = [(-1,0,0),1,(0.24986795610137,0.03498530423433,0.00034357631743),(1,0,0),1,(0.24986795610137,0.03498530423433,-0.00034357631743),(0,0,0.21275290348332),0.4,(-1.24933978050685,-0.17492652117165,0),]
panio_trio_O50_04_add = [(-1+eps,0,0),1,(0.24986795610137,0.03498530423433,0.00034357631743),(1,0,0),1,(0.24986795610137,0.03498530423433,-0.00034357631743),(0,0,0.21275290348332),0.4,(-1.24933978050685,-0.17492652117165,0),]
panio_trio_O50_04_sub = [(-1-eps,0,0),1,(0.24986795610137,0.03498530423433,0.00034357631743),(1,0,0),1,(0.24986795610137,0.03498530423433,-0.00034357631743),(0,0,0.21275290348332),0.4,(-1.24933978050685,-0.17492652117165,0),]

# initial conditions from https://numericaltank.sjtu.edu.cn/three-body/three-body.htm
# adding perturbation on all three coordinates of the body just to compare whether the results would be more interesting
# will probably not end up using this one
panio_trio_O51_05 = [(-1,0,0),1,(0.30193851769471,0.07653448180274,-0.00547987697775),(1,0,0),1,(0.30193851769471,0.07653448180274,0.00547987697775),(0,0,0.24255099091956),0.5,(-1.20775407077885,-0.30613792721098,0),]
panio_trio_O51_05_add = [(-1+eps,0+eps,0+eps),1,(0.30193851769471,0.07653448180274,-0.00547987697775),(1,0,0),1,(0.30193851769471,0.07653448180274,0.00547987697775),(0,0,0.24255099091956),0.5,(-1.20775407077885,-0.30613792721098,0),]
panio_trio_O51_05_sub = [(-1-eps,0-eps,0-eps),1,(0.30193851769471,0.07653448180274,-0.00547987697775),(1,0,0),1,(0.30193851769471,0.07653448180274,0.00547987697775),(0,0,0.24255099091956),0.5,(-1.20775407077885,-0.30613792721098,0),]

NUM_BODIES = 3

def Simulate(data_list, precision, run_name):
    # extracting the initial coniditons from the configuration line
    # with float64 no calculation can be more precise than 16 decimal digits
    mass = np.array([data_list[1], data_list[4], data_list[7]], dtype=np.float64)
    start_pos = np.array([data_list[0], data_list[3], data_list[6],], dtype=np.float64)
    start_vel = np.array([data_list[2], data_list[5], data_list[8],], dtype=np.float64)

    # conditions for time and frames
    timestep = float(precision)
    sample_every = max(1, int(1 / timestep))

    # the saved frames should correspond to the sampled position
    frames, timestep_size_list = position_sampled(
        sample_every, NUM_BODIES, start_pos, start_vel, mass)

    # save CSV files to computer folder Simulated_Data
    # gave up on trying to save them to GitHub..
    PATH_FILES = Path(r"C:\Users\kaisa\My Drive")
    my_dir = PATH_FILES / "Simulated_Data"
    my_dir.mkdir(parents=True, exist_ok=True)

    # all sampled coordinates of each body are stored
    for body in range(NUM_BODIES):
        path = my_dir / f"{run_name}_NEW_body{body}.csv"
        np.savetxt(path, frames[body], delimiter=",")
    # all sampled timesteps are stored
    timestep_path = my_dir / f"{run_name}_NEW_timestep_sizes.csv"
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

            # softening because another code had it (link on 1st line)
            # i suppose this is to better regulate close encounters
            # visuals still look rough around the edges though
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
    # fixed timestep:
    # t_end = (TOTAL_STEPS - 1) * TIMESTEP

    # initial state vector
    f0 = np.concatenate([START_POS.flatten(), START_VEL.flatten()])

    solver = RK45(
        fun=lambda t, y: ode_system(t, y, MASS, NUM_BODIES),
        t0=t0,
        y0=f0,
        t_bound=10000, # used to be np.inf and 50
        rtol=3.162e-12, #1e-9
        atol=1e-12, #1e-13 can be both when fixed?
        max_step=np.inf # adaptive timestep
    )

    states = []
    times = []
    step_count = 0

    COLLISION_THRESHOLD = 0.0001   # bodies too close
    ESCAPE_THRESHOLD = 100.0     # bodies too far apart

    while solver.status == 'running':
        solver.step()

        # print progress every 1000 steps because i am anxious and skeptical whether this actually works
        #nevermind i ran it and it does
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

        if collapsed: # initially my code kept running even when the bodies drifted too far apart
            break

        # for animaton save every other step
        if step_count % SAMPLE_EVERY == 0:
            states.append(solver.y.copy())
            times.append(solver.t)

        step_count += 1 # because i am only using timer not actually timing the true fixed timestep simulation in the end

    # convert to arrays
    states = np.array(states)   # (T, 6*N)
    times = np.array(times)

# ai input begins
# validation round made me realize mistake in data shaping in the data file which messed up the 3D visualisation
    T = len(states)

    pos = states[:, :3*NUM_BODIES].reshape(T, NUM_BODIES, 3)
    vel = states[:, 3*NUM_BODIES:].reshape(T, NUM_BODIES, 3)

    frames = np.concatenate([pos, vel], axis=2)   # (T, N, 6)
    frames = frames.transpose(1, 0, 2)            # (N, T, 6)

# ai input ends

    # the old version
    # Reshape to (NUM_BODIES, T, 6)
    #states = states.reshape(-1, NUM_BODIES, 6) # (T, N, 6)
    #frames = states.transpose(1, 0, 2) # (N, T, 6)

    # timestep sizes (important for animation timing)
    timestep_size_list = np.concatenate([[0], np.diff(times)])

    return frames, timestep_size_list

# structuring the data in body files
def read_phase_space(NUM_BODIES, path, run_name):
    
    phase_space_data = []
    
    for b in range(NUM_BODIES):
        path_b = str(path) + f"/{run_name}_NEW_body{b}.csv"
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

# initial
#print(f"figure 8")
#start = time.time()
# 1 simulation time unit is like 200 internal steps with dt=0.005, 2000 with dt=0.0005
# making it stricter because the 3D visualised simulation is choppy right now
#frames, timesteps = Simulate(figure8, 0.0005, "figure8")
#end = time.time()

#path = Path.cwd() / "Simulated_Data"
#path = Path(r"C:\Users\kaisa\My Drive\Simulated_Data")

#sim_data = read_phase_space(NUM_BODIES, path, "figure8")
#print(f"Simulation computations lasted {end - start:.2f} s")
#print(f"Total timesteps: {len(timesteps)}")

#print("\n output of 10 rows for each body")
#for body in range(NUM_BODIES):
#    print(f"\nfigure8_Body {body}:")
#    print(frames[body][:10])

#print("\n output of 10 rows of timestep sizes")
#timestep_path = path / "figure8_timestep_sizes.csv"
#with open(timestep_path, "r") as f:
#    for i, line in enumerate(f):
#        if i >= 10:
#            break
#        print(line, end="")

#print(f"figure 8 + epsilon")
#start = time.time()
#frames, timesteps = Simulate(figure8add, 0.0005, "figure8add")
#end = time.time()

#sim_data = read_phase_space(NUM_BODIES, path, "figure8add")
#print(f"Simulation computations lasted {end - start:.2f} s")
#print(f"Total timesteps: {len(timesteps)}")

#print("\n output of 10 rows for each body")
#for body in range(NUM_BODIES):
#    print(f"\nfigure8add_Body {body}:")
#    print(frames[body][:10])

#print("\n output of 10 rows of timestep sizes")
#timestep_path = path / "figure8add_timestep_sizes.csv"
#with open(timestep_path, "r") as f:
#    for i, line in enumerate(f):
#        if i >= 10:
#            break
#        print(line, end="")

#print(f"figure 8 - epsilon")
#start = time.time()
#frames, timesteps = Simulate(figure8sub, 0.0005, "figure8sub")
#end = time.time()

#sim_data = read_phase_space(NUM_BODIES, path, "figure8sub")
#print(f"Simulation computations lasted {end - start:.2f} s")
#print(f"Total timesteps: {len(timesteps)}")

#print("\n output of 10 rows for each body")
#for body in range(NUM_BODIES):
#    print(f"\nfigure8sub_Body {body}:")
#    print(frames[body][:10])

#print("\n output of 10 rows of timestep sizes")
#timestep_path = path / "figure8sub_timestep_sizes.csv"
#with open(timestep_path, "r") as f:
#    for i, line in enumerate(f):
#        if i >= 10:
#            break
#        print(line, end="")

#now deepai experiment to systemize this
configurations = [{"func": figure8, "name":"figure8"},{"func":figure8add, "name": "figure8add"},
{"func": figure8sub, "name":"figuresub"},
{"func": yinyang, "name":"yinyang"},{"func":yinyangadd, "name": "yinyangadd"},
{"func": yinyangsub, "name":"yinyangsub"},
{"func": brouckeA1, "name":"brouckeA1"},{"func":brouckeA1add, "name": "brouckeA1add"},
{"func": brouckeA1sub, "name":"brouckeA1sub"},
{"func": brouckeA7, "name":"brouckeA7"},{"func":brouckeA7add, "name": "brouckeA7add"},
{"func": brouckeA7sub, "name":"brouckeA7sub"},
{"func": yinyang312ABeta, "name":"yinyang312ABeta"},{"func":yinyang312ABetaadd, "name": "yinyang312ABetaadd"},
{"func": yinyang312ABetasub, "name":"yinyang312ABetasub"},
{"func": oval_catface_starship, "name":"oval_catface_starship"},{"func":oval_catface_starship_add, "name": "oval_catface_starship_add"},
{"func": oval_catface_starship_sub, "name":"oval_catface_starship_sub"},
{"func": brouckeA11, "name":"brouckeA11"},{"func":brouckeA11add, "name": "brouckeA11add"},
{"func": brouckeA11sub, "name":"brouckeA11sub"},
{"func": yarn, "name":"yarn"},{"func":yarn_add, "name": "yarn_add"},
{"func": yarn_sub, "name":"yarn_sub"},
{"func": orbit_O3, "name":"orbit_O3"},{"func":orbit_O3add, "name": "orbit_O3add"},
{"func": orbit_O3sub, "name":"orbit_O3sub"},
{"func": orbit_O26, "name":"orbit_O26"},{"func":orbit_O26add, "name": "orbit_O26add"},
{"func": orbit_O26sub, "name":"orbit_O26sub"},
{"func": panio_trio_O50_04, "name":"panio_trio_O50_04"},{"func":panio_trio_O50_04_add, "name": "panio_trio_O50_04_add"},
{"func": panio_trio_O50_04_sub, "name":"panio_trio_O50_sub"},]

# loop through each configuration
for config in configurations:
    print(f"\n{config['name']}")

    start_time = time.time()
    # the simulation
    frames, timesteps = Simulate(config['func'], 0.00005, config['name'])
    end_time = time.time()

    # print summary after run of 1 configuration ends
    path = Path(r"C:\Users\kaisa\My Drive\Simulated_Data")
    sim_data = read_phase_space(NUM_BODIES, path, config['name'])
    print(f"Simulation computations lasted {end_time - start_time:.2f} s")
    print(f"Total timesteps: {len(timesteps)}")
    
    # first 10 rows for each body
    print("\nOutput of 10 rows for each body:")
    for body in range(NUM_BODIES):
        print(f"\n{config['name']}_NEW_Body {body}:")
        print(frames[body][:10])
    
    # first 10 lines of timestep sizes
    timestep_path = path / f"{config['name']}_NEW_timestep_sizes.csv"
    with open(timestep_path, "r") as f:
        for i, line in enumerate(f):
            if i >= 10:
                break
            print(line, end="")