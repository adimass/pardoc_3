from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db
from datetime import datetime
from flask_paginate import Pagination, get_page_parameter

bp_transaksi = Blueprint('bp_transaksi', __name__)

@bp_transaksi.route('/transaction')
def doc_transaksi():


    return render_template('content_transaksi.html')

@bp_transaksi.route('/isi_wallet')
def isi_wallet():


    return render_template('isi_wallet.html')


@bp_transaksi.route('/add_money',methods=['POST','GET'])
def add_money():

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

    return redirect('/')



@bp_transaksi.route('/bayar_wallet',methods=['POST','GET'])
def bayar_wallet():

    money = request.args.get("money")
    money = int(money) - 30000
    query = """
    
    UPDATE wallet
    SET amount_money=%s
    WHERE userId like '%s'
    """%(int(money),session['userId'])
    db.execute_query(query)

    return redirect('/private')