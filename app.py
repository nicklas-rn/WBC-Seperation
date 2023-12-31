from flask import Flask, Response, render_template, request, jsonify, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
import time
import distance_detection
from flask_cors import CORS, cross_origin
import serial.tools.list_ports
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

MM_CONVERSION = 10.0 # distance in mm / distance in pixels
# set to 1, then compare distance that program outputs (p) with distance measured with ruler (m) and set value to m/p
STEPPER_HEIGHT = 60 # travel in mm
# set to highest position - lowest position of laser
STEPPER_STEPS = 600 # amount of steps that stepper does for entire stepper_height


positions = {
    'white': 0,
    'ficole': 0,
    'red': 0,
}


@app.route('/select_port', methods=['POST'])
def select_port():
    global device

    port = request.args.get('port')

    print(port)

    device_port = [p.device for p in serial.tools.list_ports.comports() if p.name == port][0]

    device = serial.Serial(device_port, 115200, timeout=0.5)

    return jsonify({'success': 'ok'})

@app.route('/')
def index():

    ports = serial.tools.list_ports.comports()

    print([port.name for port in ports])

    ports_serialized = [{'name': port.name, 'description': port.description} for port in ports]
    print(ports_serialized)

    try:
        selected_port = device.port.replace('/dev/', '')
    except:
        selected_port = ''

    print(selected_port)

    context = {
        'ports': ports_serialized,
        'selected_port': selected_port,
    }

    return render_template('index.html', context=context)


@app.route('/video_feed')
def video_feed():
    return Response(distance_detection.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/change_value_stepper', methods=['POST'])
def change_value_stepper():
    value = request.args.get('value')
    print(f"set stepper to {value}")
    device.write(bytes(f"stepper,{value}, ", 'utf-8'))

    return jsonify({'success': 'ok'})


@app.route('/change_value_laser', methods=['POST'])
def change_value_laser():
    value = request.args.get('value')
    print(f"set laser to {value}")
    device.write(bytes(f"laser,{value}, ", 'utf-8'))

    return jsonify({'success': 'ok'})


@app.route('/move_stepper_position', methods=['POST'])
def move_stepper_position():
    position = request.args.get('position')
    value = positions[position] * MM_CONVERSION * STEPPER_STEPS / STEPPER_HEIGHT
    print(f"set stepper to {position} at {value}")
    device.write(bytes(f"stepper,{value}, ", 'utf-8'))

    return jsonify({'success': 'ok', 'value': value})


if __name__ == '__main__':
    app.run(debug=True)





