from bcrypt import checkpw
from flask import Flask, abort, redirect, request, render_template, make_response
import random
import string

app = Flask(__name__)

tokens = set([])
passwords = {}
with open('.password') as f:
    for line in f.read().splitlines():
        u, p = line.split(' ')
        passwords[u] = p.encode('unicode-escape')

@app.route('/auth')
def auth():
    if (request.cookies.get('auth-token') in tokens):
        return "OK"
    else:
        return abort(401)

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if 'username' not in request.form or 'password' not in request.form:
        return abort(400)

    h = passwords.get(request.form["username"])
    p = request.form['password'].encode('unicode-escape')
    if h != None and checkpw(p, h):
        res = make_response(redirect('/'))
        token = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(24)])
        tokens.add(token)
        res.set_cookie('auth-token', token)
        return res
    else:
        return abort(403)

