from flask import Blueprint, render_template, redirect, url_for, send_file,session, abort, redirect, request
import requests
import json
import database as db
import pandas as pd
from flask_paginate import Pagination, get_page_parameter

PER_PAGES = 5
bp_profile = Blueprint("bp_profile",__name__)

@bp_profile.route("/user-profile",methods=["POST","GET"])
def user_profile():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    userId = session['userId']
    query = '''
    
    select *
    from users
    where userId like '%s'
    
    '''%(str(userId))
    user = db.df_query(query)
    parsed = user.to_json(orient="records")
    user_json = json.loads(parsed)
    
    return render_template('content_user_profile.html',user = user_json[0])

@bp_profile.route('/update-users', methods=['POST',"GET"])
def update_users():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')
    hasil = request.form.to_dict(flat=False)
    
    string = ""
    for i in hasil.items():
        if len(i[1][0]) > 0 :
            qry = str(i[0])+" = '%s',"%(i[1][0])
            string = string+qry

    userId = session['userId']
    query = """
    UPDATE users
    SET %s
    WHERE userId = '%s'
    """%(string[:-1],userId)
    db.execute_query(query)
    return redirect("/user-profile")


@bp_profile.route('/list_user', methods=['POST',"GET"])
def list_users():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    query = '''
    select *
    from users
    where role like 'user'
    '''
    all_user = db.df_query(query)
    list_user = all_user.values.tolist()
    return render_template('content_admin_list_user.html',list_user=list_user)


@bp_profile.route('/delete_list_user', methods=['POST',"GET"])
def delete_list_users():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')
    userId = request.args.get("userId")
    query = """
    delete from users
    where userId like '%s'
    """%(userId)
    db.execute_query(query)

    return redirect("/list_user")

#################################################################################penyakit

@bp_profile.route('/list_penyakit', methods=['POST',"GET"])
def list_penyakit():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    search = False
    q = request.args.get('q')
    if q:
        search = True

    page = request.args.get(get_page_parameter(), type=int, default=1)

    query = '''
    select *
    from penyakit
    '''
    all_penyakit = db.df_query(query)
    list_penyakit = all_penyakit.values.tolist()

    i=(page-1)*PER_PAGES
    penyakit_page = list_penyakit[i:i+5]
    pagination = Pagination(page=page,per_page=PER_PAGES, total=len(list_penyakit), search=search, record_name='List')

    return render_template('content_admin_list_penyakit.html',penyakit = penyakit_page, pagination=pagination,css_framework='bootstrap4')

@bp_profile.route('/delete_penyakit', methods=['POST',"GET"])
def delete_penyakit():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')
    penyakitId = request.args.get("penyakitId")
    query = """
    delete from penyakit
    where penyakitId like '%s'
    """%(penyakitId)
    db.execute_query(query)
    query = """
    delete from relasi 
    where penyakitId like '%s'
    """%(penyakitId)
    db.execute_query(query)

    return redirect("/list_penyakit")

@bp_profile.route('/page_add_penyakit', methods=['POST',"GET"])
def page_add_penyakit():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    query = '''
    select *
    from gejala
    '''
    all_gejala = db.df_query(query)
    list_gejala = all_gejala.values.tolist()

    return render_template('content_admin_add_penyakit.html',gejala=list_gejala)

@bp_profile.route('/add_penyakit', methods=['POST',"GET"])
def add_penyakit():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    data = request.form.getlist('gejalabox')
    name = request.form.get("name")
    keterangan = request.form.get("keterangan")
    level = request.form.get("level")
    query="""
    select count(*)
    from penyakit
    """
    id = db.execute_query_one(query)
    id = id+1
    id = 'R'+str(id)
    query="""
    insert into penyakit values('%s','%s','%s','%s','')
    """%(id,name,keterangan,level)
    db.execute_query(query)
    for i in data:
        query = """
        insert into relasi values ('%s','%s')
        """%(id,i)
        db.execute_query(query)

    return redirect('/list_penyakit')


#################################################################################gejala

@bp_profile.route('/list_gejala', methods=['POST',"GET"])
def list_gejala():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    query = '''
    select *
    from gejala
    '''
    all_gejala = db.df_query(query)
    list_gejala = all_gejala.values.tolist()
    i=(page-1)*PER_PAGES
    gejala_page = list_gejala[i:i+5]
    pagination = Pagination(page=page,per_page=PER_PAGES, total=len(list_gejala), record_name='List')

    return render_template('content_admin_list_gejala.html',gejala = gejala_page,pagination = pagination)

@bp_profile.route('/delete_gejala', methods=['POST',"GET"])
def delete_gejala():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    gejalaId = request.args.get("gejalaId")
    query = """
    delete from gejala
    where gejalaId like '%s'
    """%(gejalaId)
    db.execute_query(query)
    query = """
    delete from relasi
    where gejalaId like '%s'
    """%(gejalaId)
    db.execute_query(query)
    return redirect("/list_gejala")

@bp_profile.route('/page_add_gejala', methods=['POST',"GET"])
def page_add_gejala():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    return render_template('content_admin_add_gejala.html')


@bp_profile.route('/add_gejala', methods=['POST',"GET"])
def add_gejala():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')
    name = request.form.get("name")
    pertanyaan = request.form.get("pertanyaan")
    query="""
    select count(*)
    from gejala
    """
    id = db.execute_query_one(query)
    id = id+1
    id = 'G'+str(id)
    query="""
    insert into gejala values ('%s','%s','%s')
    """%(str(id),str(name),str(pertanyaan))
    db.execute_query(query)

    return redirect('/list_gejala')

#######################################################drug

@bp_profile.route('/list_drug', methods=['POST',"GET"])
def list_drug():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    page = request.args.get(get_page_parameter(), type=int, default=1)
    query = '''
    select *
    from obat
    '''
    all_obat = db.df_query(query)
    list_obat = all_obat.values.tolist()
    i=(page-1)*PER_PAGES
    obat_page = list_obat[i:i+5]
    pagination = Pagination(page=page,per_page=PER_PAGES, total=len(list_obat), record_name='List')

    return render_template('content_admin_list_drug.html',obat = obat_page,pagination = pagination)
 
@bp_profile.route('/delete_obat', methods=['POST',"GET"])
def delete_obat():

    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    obatId = request.args.get("obatId")
    query = """
    delete from obat
    where obatId like '%s'
    """%(obatId)
    db.execute_query(query)

    return redirect('/list_drug')

@bp_profile.route('/page_add_obat', methods=['POST',"GET"])
def page_add_obat():
    if "google_login" not in session:
        restricted_message = ""
        return render_template('login.html')

    query="""
    
    select penyakitId,name
    from penyakit
    
    
    """
    df = db.df_query(query)
    df = df.values.tolist()

    return render_template('content_admin_add_obat.html',penyakit=df)

@bp_profile.route('/add_obat', methods=['POST',"GET"])
def add_obat():

    name = request.form.get("name")
    pertanyaan = request.form.get("pertanyaan")
    penyakit = request.form.get("penyakit")

    query="""
    select count(*)
    from obat
    """
    id = db.execute_query_one(query)
    id = id+1
    id = 'B'+str(id)
    
    query ="""
    insert into obat values ("%s","%s","%s","%s")
    """%(id,penyakit,name,pertanyaan)

    db.execute_query(query)

    return redirect('/list_drug')

# for i in hasil.items():
#     if len(i[1][0]) > 0 :
#         if i[1][0].isnumeric():
#             qry = str(i[0])+" = %s,"%(i[1][0])
#         else:
#             qry = str(i[0])+" = '%s',"%(i[1][0])
#         print(qry)
#         string = string+qry
