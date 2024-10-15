import flask 
import os 
app = flask.Flask(__name__) 
print("hello world")
@app.route('/') 
def index():     
    return flask.render_template('index.html') 
@app.route("/call_function",methods=['GET',"POST"]) 
def upload_arduino():     
    if flask.request.method == "POST":         
        data = flask.request.form.to_dict()         
        thefile = flask.request.files['file']   
        thefile.save("main-sketch/main-sketch.ino")   
        file_loc = f"~/gui-arduino/main-sketch"
        fbqn = "-b " + data["fbqn"]         
        port = "-p " + data["port"]         
        os.system("arduino-cli compile" + " " + fbqn + " " + file_loc)         
        os.system("arduino-cli upload" + " " + fbqn + " " + port + " " + file_loc)     
        return flask.render_template('index.html',file_loc=file_loc,port=port,fbqn=fbqn)  
    if __name__ == '__main__':     
        app.run(debug=True, port=8080,host="0.0.0.0",threaded=False)
