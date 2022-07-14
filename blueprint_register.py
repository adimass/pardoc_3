from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db
from datetime import datetime
from uuid import uuid4

bp_register = Blueprint('bp_register', __name__)

@bp_register.route('/register')
def register():

    return render_template('register.html')


@bp_register.route('/register-users', methods=['POST'])
def register_user():

    email = request.form.get("email")
    name = request.form.get("name")
    psw = request.form.get("psw")
    psw2 = request.form.get("psw-repeat")

    if '@' not in email and len(email) <5:
        return redirect("/register")
    if len(psw) < 8 :
        return redirect("/register")
    if psw != psw2:
        return redirect("/register")

    query = '''
    
    select count(*)
    from users
    
    '''
    
    #createuserID
    tl = datetime.today().strftime('%Y%m%d')
    hasil = db.execute_query_one(query)
    hasil = hasil+1
    userid = 'usr'+str(tl)+str(hasil)
    role = 'user'
    socket = uuid4().hex

    insert = """
    
    insert into users values('%s','%s','%s','%s','%s','','','','','','%s')

    """%(str(userid),str(name),str(psw),str(role),str(email),str(socket))

    db.execute_query(insert)

    insert = """
    
    insert into wallet values('%s',0)

    """%(str(userid))

    db.execute_query(insert)


    

    return redirect("/")