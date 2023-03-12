from flask import *
import cv2

myapp = Flask(__name__)
myapp.secret_key = "VERY_VERY_SECRET"

camera = cv2.VideoCapture(-1)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera 
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # print("Success: ", success)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            # print("OLD: ",  type(buffer))            
            frame = buffer.tobytes()
            # print("FRAME: ", type(frame))
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@myapp.route('/home')
def index():
    print("Ghar aagya...")
    return render_template("index.html")

@myapp.route('/video_feed')
def video_feed():
    print("Video aaega ab...")
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    myapp.run(host = "0.0.0.0", port="8081")