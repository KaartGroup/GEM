from flask import (Flask, render_template, redirect)
import webview
import threading



app = Flask("__main__")

@app.route("/")
def my_index():
    return render_template('index.html')





app.run(debug=True)