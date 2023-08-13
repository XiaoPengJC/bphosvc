import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter

from bpho_computation import kepler_correlation, plot_orbit, animate_orbit, angle_vs_time, plot_spinograph, plot_imaginary_orbit
from constants.data import retrieve_planet_details, get_planet
from constants.colours import get_colours

dir_path = os.path.abspath(os.path.dirname(__file__))


#Task 1
def generate_kepler_correlation(filename: str):
    fig, ax = figure_setup(is_3D_orbit=False)
    kepler_correlation(retrieve_planet_details())
    finish_figure(ax, "Kepler's Third Law")

    fig.savefig(os.path.join(dir_path, "cache", filename))
    close_figure()


# Task 2A
def generate_2d_orbit(input_planets: list[str], filename: str):
    fig, ax = figure_setup(is_3D_orbit=False)
    input_planets = [get_planet(_) for _ in input_planets]
    plot_orbit(input_planets, True, False, ax)
    finish_figure(ax, "2D Planet Orbits")

    fig.savefig(os.path.join(dir_path, "cache", filename))
    close_figure()


# Task 2B
def generate_3d_orbit(input_planets: list[str], filename: str):
    fig, ax = figure_setup(is_3D_orbit=True)
    input_planets = [get_planet(_) for _ in input_planets]
    plot_orbit(input_planets, True, True, ax)
    finish_figure(ax, "3D Planet Orbits")

    fig.savefig(os.path.join(dir_path, "cache", filename))
    close_figure()


#Task 3
def generate_2d_orbit_animation(input_planets: list[str], filename : str, colours: list[str] = get_colours()):
    fig, ax = figure_setup(is_3D_orbit=False)
    input_planets = [get_planet(_) for _ in input_planets]
    animation = animate_orbit(input_planets, False, ax, fig, colours)
    finish_figure(ax, "2D Planet Orbits")

    writer = PillowWriter(fps=15, bitrate=400)
    animation.save(os.path.join(dir_path, "cache", filename), writer=writer)
    close_figure()


#Task 4
def generate_3d_orbit_animation(input_planets: list[str], filename: str, colours: list[str] = get_colours()):
    fig, ax = figure_setup(is_3D_orbit=True)
    input_planets = [get_planet(_) for _ in input_planets]
    animation = animate_orbit(input_planets, True, ax, fig, colours)
    finish_figure(ax, "3D Planet Orbits")

    writer = PillowWriter(fps=15, bitrate=400)
    animation.save(os.path.join(dir_path, "cache", filename), writer=writer)
    close_figure()


#Task 5
def generate_angle_vs_time(input_planet: str, filename: str):
    fig, ax = figure_setup(is_3D_orbit=False)
    input_planet = get_planet(input_planet)
    angle_vs_time(ax, input_planet)
    finish_figure(ax, "Angle vs Time")

    fig.savefig(os.path.join(dir_path, "cache", filename))
    close_figure()


# Task 6
def generate_spinograph(input_planets: list[str], filename: str):
    fig, ax = figure_setup(is_3D_orbit=False)
    input_planets = [get_planet(_) for _ in input_planets]
    plot_spinograph(input_planets, False, ax)
    finish_figure(ax, "Spinograph")

    fig.savefig(os.path.join(dir_path, "cache", filename))
    close_figure()


# Task 7A
def generate_2d_imaginary_orbit(input_centre_planet: str, input_planets: list[str], filename: str):
    fig, ax = figure_setup(is_3D_orbit=False)
    input_planets = [get_planet(_) for _ in input_planets]
    input_centre_planet = get_planet(input_centre_planet)
    plot_imaginary_orbit(input_centre_planet, input_planets, False, ax)
    finish_figure(ax, "2D Imaginary Orbits")

    fig.savefig(os.path.join(dir_path, "cache", filename))
    close_figure()


# Task 7B
def generate_3d_imaginary_orbit(input_centre_planet: str, input_planets: list[str], filename: str):
    fig, ax = figure_setup(is_3D_orbit=True)
    input_planets = [get_planet(_) for _ in input_planets]
    input_centre_planet = get_planet(input_centre_planet)
    plot_imaginary_orbit(input_centre_planet, input_planets, True, ax)
    finish_figure(ax, "3D Imaginary Orbits")

    fig.savefig(os.path.join(dir_path, "cache", filename))
    close_figure()


## GRAPH FUNCTIONS

def figure_setup(is_3D_orbit: bool):
    fig = plt.figure()
    fig.set_figwidth(8)
    fig.set_figheight(8)
    ax = fig.add_subplot(projection = "3d") if is_3D_orbit else fig.add_subplot()
    return fig, ax


def finish_figure(ax, title: str) -> None:
    # SHOW THE GRAPH
    ax.legend()
    ax.set_title(title)
    ax.grid()


def show_figure():
    plt.show()


def close_figure():
    plt.close()