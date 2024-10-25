import flask 
import os 
import subprocess
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
        file_name = thefile.filename  
        dir_name = file_name.rstrip(".ino")
        print(file_name)
        if os.path.exists(f"sketches/{dir_name}") == False:
            os.mkdir(f"sketches/{dir_name}")
            thefile.save(f"sketches/{dir_name}/{file_name}")   
            file_loc = f"sketches/{dir_name}"
            fbqn = data["fbqn"]         
            port = data["port"]         
            compile = subprocess.run(["arduino-cli","compile","-b",fbqn,"-p",port,file_loc],stdout= subprocess.PIPE,universal_newlines=True)
            upload = subprocess.run(["arduino-cli","upload","-b",fbqn,"-p",port,file_loc],stdout= subprocess.PIPE,universal_newlines=True)   
            return flask.render_template('index.html',file_loc=file_loc,port=port,fbqn=fbqn,compile_res=compile.stdout,upload_res=upload.stdout)  
        else:
            return flask.render_template('index.html',exist=True)
if __name__ == '__main__':     
    app.run(debug=True, port=8080,host="0.0.0.0",threaded=False)

