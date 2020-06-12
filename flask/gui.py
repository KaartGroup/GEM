from flask import (Flask, render_template)
import webview
import threading


def mwin():
    window = webview.create_window(title="Gem Gui", url='', html="", width=100, height=600,
            x=None, y= None, fullscreen=False, \
            hidden=True, frameless=False, \
            confirm_close=False, background_color='#FFF', \
            text_select=False)
    webview.start()
