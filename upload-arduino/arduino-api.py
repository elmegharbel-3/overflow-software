import flask
import os
app = flask.Flask(__name__)
@app.route('/')
def index():
    return flask.render_template('index.html')
@app.route("/call_function",methods=['GET',"POST"])
def upload_arduino():
    if flask.request.method == "POST":
        data = flask.request.form.to_dict()
        file_loc = data["file"]
        fbqn = "-b " + data["fbqn"]
        port = "-p " + data["port"]
        print("arduino-cli upload" + " " + fbqn + " " + port + " " + file_loc)
    return flask.render_template('index.html',file_loc=file_loc,port=port,fbqn=fbqn)

if __name__ == '__main__':
    app.run(debug=True, port=8080,host="0.0.0.0",threaded=False)
