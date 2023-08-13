# BPhO Computational Challenge 2023
# Challenges 1 - 7

from dataclasses import dataclass
import matplotlib.pyplot as plt
from constants.data import Planet
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.interpolate import interp1d


@dataclass
class PlanetCoordinates:
    x: float
    y: float
    z: float


## GRAPH FUNCTIONS

def plot_centre(centre_planet_name: str, axis) -> None: #TODO
    """
    Plot a planet at the centre of the planetary system
    """
    if centre_planet_name == "Sun":
        axis.plot(0, 0, "o", color = "yellow", label = centre_planet_name)
    else:
        axis.plot(0, 0, "o", label = centre_planet_name)


## ORBIT FUNCTIONS

# Calculate the elliptical orbits of each planet
def calculate_orbit_position(planet: Planet, theta, orbit_3D) -> PlanetCoordinates:
    """
    Calculates the x and y coordinates of the orbit of a planet at a given angle theta
    """

    def compute_r(a: float, ecc: float, theta: float):
        """
        Computes the radius of the orbit at a given angle theta
        """
        return (a*(1-ecc**2))/(1-ecc*np.cos(theta))

    # Calculate r
    r = compute_r(planet.a, planet.ecc, theta)

    # Calculate x coordinate
    x = r * np.cos(theta)

    # Calculate y coordinate
    y = r * np.sin(theta)

    # If 3D orbits are to be calculated
    x = x * np.cos(planet.beta * np.pi / 180) if orbit_3D else x
    z = x * np.sin(planet.beta * np.pi / 180) if orbit_3D else None

    return PlanetCoordinates(x, y, z)


# Task 1 - 2D
def kepler_correlation(planets: list[Planet]) -> None:
    """
    Plots the Kepler's Third Law correlation
    """

    def plot_kepler_correlation():
        plt.plot(x, y, marker="s", markerfacecolor="red", markeredgecolor="red", label="Kepler's Third Law")
        plt.title("Kepler's Third Law")
        plt.xlabel("(a/AU)^(3/2)")
        plt.ylabel("T/Yr")
    

    x = []
    y = []
    for planet in planets:
        x.append(planet.a ** (3 / 2))
        y.append(planet.p)

    plot_kepler_correlation()


# Task 2 - 2D

def plot_orbit(input_planets: list[Planet], has_sun: bool, is_3D_orbit: bool, ax) -> None:

    def plot_planet(planet: Planet, ax, is_3D_orbit):
        if is_3D_orbit:
            ax.plot(x, y, z, label = planet.name)
            ax.set_zlabel("z/AU")
        else:
            ax.plot(x, y, label = planet.name)
    
    def plot_sun(has_sun, ax):
        if has_sun:
            plot_centre("Sun", ax)

    def set_labels():
        ax.set_xlabel("x/AU")
        ax.set_ylabel("y/AU")


    for input_planet in input_planets:
        x = []
        y = []
        z = []
        theta = 0
        for _ in range(1000):
            coord = calculate_orbit_position(input_planet, theta, is_3D_orbit)
            x.append(coord.x)
            y.append(coord.y)

            if is_3D_orbit:
                z.append(coord.z)

            # Increase theta
            theta += (0.002*np.pi)

        plot_planet(input_planet, ax, is_3D_orbit)
    plot_sun(has_sun, ax)
    set_labels()
    

def animate_orbit(input_planets: list[Planet], orbit_3D: bool, ax, fig, colours: list[str]):

    def animate(i: int, input_planets: list[Planet], markers: list[plt.Line2D]) -> list[plt.Line2D]:
        """
        Animate the markers for the animation
        """
        for index, input_planet in enumerate(input_planets):
            #theta = (2 * np.pi * (i * 0.002)) / input_planet.modified_p
            # Earth and Jupiter should turn one full rotation in 60 frames
            num_frames = 15 * input_planet.modified_p
            theta = (2 * np.pi * ((i % num_frames) / num_frames))
            planet_coord = calculate_orbit_position(input_planet, theta, orbit_3D)

            markers[index].set_data(planet_coord.x, planet_coord.y)

            if orbit_3D:
                markers[index].set_3d_properties(planet_coord.z)
                
        return markers

    def get_markers(ax):
        # CREATE THE MARKERS FOR THE ANIMATIONS
        if orbit_3D:
            markers = [ax.plot([0], [0], [0], marker = "o", color = colours[_])[0] for _ in range(9)]
        else:
            markers = [ax.plot([0], [0], marker = "o", color = colours[_])[0] for _ in range(9)]
        
        return markers

    def init():
        """
        Initialise the markers for the animation
        """
        markers = get_markers(ax)
        for marker in markers:
            marker.set_data([], [])

        return markers

    plot_orbit(input_planets, True, orbit_3D, ax)
    final_frames = 15 * input_planets[-1].modified_p
    final_frames = int(np.ceil(final_frames))
    return FuncAnimation(fig, animate, frames = final_frames, init_func = init,
                                fargs = (input_planets, get_markers(ax)), interval = 1, blit = True)


# Task 5
def angle_vs_time(ax, input_planet: Planet) -> None:

    def calculate_angle_vs_time(t, P, ecc, theta0) -> np.ndarray:

        # Angle step for Simpson's rule
        dtheta = 1/1000

        # Number of orbits
        N = np.ceil(t[-1] / P)
        
        # Define array of polar angles for orbits
        theta = np.arange(theta0, (2 * np.pi * N + theta0) + dtheta, dtheta)

        # Evaluate integrand of time integral
        f = (1 - ecc * np.cos(theta)) ** (-2)

        # Define Simpson rule coefficients c = [1, 4, 2, 4, 2, 4, ....1]
        L = len(theta)
        isodd = np.remainder(np.arange(1, L-1), 2)
        isodd[isodd == 1] = 4
        isodd[isodd == 0] = 2
        c = np.concatenate(([1], isodd, [1]))

        # Calculate array of times
        tt = P * ((1 - ecc ** 2) ** (3/2)) * (1 / (2 * np.pi)) * dtheta * (1 / 3) * np.cumsum(c * f)

        # Interpolate the polar angles for the eccentric orbit at the circular orbit times
        theta = interp1d(tt, theta, kind='cubic')
        theta = theta(t)
        
        return theta
    
    def plot_angle_vs_time(ax):
        ax.cla()
        ax.plot(t, theta_circ, label = "Circular")
        ax.plot(t, theta_ecc, label = "Eccentric")
        ax.set_xlabel("time/years")
        ax.set_ylabel("orbit polar angle/rad")


    t = np.linspace(1, 800, 800)

    theta_circ = calculate_angle_vs_time(t, input_planet.p, 0, 0)
    theta_ecc = calculate_angle_vs_time(t, input_planet.p, input_planet.ecc, 0)

    plot_angle_vs_time(ax)


# Task 6
def plot_spinograph(input_planets: list[Planet], is_3D_orbit: bool, ax) -> None:
    planet1 = input_planets[0]
    planet2 = input_planets[1]
    tmax = max([planet1.p, planet2.p])  # Max time /years
    dt = 10 * tmax / 1234  # Time interval in years
    t = 0

    while t < 10 * tmax:
        x = []
        y = []

        theta = (2 * np.pi * (t)) / planet1.p
        planet_coord = calculate_orbit_position(planet1, theta, is_3D_orbit)
        x.append(planet_coord.x)
        y.append(planet_coord.y)

        theta = (2* np.pi * (t)) / planet2.p
        planet_coord = calculate_orbit_position(planet2, theta, is_3D_orbit)
        x.append(planet_coord.x)
        y.append(planet_coord.y)
        
        ax.plot(x, y, color = "black", linewidth = 0.5)
        #Update time t /years
        t = t + dt

    plot_orbit(input_planets, False, False, ax)


# Task 7
def plot_imaginary_orbit(input_centre_planet: Planet, input_planets: list[Planet], is_3D_orbit: bool, ax) -> None:

    def calculate_planet_orbit(centre_planet: Planet, 
                                planet: Planet
                                ) -> (list[float], list[float], list[float]):
        
        # Calculate the position of planet 1 (eg. Earth, which will be at the centre of the solar system)
        coord_x = []
        coord_y = []
        coord_z = []
            
        tmax = max([centre_planet.p, planet.p])  # Max time /years
        dt = 10*tmax/1234  # Time interval in years
        t = 0

        for _ in range(1000):

            theta = (2 * np.pi * (t)) / centre_planet.p
            planet1 = calculate_orbit_position(centre_planet, theta, is_3D_orbit)
            
            theta = (2 * np.pi * (t)) / planet.p
            planet2 = calculate_orbit_position(planet, theta, is_3D_orbit)
            
            coord_x.append(planet2.x - planet1.x)
            coord_y.append(planet2.y - planet1.y)
            
            if is_3D_orbit:
                coord_z.append(planet2.z - planet1.z)
            
            # Update time t /years
            t = t + dt
        return coord_x, coord_y, coord_z

    def set_labels(is_3D_orbit: bool):
        ax.set_xlabel("x/AU")
        ax.set_ylabel("y/AU")
        if is_3D_orbit:
            ax.set_zlabel("z/AU")

    # Plot the centre planet
    plot_centre(input_centre_planet.name, ax)

    # Plot the orbits of the other planets
    for planet in input_planets:
        coord_x, coord_y, coord_z = calculate_planet_orbit(input_centre_planet, planet)

        if is_3D_orbit:
            ax.plot(coord_x, coord_y, coord_z, label = planet.name)
        else:
            ax.plot(coord_x, coord_y, label = planet.name)
    
    set_labels(is_3D_orbit)