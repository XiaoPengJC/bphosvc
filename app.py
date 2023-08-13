"""
Flask app and endpoints
"""
from flask import Flask, request, send_from_directory
from bpho_service import generate_kepler_correlation, generate_2d_orbit, generate_3d_orbit, generate_2d_orbit_animation, generate_3d_orbit_animation, generate_angle_vs_time, generate_spinograph, generate_2d_imaginary_orbit, generate_3d_imaginary_orbit
from cache import Cache


app = Flask(__name__)


cache = Cache()
cache.register_cache()

@app.route("/")
def healthcheck():
    return "App is working!"


@app.route('/kepler_correlation')
def kepler_correlation():
    filename = "kepler_correlation.png"

    if cache.get(filename) is None:
        generate_kepler_correlation(filename)
        cache.set(filename, True)
    
    return send_from_directory(directory='cache', path=filename, as_attachment=False)


@app.route('/orbit_image')
def orbit_image():
    args = request.args
    input_planets = args.getlist('planet')
    is_3d = args.get('is3d')

    prefix = "3d_img-" if is_3d == "true" else "2d_img-"
    filename = prefix + "_".join(input_planets) + ".png"

    if cache.get(filename) is None:
        generate_3d_orbit(input_planets, filename) if is_3d == "true" else generate_2d_orbit(input_planets, filename)
        cache.set(filename, True)

    return send_from_directory(directory='cache', path=filename, as_attachment=False)


@app.route('/orbit_animation')
def orbit_animation():
    args = request.args
    input_planets = args.getlist('planet')
    is_3d = args.get('is3d')

    prefix = "3d_anim-" if is_3d == "true" else "2d_anim-"
    filename = prefix + "_".join(input_planets) + ".gif"

    if cache.get(filename) is None:
        generate_3d_orbit_animation(input_planets, filename) if is_3d == "true" else generate_2d_orbit_animation(input_planets, filename)
        cache.set(filename, True)

    return send_from_directory(directory='cache', path=filename, as_attachment=False)


@app.route('/angle_vs_time')
def angle_vs_time():
    args = request.args
    input_planet = args.get('planet')

    prefix = "angle_vs_time-"
    filename = prefix + input_planet + ".png"

    if cache.get(filename) is None:
        generate_angle_vs_time(input_planet, filename)
        cache.set(filename, True)
    
    return send_from_directory(directory='cache', path=filename, as_attachment=False)


@app.route('/spinograph')
def spinograph():
    args = request.args
    input_planets = args.getlist('planet')

    assert len(input_planets) == 2

    prefix = "spinograph-"
    filename = prefix + "_".join(input_planets) + ".png"

    if cache.get(filename) is None:
        generate_spinograph(input_planets, filename)
        cache.set(filename, True)
    
    return send_from_directory(directory='cache', path=filename, as_attachment=False)


@app.route('/imaginary_orbit')
def imaginary_orbit():
    args = request.args
    centre_planet = args.get('centre')
    input_planets = args.getlist('planet')
    is_3d = args.get('is3d')


    prefix = "imaginary_3d_anim-" if is_3d == "true" else "imaginary_2d_anim-"
    filename = prefix + "_".join(input_planets) + ".png"

    if cache.get(filename) is None:
        generate_3d_imaginary_orbit(centre_planet, input_planets, filename) if is_3d == "true" else generate_2d_imaginary_orbit(centre_planet, input_planets, filename)
        cache.set(filename, True)
    
    return send_from_directory(directory='cache', path=filename, as_attachment=False)


if __name__ == "__main__":
    app.run()
