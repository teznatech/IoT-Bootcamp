from flask import render_template, Response, url_for, jsonify, request
from app.routine_control import bp
from app import routineControl

@bp.route("/addRoutine", methods=['GET'])
def addRoutine():
    light_splice = ''
    if request.args.get('task') == 'Light':
        light_splice = request.args.get('light_splice')
        
    task = routineControl.save_routine(request.args.get('routine_id'),request.args.get('task'),\
			request.args.get('days'),request.args.get('times'), light_splice)
            
    return jsonify({'task': task}), 201

@bp.route("/removeRoutine", methods=['GET'])
def removeRoutine():
	routineId = request.args.get('routine_id')
	routineControl.delete_routine(routineId)
	return jsonify({'routine': routineId}), 201

@bp.route("/getRoutines", methods=['GET'])
def getRoutines():
	routines = routineControl.get_routines()
	return jsonify({'routines': routines}), 201