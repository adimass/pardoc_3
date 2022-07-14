from flask import Blueprint, render_template, request, send_file,session
import pandas as pd 
import json
import os
import database as db

bp_homepage= Blueprint('bp_homepage', __name__)
@bp_homepage.route('/home')
def content_homepage():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')
    role = session['role']
    if role == 'user':
        query="select * from hub where pasId like '%s'"%(session['userId'])
        df = db.df_query(query)
        query = """
            select amount_money from wallet where userId like '%s'        
        """%(session['userId'])
        money = db.execute_query_one(query)
        if len(df) == 0:
            return render_template('content_homepage.html',money=money)
        else:
            return render_template('content_homepage.html', chat=True,money=money)

    elif role == 'dokter':
        return render_template('content_dokter_homepage.html')
    else:
        return render_template('content_admin_homepage.html')

    


    