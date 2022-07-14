from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db


bp_login = Blueprint("bp_login",__name__)

@bp_login.route("/login",methods=["POST","GET"])
def login():

    email = request.form.get("email")
    password = request.form.get("password")
    query = '''
    select *
    from users
    where email like '%s' and pass like '%s'
    '''%(str(email),str(password))
    user = db.df_query(query)

    if not user.empty:
        parsed = user.to_json(orient="records")
        hasil = json.loads(parsed)
        session["google_login"] = email
        for i in hasil[0].items():
            if str(i[0]) != 'pass':
                session[i[0]] = i[1]
    else :
        print('user not found')

    

    return redirect("/")  

@bp_login.route("/logout")
def logout():
    session.clear()
    return redirect("/")