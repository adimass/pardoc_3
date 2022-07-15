from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db
from datetime import datetime

bp_chat = Blueprint("bp_chat",__name__)

@bp_chat.route('/private',methods=["POST","GET"])
def content_private_chat():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')
    if session['role'] == 'user':
        query = """
            select *
            from pesan
            where pengirimId like '%s' or penerimaId like '%s'
        """%(session['userId'],session['userId'])
    else:
        user = request.args.get("userId")
        query = """
            select *
            from pesan
            where pengirimId like '%s' or penerimaId like '%s'
        """%(user,user)
    df = db.df_query(query)

    if len(df) == 0:
        query = """
        SELECT userId FROM users
        where role like 'dokter'
        ORDER BY RANDOM() LIMIT 1
        """
        dokter = db.execute_query_one(query)
        query ="""
        insert into hub values('%s','%s')
        """%(dokter,session['userId'])
        db.execute_query(query)
        if session['role'] == 'user':
            return render_template('content_private_chat.html')
        else:
            return render_template('content_private_chat.html',user=user)
    else :
        array_chat = df.values.tolist()
        if session['role'] == 'user':
            return render_template('content_private_chat.html',array_chat=array_chat)
        else:
            return render_template('content_private_chat.html',array_chat=array_chat,user=user)


@bp_chat.route('/send',methods=["POST","GET"])
def content_send_chat():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')
    if session['role'] == 'user':
        query ="""
        select count(*)
        from pesan
        """
        jml = db.execute_query_one(query)
        jml = jml+1
        query = """
        select dokId
        from hub
        where pasId like '%s'
        """%(session['userId'])
        dokter = db.execute_query_one(query)
        isi = request.form.get("chat")
        tl = datetime.today().strftime('%Y-%m-%d')
        hl = datetime.today().strftime('%H:%M')
        query = """
        insert into pesan values('%s','%s','%s','%s','%s','%s','')
        """%(jml,session['userId'],dokter,isi,tl,hl)
        db.execute_query(query)

        return redirect('/private')

    else:
        query ="""
        select count(*)
        from pesan
        """
        jml = db.execute_query_one(query)
        jml = jml+1
        user = request.args.get('user')
        isi = request.form.get("chat")
        tl = datetime.today().strftime('%Y-%m-%d')
        hl = datetime.today().strftime('%H:%M')
        query = """
        insert into pesan values('%s','%s','%s','%s','%s','%s','')        
        """%(jml,session['userId'],user,isi,tl,hl)
        db.execute_query(query)

        return redirect('/private?userId='+user)

@bp_chat.route('/list_chat',methods=["POST","GET"])
def content_list_chat():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    query = """
    select distinct(pasId)
    from hub
    where dokId like '%s'
    """%(session['userId'])
    df = db.df_query(query)
    if len(df) == 0:
        return render_template('content_dokter_user_chat.html')
    else:
        users=[]
        list_user = df.values.tolist()
        a = 0
        for i in list_user:
            query="""
            select *
            from users
            where userId like '%s'
            """%(i[0])
            df = db.df_query(query)
            df = df.iloc[0]
            df = df.values.tolist()
            users.append(df)
        
        return render_template('content_dokter_user_chat.html',pasien=users)