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

global stepper
global laser

def initialize_ports():
    ports = serial.tools.list_ports.comports()

    print([port.name for port in ports])

    global stepper
    global laser

    try:
        #stepper = serial.Serial(port='/dev/usbmodem1101', baudrate=115200, timeout=.1)
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'USB2.0-Serial' in p.description or p.name =='COM7'
        ]
        print(arduino_ports)
        if not arduino_ports:
            raise IOError("No Arduino found")
        if len(arduino_ports) > 1:
            print('Multiple Arduinos found - using the first')

        stepper = serial.Serial(arduino_ports[0])
    except:
        stepper = serial.Serial()
        print("connecting to stepper failed")
    
    try:
        laser = serial.Serial(port='/dev/ttyUSB2', baudrate=115200, timeout=.1)
    except:
        laser = serial.Serial()
        print("connecting to laser failed")



    time.sleep(1)

initialize_ports()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(distance_detection.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/change_value_stepper', methods=['POST'])
def change_value_stepper():
    value = request.args.get('value')
    print(f"set stepper to {value}")
    stepper.write(bytes(f"stepper,{value}, ", 'utf-8'))

    return jsonify({'success': 'ok'})


@app.route('/change_value_laser', methods=['POST'])
def change_value_laser():
    value = request.args.get('value')
    print(f"set laser to {value}")
    stepper.write(bytes(f"laser,{value}, ", 'utf-8'))

    return jsonify({'success': 'ok'})


@app.route('/move_stepper_position', methods=['POST'])
def move_stepper_position():
    position = request.args.get('position')
    value = positions[position] * MM_CONVERSION * STEPPER_STEPS / STEPPER_HEIGHT
    print(f"set stepper to {position} at {value}")
    stepper.write(bytes(f"stepper,{value}, ", 'utf-8'))

    return jsonify({'success': 'ok', 'value': value})


if __name__ == '__main__':
    app.run(debug=True)





