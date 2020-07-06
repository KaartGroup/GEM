from flask import (Flask, render_template, redirect, request, jsonify, json)
from eclass import Editor
from werkzeug.utils import secure_filename
from jinja2 import (Template, Environment, FileSystemLoader)
import webview
import threading
import json
import os
import copy
import ast
import string
import re

editor = Editor()

Editorlist = {}

Editors = {}

app = Flask("__main__")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def my_index():
    return render_template('index.html')

@app.route("/add", methods=['GET','POST'] )
def getdata():
    if request.method == 'POST':

        req = request.form.to_dict()
        print('req',req)
        editor.name = req["ename"]
        editor.team = req["team"]
        editor.username = req["username"]
        editor.uid = req["editoruid"]
        editor.linecolor = req["elinecolor"]
        editor.nodecolor = req["enodecolor"]
        editor.linewidth = req["elinewidth"]
        editor.nodesize = req["enodesize"]
        editor.nodeshape = req["enodeshape"]

        
        for key, val in req.items():
            Editorlist[key] = req[key]

        del Editorlist['ename']



        Editors = { editor.name : Editorlist}
        print(Editors)

        return redirect(request.url)

    return render_template("index.html", flask_data = )



@app.route("/upload", methods=['GET','POST'])
def getupload():
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
    getinfile()

    return render_template("index.html")
    
def getinfile():
    for file in "/uploads":
        infile = file
        infile = str(infile[0])
    with open (infile, "r+") as reader:
        infile_text = reader.read()
        typecheck = infile.split("{")
        if typecheck[0] == ("meta"):
            oldstyle = True
        else:
            oldstyle = False
        typecheck = ""
        print (oldstyle)


if __name__ == "__main__":
    app.run(debug=True)