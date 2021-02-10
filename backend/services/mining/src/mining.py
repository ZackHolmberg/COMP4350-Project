from src import app, socketio

@app.route("/")
@app.route("/mining")
def index():
    return "Hello From the Mining"

@socketio.on('my event')
def handle(message):
    socketio.emit("my response", message, callback=msg)

def msg(methods=['GET', 'POST']):
    print('message was received!!!')
