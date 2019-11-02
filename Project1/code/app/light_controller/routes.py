from app import lightControl
from app.light_controller import bp
from flask import request, render_template


@bp.route("/switch")
def switch():
    return render_template('lights/switch.html')


@bp.route("/on")
def light_on():
    red = int(request.args.get('red', 255))
    green = int(request.args.get('green', 255))
    blue = int(request.args.get('blue', 255))
    brightness = float(request.args.get('brightness', 0.2))
    lightControl.lightSwitch(red, green, blue, brightness)
    return '', 204

@bp.route("/off")
def light_off():
    lightControl.lightSwitch(0,0,0,0)
    return '', 204