from flask import Response
from app import camera, pantilt
from app.camera import bp


def gen(camera):
	"""Video streaming generator function."""
	camera.start_camera_thread()
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@bp.route('/', methods=['GET'])
def cam():
	"""Video streaming route. Put this in the src attribute of an img tag."""
	return Response(gen(camera),
					mimetype='multipart/x-mixed-replace; boundary=frame'), 200

@bp.route('/camOff', methods=['GET'])  
def camOff():
	camera.stop_camera_thread()
	return '', 204


@bp.route('/move/<move>', methods=['GET'])
def move(move):
    '''
     move = 0 -> default
     move = 1 -> pan right
     move = 2 -> pan left
     move = 3 -> tilt up
     move = 4 -> tilt down
    '''
    moves = ['center', 'right', 'left', 'up', 'down']

    pantilt.pan_and_tilt(moves.index(move))
    return '', 204
