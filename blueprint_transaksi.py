from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db
from datetime import datetime
from flask_paginate import Pagination, get_page_parameter

bp_transaksi = Blueprint('bp_transaksi', __name__)

@bp_transaksi.route('/transaction')
def doc_transaksi():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')


    return render_template('content_transaksi.html')

@bp_transaksi.route('/isi_wallet')
def isi_wallet():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')


    return render_template('isi_wallet.html')


@bp_transaksi.route('/add_money',methods=['POST','GET'])
def add_money():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    money = request.form.get('money')
    query ="""
    select amount_money
    from wallet
    where userId like '%s'
    """%(session['userId'])

    last_money = db.execute_query_one(query)
    plus_money = last_money + int(money)

    query = """    
    UPDATE wallet
    SET amount_money=%s
    WHERE userId like '%s'
    """%(int(plus_money),session['userId'])

    db.execute_query(query)

    query = '''
    select count(*)
    from transaksi
    '''
    tl = datetime.today().strftime('%Y%m%d')
    hasil = db.execute_query_one(query)
    hasil = hasil+1
    trid = 'tr'+str(tl)+str(hasil)

    tl = datetime.today().strftime('%Y-%m-%d')

    query='''
    insert into transaksi values('%s','%s','%s',%s)
    '''%(trid,session['userId'],tl,int(money))

    return redirect('/')



@bp_transaksi.route('/bayar_wallet',methods=['POST','GET'])
def bayar_wallet():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    money = request.args.get("money")
    money = int(money) - 30000
    query = """
    UPDATE wallet
    SET amount_money=%s
    WHERE userId like '%s'
    """%(int(money),session['userId'])
    db.execute_query(query)

    query = '''
    select count(*)
    from transaksi
    '''
    tl = datetime.today().strftime('%Y%m%d')
    hasil = db.execute_query_one(query)
    hasil = hasil+1
    trid = 'tr'+str(tl)+str(hasil)
    tl = datetime.today().strftime('%Y-%m-%d')
    query='''
    insert into transaksi values('%s','%s','%s',%s)
    '''%(trid,session['userId'],tl,30000)
    db.execute_query(query)

    query = '''

            select * 
            from hub
            where pasId like '%s'

    '''%(session['userId'])

    df = db.df_query(query)

    if len(df)==0:

        return redirect('/private')

    else :
        query = """
        UPDATE hub
        SET flag=1
        WHERE pasId like '%s'
        """%(session['userId'])

        db.execute_query(query)

        return redirect('/private')

