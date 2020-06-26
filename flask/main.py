from flask import (Flask, render_template, redirect, request)
import webview
import threading



app = Flask("__main__")

@app.route("/")
def my_index():
    return render_template('index.html')

@app.route("/", methods=['POST'] )
def getdata():
    if request.method == 'POST':
        team = request.form('team')
        print(team)
    return team


app.run(debug=True)