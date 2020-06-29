from flask import (Flask, render_template, redirect, request)
from eclass import Editor
import webview
import threading
import json

editor = Editor()

app = Flask("__main__")

@app.route("/")
def my_index():
    return render_template('index.html')

@app.route("/gdat", methods=['GET','POST'] )
def getdata():
        if request.method == 'POST':

            req = request.form
            print(req)
            
            editor.team = req["team"]
            editor.name = req["ename"]
            editor.username = req["username"]
            editor.uid = req["editoruid"]
            editor.linecolor = req["elinecolor"]
            editor.nodecolor = req["enodecolor"]
            editor.linewidth = req["elinewidth"]
            editor.nodesize = req["enodesize"]
            editor.nodeshape = req["enodeshape"]

            ejson = json.dumps(editor.__dict__)
            data = open("data.json", "w")
            data.write(ejson)

            return redirect(request.url)

        return render_template("index.html")

app.run(debug=True)