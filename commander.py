#! /usr/bin/python

"""
Simple web interface for Anki Vector

"""

import anki_vector
from anki_vector import events
from flask import Flask, render_template, request, Response, redirect, url_for
import time
import io
import json

robot = anki_vector.Robot()
robot.connect()
robot.camera.init_camera_feed()


controls = {
    'a' : "forward_left",
    'q' : "backward_left",
    'p' : "forward_right",
    'l' : "backward_right",
    'o' : "head_up",
    'k' : "head_down",
    ' ': "stop"
}

WHEELS_SPEED = 200 # mm/sec
wheels_motion = {"left":0,"right":0} # in mm / sec

HEAD_SPEED = 4 # rad/sec
head_motion = 0

# Stream video from Vector
def stream_video():
    while True:
        time.sleep(0.1)
        image = robot.camera.latest_image.raw_image
        temp_image = io.BytesIO()
        image.convert('RGBA').save(temp_image, format='PNG')
        temp_image.seek(0, 0)
        b = temp_image.getvalue()
        yield (b'--frame\r\n' + b'Content-Type: image/jpg\r\n\r\n' + b + b'\r\n\r\n')
        

app = Flask(__name__)

@app.route('/')
def home():
    # robot.behavior.say_text("Hello")
    return render_template('commander.html')

@app.route('/video_stream')
def video_stream():
  return Response(stream_video(), mimetype='multipart/x-mixed-replace; boundary=frame')
  

@app.route('/keydown',methods=["POST"])
def keydown():
    global wheels_motion
    global head_motion
    key = request.form['key']
    if key in controls :
        command = controls[key]
        if command == "forward_right":
            wheels_motion["right"] = WHEELS_SPEED
        if command == "forward_left":
            wheels_motion["left"] = WHEELS_SPEED
        if command == "backward_right":
            wheels_motion["right"] = -WHEELS_SPEED
        if command == "backward_left":
            wheels_motion["left"] = -WHEELS_SPEED
        if command == "stop":
            wheels_motion["right"] = 0
            wheels_motion["left"] = 0
        if command == "head_up":
            head_motion = HEAD_SPEED
        if command == "head_down":
            head_motion = -HEAD_SPEED
        robot.motors.set_wheel_motors(wheels_motion["left"],wheels_motion["right"])
        robot.motors.set_head_motor(head_motion)
    return json.dumps(wheels_motion)

@app.route('/keyup',methods=["POST"])
def keyup():
    global wheels_motion
    global head_motion
    key = request.form['key']
    if key in controls :
        command = controls[key]
        if command == "forward_right":
            wheels_motion["right"] = 0
        if command == "forward_left":
            wheels_motion["left"] = 0
        if command == "backward_right":
            wheels_motion["right"] = 0
        if command == "backward_left":
            wheels_motion["left"] = 0
        if command == "stop":
            wheels_motion["right"] = 0
            wheels_motion["left"] = 0
        if command == "head_up":
            head_motion = 0
        if command == "head_down":
            head_motion = 0
        robot.motors.set_wheel_motors(wheels_motion["left"],wheels_motion["right"])
        robot.motors.set_head_motor(head_motion)
    return json.dumps(wheels_motion)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=80)