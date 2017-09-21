from functools import wraps

from flask import Flask, render_template, session, redirect, url_for, request, send_from_directory
from db import db_session
from models import *
from json import dumps, loads
from random import randint
from datetime import datetime
from time import time

app = Flask(__name__)
app.secret_key = "sadfjlaksdfjkalsfjlkajfklajskl23jkl42kmsdlf"

app.config['is_blind'] = False
app.config['is_finish'] = False

'''
todo
5. admin
    - add chall with id
    - edit chall
    - delete chall
    - control start/end of the competetion
'''

def timestamp2str(timestamp):
    return datetime.fromtimestamp(
        int(timestamp)
    ).strftime('%Y-%m-%d %H:%M:%S')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'username' in session:
            return 'you need to login'
        return f(*args, **kwargs)
    return decorated_function


def calculate_hori_ver(arr, index):
    arr_len = len(arr)
    hori_ver_count = [0, 0]
    bingo_count = 0

    for i in range(arr_len):
        hori_ver_count[0] = hori_ver_count[0] + 1 if arr[index][i] else hori_ver_count[0]
        hori_ver_count[1] = hori_ver_count[1] + 1 if arr[i][index] else hori_ver_count[1]

    bingo_count = bingo_count + 1 if hori_ver_count[0] ==  arr_len else bingo_count
    bingo_count = bingo_count + 1 if hori_ver_count[1] == arr_len else bingo_count
    return bingo_count


def calculate_bingo(arr):
    # arr will be 5*5 with 25 index
    arr_len = len(arr)

    diagonal_count = [0, 0]
    bingo_count = 0

    for i in range(arr_len):
        diagonal_count[0] = diagonal_count[0] + 1 if arr[i][i] else diagonal_count[0]
        diagonal_count[1] = diagonal_count[1] + 1 if arr[i][arr_len-i-1] else diagonal_count[1]
        bingo_count += calculate_hori_ver(arr, i)

    bingo_count = bingo_count + 1 if diagonal_count[0] ==  arr_len else bingo_count
    bingo_count = bingo_count + 1 if diagonal_count[1] == arr_len else bingo_count


    return bingo_count


@app.route("/")
def main():
    login_msg = session['username'] if "username" in session else "Login"
    # get auth log

    kaist_bingo = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    postech_bingo = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    kaist_score, postech_score = 0, 0

    breakthrough = list(range(16))

    t_notices = Notice.query.order_by(Notice.n_time.desc()).all()
    notices = []
    for t_notice in t_notices:
        detail = "[{}] {}".format(timestamp2str(t_notice.n_time), t_notice.detail)
        notices.append(detail)

    t_auth_logs = AuthLog.query.filter(AuthLog.is_solve == True).order_by(AuthLog.submit_time.desc()).all()
    auth_logs = []
    for t_auth_log in t_auth_logs:
        score = Challenge.query.filter(Challenge.chall_id == t_auth_log.chall_id).first().chall_score
        # for checking breakthrough
        breakthrough[t_auth_log.chall_id] = t_auth_log.username
        if t_auth_log.username == 'postech':
            postech_bingo[int(t_auth_log.chall_id / 4)][t_auth_log.chall_id % 4] = 1
            postech_score += int(score)
        else:
            kaist_bingo[int(t_auth_log.chall_id / 4)][t_auth_log.chall_id % 4] = 1
            kaist_score += int(score)

        detail = "[{}] {} kills {}.".format(timestamp2str(t_auth_log.submit_time), t_auth_log.username, t_auth_log.chall_title)
        auth_logs.append(detail)

    kaist_bingo_count = calculate_bingo(kaist_bingo)
    postech_bingo_count = calculate_bingo(postech_bingo)

    # adding bingo bonus score
    kaist_score += 39 * kaist_bingo_count
    postech_score += 39 * postech_bingo_count

    # adding breakthrough score
    for i in range(len(breakthrough)):
        if breakthrough[i] == 'postech':
            postech_score += 1
        elif breakthrough[i] == 'kaist':
            kaist_score += 1

    is_blind_kaist, is_blind_postech = False, False

    if app.config['is_blind']:
        if not 'username' in session:
            kaist_score = 0
            kaist_bingo_count = 0
            postech_score = 0
            postech_bingo_count = 0
            auth_logs = ["[BLIND MODE]"]
        elif session['username'] == 'postech':
            kaist_score = 0
            kaist_bingo_count = 0
            is_blind_kaist = True
            auth_logs = ["[BLIND MODE]"]
        elif session['username'] == 'kaist':
            postech_score = 0
            postech_bingo_count = 0
            is_blind_postech = True
            auth_logs = ["[BLIND MODE]"]

    if 'username' in session:
        if session['username'] == 'admin':
            return render_template('scoreboard.html', kaist_bingo_count=kaist_bingo_count, postech_bingo_count=postech_bingo_count,
        kaist_score=kaist_score, postech_score=postech_score, is_login=login_msg, is_end=app.config['is_finish'], notices=notices, auth_logs=auth_logs,
        is_blind_kaist=is_blind_kaist, is_blind_postech=is_blind_postech)

    return render_template('index2.html', kaist_bingo_count=kaist_bingo_count, postech_bingo_count=postech_bingo_count,
        kaist_score=kaist_score, postech_score=postech_score, is_login=login_msg, is_end=app.config['is_finish'], notices=notices, auth_logs=auth_logs,
        is_blind_kaist=is_blind_kaist, is_blind_postech=is_blind_postech)


@app.route('/firstblood/<who>/<what>')
def firsblood(who, what):
    return render_template('firstblood.html', who=who, what=what)


@app.route("/end")
def end():
    if not app.config['is_finish']:
        return 'dododo'

    who_win = "POSTECH"
    return render_template('end.html', kaist_bingo_count=1, postech_bingo_count=3,
        kaist_score=1200, postech_score=2100, who_win=who_win)


# get chall
@app.route("/api/get_challs")
def get_challs():
    # todo : blind kaist auth
    challs, x = [], {}
    challenges = Challenge.query.all()

    for challenge in challenges:
        postech_auth = AuthLog.query.filter((AuthLog.is_solve == True) & (AuthLog.username == 'postech') & (AuthLog.chall_id == challenge.chall_id)).first()
        try:
            is_postech = postech_auth.is_solve
        except:
            is_postech = False

        kaist_auth = AuthLog.query.filter((AuthLog.is_solve == True) & (AuthLog.username == 'kaist') & (AuthLog.chall_id == challenge.chall_id)).first()
        try:
            is_kaist = kaist_auth.is_solve
        except:
            is_kaist = False

        if app.config['is_blind']:
            if not 'username' in session:
                is_kaist = False
                is_postech = False
            elif session['username'] == 'postech':
                is_kaist = False
            elif session['username'] == 'kaist':
                is_postech = False            

        challs.append({'chall_id': challenge.chall_id, 'chall_img': challenge.chall_img, 'chall_title': challenge.chall_title, 'chall_score': challenge.chall_score, 'is_kaist': is_kaist, 'is_postech': is_postech})

    x['status'] = 'true'
    x['challs'] = challs
    return dumps(x)


@app.route('/api/get_detail/<chall_id>')
@login_required
def get_detail(chall_id):
    challenge = Challenge.query.filter(Challenge.chall_id==int(chall_id)).first()
    try:
        x = {}
        x['status'] = True
        x['chall_id'] = challenge.chall_id
        x['chall_title'] = challenge.chall_title
        x['chall_detail'] = challenge.chall_detail
        x['chall_score'] = challenge.chall_score
    except:
        x = {}
        x['status'] = False
    return dumps(x)


@app.route("/api/auth", methods=['POST'])
@login_required
def auth():
    chall_id = int(request.form['chall_id'])
    if session['username'] == 'admin':
        x = {}
        x['msg'] = "Admin cannot solve the challenges."
        x['status'] = False
        return dumps(x)

    if AuthLog.query.filter((AuthLog.is_solve == True) & (AuthLog.username == session['username']) & (AuthLog.chall_id == chall_id)).first() is not None:
        x = {}
        x['msg'] = "You already solved !"
        x['status'] = False
        return dumps(x)

    challenge = Challenge.query.filter(Challenge.chall_id==int(chall_id)).first()

    x = {}
    try:
        if challenge.chall_flag == request.form['flag']:
            x['status'] = True
        else:
            x['status'] = False
            x['msg'] = "Wrong !"
    except:
        x['status'] = False
        x['msg'] = "Erorr !"
        return dumps(x)

    auth_log = AuthLog(chall_id, challenge.chall_title, 0, session['username'], request.form['flag'], x['status'])
    db_session.add(auth_log)
    db_session.commit()
    return dumps(x)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    u = User.query.filter(User.username == username).first()
    try:
        if u.password == request.form['password']:
            session['username'] = username
    except:
        pass

    return redirect(url_for('main'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main'))


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/goblind')
def go_blind():
    if session['username'] != 'admin':
        return 'no'

    if app.config['is_blind']:
        app.config['is_blind'] = False
    else:
        app.config['is_blind'] = True

    return 'd'


@app.route('/goend')
def go_end():
    if session['username'] != 'admin':
        return 'no'
        
    if app.config['is_finish']:
        app.config['is_finish'] = False
    else:
        app.config['is_finish'] = True

    return 'd'


@app.route('/api/get_firstblood')
def get_firstblood():
    x = {}
    x['status'] = False
    a = AuthLog.query.filter((AuthLog.submit_time + 20 > int(time())) & (AuthLog.is_solve == True)).all()
    try:
        if len(a) >= 2:
            return dumps(x)
        x['status'] = True
        x['data'] = {'who': a[0].username, 'what': a[0].chall_title}
    except:
        x['status'] = False
        pass
    return dumps(x)


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run()
