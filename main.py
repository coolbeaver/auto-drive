# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session, abort
import sqlite3
import hashlib
import os
import datetime
from random import getrandbits, randint
from werkzeug.utils import secure_filename

from config import user_db
from defs.sct_key import s_key
from defs.database import *
from defs.calculate import *
from defs.auth import only_auth_user
from defs.images import *
from defs.parse_news import *

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)

s_key(app)

con = sqlite3.connect(user_db, check_same_thread=False)
cur = con.cursor()


@app.route('/', methods=['GET', 'POST'])
@app.route('/news', methods=['GET', 'POST'])
def news():
    news_list = pars_news()
    try:
        logged_in = session['logged_in']
        id = session['id']
        picture = session['picture']
        return render_template('news.html', id=id, logged_in=logged_in, news=news_list, picture=picture)
    except KeyError:
        return render_template('news.html', id=None, logged_in=False, news=news_list)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    try:
        logged_in = session['logged_in']
        id = session['id']
        picture = session['picture']
        token = session['token']
        if token == '44a8c14151b3cad58278fb2b706831f7853f971d847979b6dfb3119721c9401d':
            return render_template('admin.html', id=id, logged_in=logged_in, picture=picture)
        else:
            abort(401)
    except KeyError:
        abort(401)


@app.route('/users', methods=['GET', 'POST'])
def users():
    allUsers = select_all_users(cur)
    try:
        logged_in = session['logged_in']
        id = session['id']
        picture = session['picture']
        return render_template('users.html', id=id, logged_in=logged_in, picture=picture, allUsers=allUsers)
    except KeyError:
        return render_template('users.html', logged_in=False, allUsers=allUsers)


@app.route('/user/<int:id>/', methods=['GET', 'POST'])
def index(id):
    try:
        result_token = only_auth_user(cur, session['token'])
        idUser = session['id']
        logged_in = session['logged_in']
        picture = session['picture']
        if result_token is True:
            news_list = pars_news()
            posts = check_posts(cur, id)
            print(posts)
            info_user = check_info(cur, id)
            if request.method == 'POST':
                text = request.form['text_post']
                file = request.files['file']
                filename = save_image(file, app, secure_filename, os, randint, 'static/images/userspic/')
                current_date = datetime.datetime.now()
                current_date_string = current_date.strftime('%m/%d/%y %H:%M:%S')
                data = (idUser, current_date_string, text, filename,)
                create_post(cur, con, data)
                return redirect(url_for('index', id=id))
            try:
                return render_template('index.html', posts=posts, idUser=idUser, id=id, logged_in=logged_in,
                                       picture=picture, news=news_list, picture_user=info_user['picture'],
                                       username=info_user['username'], about=info_user['about'], car=info_user['car'])
            except:
                return redirect(url_for('news'))
        else:
            return redirect(url_for('login'))
    except KeyError:
        news = pars_news()
        posts = check_posts(cur, id)
        print(posts)
        info_user = check_info(cur, id)
        idUser = 993912391293129391912
        return render_template('index.html', posts=posts, idUser=idUser, id=id, logged_in=False,
                               picture=None, news=news, picture_user=info_user['picture'],
                               username=info_user['username'], about=info_user['about'],
                               car=info_user['car'])


@app.route('/logout')
def logout():
    session.pop('mail', None)
    session.pop('logged_in', None)
    session.pop('password', None)
    session.pop('token', None)
    session.pop('id', None)
    session.pop('picture', None)
    print('Logout successfully!')
    return redirect(url_for('news'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = True
    if request.method == 'POST':
        session['mail'] = request.form['mail']
        session['password'] = request.form['password']
        data = (session['mail'], session['password'],)
        result_sign = sign_db(cur, data)
        if result_sign is False:
            return render_template('login.html', result="improperly")
        elif result_sign['block'] == "True":
            return render_template('login.html', result="block")
        elif str(result_sign['id']).isdigit() is True:
            session['token'] = result_sign['token']
            session['id'] = result_sign['id']
            session['picture'] = result_sign['picture']
            session['logged_in'] = True
            session.modified = True
            print(session)
            if str(result_sign['token']) == '44a8c14151b3cad58278fb2b706831f7853f971d847979b6dfb3119721c9401d':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('index', id=result_sign['id']))

    return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        username = request.form['username']
        print(username)
        token = hashlib.sha256(str(getrandbits(256)).encode('utf-8') + str(password).encode('utf-8')).hexdigest()
        data = (username, mail, password, token)
        result_reg = reg_db(cur, con, data)
        if result_reg is True:
            return redirect(url_for('login'))
        elif result_reg == 'Rep_Name':
            return render_template('reg.html', result="rep_name")
        elif result_reg == 'Rep_Mail':
            return render_template('reg.html', result="rep_mail")

    return render_template('reg.html')


@app.route('/calculations', methods=['GET', 'POST'])
def calculations():
    try:
        print(session)
        logged_in = session['logged_in']
        picture = session['picture']
        id = session['id']
    except KeyError:
        logged_in = False
        id = None
        picture = None
    credit_result = 0
    checked = False
    if request.method == 'POST':
        checked = True
        ls = int(request.form['ls'])
        price_ts = int(request.form['price_ts'])
        credit = int(request.form['credit'])
        time_credit = request.form['time_credit']
        percent_credit = request.form['percent_credit']
        avg_cons = int(request.form['avg_cons'])
        price_benz = int(request.form['price_benz'])
        reg_go = int(request.form['reg_go'])
        col_reg = int(request.form['col_reg'])
        noreg_go = int(request.form['noreg_go'])
        col_noreg = int(request.form['col_noreg'])
        strah = request.form['strah']
        current_date = datetime.datetime.now()
        current_date_string = current_date.strftime('%m/%d/%y %H:%M:%S')
        data = (ls, current_date_string, price_ts, credit, time_credit, percent_credit, avg_cons,
                price_benz, reg_go, col_reg, noreg_go, col_noreg, strah,)
        if credit != 0:
            credit_result = calc_credit(credit, int(percent_credit), int(time_credit))
        if strah == 'osago':
            strah_result = calc_osago(ls)
        elif strah == 'casko':
            strah_result = 71000
        oil_result = calc_oil(avg_cons, price_benz, reg_go, col_reg, noreg_go, col_noreg)
        nalog_result = calc_nalog(ls)
        itog = (12 * credit_result) + strah_result + (12 * oil_result) + nalog_result + 5000 + 7200
        print(itog)
        create_result(cur, con, data)
        return render_template('calculations.html', credit=credit_result, strah=strah_result, oil=oil_result,
                               nalog=nalog_result, itog=itog, checked=checked, picture=picture)
    return render_template('calculations.html', credit=credit_result, checked=checked, logged_in=logged_in,
                           id=id, picture=picture)


@app.route('/admin/<action>/', methods=['GET', 'POST'])
def admin_menu(action):
    try:
        logged_in = session['logged_in']
        id = session['id']
        picture = session['picture']
        token = session['token']
        if token == '44a8c14151b3cad58278fb2b706831f7853f971d847979b6dfb3119721c9401d':
            if request.method == 'POST':
                try:
                    idBlock = request.form['block_id']
                except:
                    idBlock = ''
                try:
                    deletePost = request.form['delete_post']
                except:
                    deletePost = ''
                if idBlock:
                    result_block = check_block(cur, idBlock)
                    if "True" in result_block:
                        update_user(cur, con, 'block', "False", idBlock)
                    elif "False" in result_block:
                        update_user(cur, con, 'block', "True", idBlock)
                    return redirect(url_for('admin_menu', action='users'))
                elif deletePost:
                    delete_post(cur, con, deletePost)
                    return redirect(url_for('admin_menu', action='posts'))

            allUsers = select_all_users(cur)
            data_calc = select_all_calc(cur)
            allPosts = select_all_posts(cur)
            return render_template('admin.html', id=id, logged_in=logged_in, picture=picture,
                                   action=action, allUsers=allUsers, data_calc=data_calc, allPosts=allPosts)
        else:
            abort(401)
    except KeyError:
        abort(401)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    try:
        logged_in = session['logged_in']
        id = session['id']
        picture = session['picture']
        if request.method == 'POST':
            file = request.files['file']
            username_change = request.form['text_post']
            about = request.form['text_about']
            car = request.form['text_car']
            if str(file.filename):
                filename = save_image(file, app, secure_filename, os, randint, 'static/images/userspic/')
                update_user(cur, con, 'picture', filename, id)
                session['picture'] = filename
            if username_change:
                update_user(cur, con, 'username', username_change, id)
            if about:
                update_user(cur, con, 'about', about, id)
            if car:
                update_user(cur, con, 'car', car, id)
            return redirect(url_for('profile', id=id))
        else:
            return render_template('profile.html', id=id, logged_in=logged_in, picture=picture)
    except KeyError:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(port=5005)
