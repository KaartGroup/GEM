from flask import (Flask, render_template)
import webview
import threading



app = Flask("__main__")

@app.route("/")
def my_index():
    return render_template("index.html")

window = webview.create_window(title="GEM", url='', confirm_close=True, background_color='#FFF', hidden=True)
webview.start()

@app.route("gui")
def showwin():
    return window.show()

app.run(debug=True)