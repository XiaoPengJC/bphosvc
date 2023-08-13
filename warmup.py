from bpho_service import generate_2d_orbit_animation ,generate_3d_orbit_animation
import itertools

inner_planets = ["Mercury", "Venus", "Earth", "Mars"]
complete_outer_planets = ["Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]



def warmup_inner_orbit_2d_animation():
    for i in range(1, len(inner_planets) + 1):
        for combination in itertools.combinations(inner_planets, i):
            print("Generating 2D animation for " + str(combination))
            generate_2d_orbit_animation(list(combination), "2d_anim-" + "_".join(combination) + ".gif")


def warmup_inner_orbit_3d_animation():
    for i in range(1, len(inner_planets) + 1):
        for combination in itertools.combinations(inner_planets, i):
            print("Generating 3D animation for " + str(combination))
            generate_3d_orbit_animation(list(combination), "3d_anim-" + "_".join(combination) + ".gif")


def warmup_outer_orbit_2d_animation():
    for i in range(1, len(complete_outer_planets) + 1):
        for combination in itertools.combinations(complete_outer_planets, i):
            print("Generating 2D animation for " + str(combination))
            generate_2d_orbit_animation(list(combination), "2d_anim-" + "_".join(combination) + ".gif")


def warmup_outer_orbit_3d_animation():
    for i in range(1, len(complete_outer_planets) + 1):
        for combination in itertools.combinations(complete_outer_planets, i):
            print("Generating 3D animation for " + str(combination))
            generate_3d_orbit_animation(list(combination), "3d_anim-" + "_".join(combination) + ".gif")