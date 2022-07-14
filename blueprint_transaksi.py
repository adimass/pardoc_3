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