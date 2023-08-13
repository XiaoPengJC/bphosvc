from dataclasses import dataclass


@dataclass
class Planet:
    name: str  # name of planet
    a: float  # semi-major axis
    ecc: float  # eccentricity
    p: float  # period of orbit
    modified_p: float  # p relative to either Earth or Jupiter
    beta: float # angle of inclination of orbit


# Array of planet data where the period of orbit of the outer planets (Jupiter,
# Saturn, Uranus, Neptune, Pluto) are relative to Jupiter's period, in order to speed 
# up the animations. Hence, P for Jupiter is 11.861/11.861 = 1.000, P for Saturn is
# 29.628/11.861 = 2.498, P for Uranus is 84.747/11.861 = 7.145... and so on.
planet = [Planet("Mercury", 0.387, 0.21, 0.241, 0.241, 7.00),
            Planet("Venus", 0.723, 0.01, 0.615, 0.615, 3.39),
            Planet("Earth", 1.000, 0.02, 1.000, 1.000, 0.00),
            Planet("Mars", 1.523, 0.09, 1.881, 1.881, 1.85),
            Planet("Jupiter", 5.202, 0.05, 11.861, 1.000, 1.31),
            Planet("Saturn", 9.576, 0.06, 29.628, 2.498, 2.49),
            Planet("Uranus", 19.293, 0.05, 84.747, 7.145, 0.77),
            Planet("Neptune", 30.246, 0.01, 166.344, 14.024, 1.77),
            Planet("Pluto", 39.509, 0.25, 248.348, 20.938, 7.00)]

def retrieve_planet_details()-> list[Planet]:
    return planet

def get_planet(name: str) -> Planet:
    for p in planet:
        if p.name == name:
            return p
    raise ValueError(f"Planet {name} not found")