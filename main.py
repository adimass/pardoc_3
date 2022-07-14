from flask import Flask, render_template, redirect, url_for, send_file,session, abort, redirect, request
from flask.helpers import flash
from datetime import timedelta
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import sqlite3
from uuid import uuid4


app = Flask(__name__)
app.secret_key = b'XPfUfGyVOG27419oLKG51o0TMBKfSTJS9nmypRzM'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)
SESSION_REFRESH_EACH_REQUEST = True



#this is for 
dotenv_path = Path('config/.env')
load_dotenv(dotenv_path=dotenv_path)
SERVER_RUN = os.getenv('run_server')
DATABASE = os.getenv('db_name')


# @app.errorhandler(Exception)
# def server_error(err):
#     app.logger.exception(err)
#     return "Error server, please contact a-team", 500


# @socketio.on('message')
# def handleMessage(msg):
#     print('Massage' + msg)
#     send(msg, broadcast=True)

@app.route("/")
def content_main():

    if "google_login" not in session:
        return render_template('login.html')
    else:
        return redirect('home')


### INITIALIZE LOGIN ###
from blueprint_login import bp_login
app.register_blueprint(bp_login)

### INITIALIZE HOMEPAGE ###
from blueprint_homepage import bp_homepage
app.register_blueprint(bp_homepage)

from blueprint_profile import bp_profile
app.register_blueprint(bp_profile)

from blueprint_self_diagnose import bp_self_diagnose
app.register_blueprint(bp_self_diagnose)

from blueprint_register import bp_register
app.register_blueprint(bp_register)

from blueprint_chat import bp_chat
app.register_blueprint(bp_chat)

from blueprint_transaksi import bp_transaksi
app.register_blueprint(bp_transaksi)

if __name__ == '__main__':

    # print(SERVER_RUN)
    app.run('localhost', 8080,debug=False)
    
    # socketio.run(app,debug=True)

    # socketio.run(app, host='localhost',port=8080,debug=True)