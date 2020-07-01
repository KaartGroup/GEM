from flask import (Flask, render_template, redirect, request, jsonify)
from eclass import Editor
from werkzeug.utils import secure_filename
import webview
import threading
import json
import os
import copy

editor = Editor()

Editorlist = {}

app = Flask("__main__")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def my_index():
    return render_template('index.html')

@app.route("/add", methods=['GET','POST'] )
def getdata():
        if request.method == 'POST':

            req = request.form
            print(req)

            for key in req:
                Editorlist[key] = req[key]
                str(Editorlist)

            return redirect(request.url)

        return render_template("index.html", flask_data=(Editorlist))



@app.route("/upload", methods=['GET','POST'])
def upload():
    target = os.path.join(APP_ROOT, "uploads/")
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("upfile"):
        print(file)
        filename = file.filename
        destination = "/".join((target, filename))
        print(destination)
        file.save(destination)


    return render_template("index.html")
    



if __name__ == "__main__":
    app.run(debug=True)