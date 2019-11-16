from app import lightControl
from app.light_controller import bp
from flask import request, render_template, jsonify
import os, json


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
    lightstat = '/home/pi/IoT-Bootcamp/Project1/code/app/static/record/light-status.json'
        with open(lightstat, "r+") as file:
            file.seek(0)
            json.dump({'status':True,
                        'red': red,
                        'green': green,
                        'blue': blue,
                        'brightness': brightness
                        }, file)
            file.truncate()
    return '', 204

@bp.route("/off")
def light_off():
    lightControl.lightSwitch(0,0,0,0)
    lightstat = '/home/pi/IoT-Bootcamp/Project1/code/app/static/record/light-status.json'
        with open(lightstat, "r+") as file:
            data = json.load(file)
            file.seek(0)
            json.dump({'status': False,
                        'red': data['red'],
                        'green': data['green'],
                        'blue': data['blue'],
                        'brightness': data['brightness']
                        }, file)
            file.truncate()
    return '', 204

@bp.route("/status")
def light_status():
    lightstat = '/home/pi/IoT-Bootcamp/Project1/code/app/static/record/light-status.json'
    data = ''
    with open(lightstat, "r") as json_file:
        data = json.load(json_file)
    return jsonify(data), 200