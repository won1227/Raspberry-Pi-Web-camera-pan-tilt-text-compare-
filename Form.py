from flask import Flask, render_template,url_for,request,Response,redirect
from camera_pi import Camera
import os

app = Flask(__name__)
PW = 1234

global panServoAngle
global tiltServoAngle
panServoAngle = 90
tiltServoAngle = 90

panPin = 27
tiltPin = 17  #servo_motor

@app.route('/')
@app.route('/form_send')											#초기화면
def form_send():
	return render_template('form_send.html')

@app.route('/form_recv',methods=['POST'])
def form_recv():													#결과화면
	if request.method == 'POST':
		data = request.form

	else:
		data = {}

	return render_template('form_result.html',data=data,PW_value=PW)

@app.route('/picam')												#파이_카메라
def index():														#비디오 스트리밍
    return redirect(url_for('form_send'))


def gen(camera):													#비디오 스트리밍 함수
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():													#비디오 스트리밍 루트
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


#angle
@app.route("/<servo>/<angle>")										#카메라 팬 / 틸트 제어
def move(servo, angle):
	global panServoAngle
	global tiltServoAngle
	if servo == 'pan':
		if angle == '+':
			panServoAngle = panServoAngle + 10
		else:
			panServoAngle = panServoAngle - 10
		os.system("python3 angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
	if servo == 'tilt':
		if angle == '+':
			tiltServoAngle = tiltServoAngle + 10
		else:
			tiltServoAngle = tiltServoAngle - 10
		os.system("python3 angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))
	
	return redirect(url_for('index')) 


if __name__ =='__main__':
	app.run(debug=True, host = '192.168.0.7', port= 5000)
