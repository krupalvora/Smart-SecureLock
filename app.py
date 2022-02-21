from flask import Flask, render_template, request, redirect, url_for, flash
import kv_mail
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
app = Flask(__name__)
s=URLSafeTimedSerializer('Thisisasecret!')

@app.route('/')
def home():
    return 'Home page'


@app.route('/rfid/<rfid>')
def rfid(rfid):
    # generate url mail to specific user
    hash = 'adahgl09-9dgdfg-dbd-fg9-34'  # demo hash
    token=s.dumps(rfid, salt='rfid')
    body = 'click here to login: ' + url_for('verified_rfid', token=token, _external=True)
    user_email = 'krupal.vora@sakec.ac.in'
    kv_mail.mail('mg9417054@gmail.com', 'eHi3mohwier', user_email, "Verify your password", body)
    return 'Hello world!'


@app.route('/verified_rfid/<token>')
def verified_rfid(token):
    try:
        rfid=s.loads(token, salt='rfid', max_age=100)
    except SignatureExpired:
        return '<h1>session expired</h1>'
    # open unique url and ask for inputs
    return render_template('index.html',rfid=rfid)


@app.route('/verify', methods=('GET', 'POST'))
def verify():
    if request.method == 'POST':
        pswd = request.form["pswd"]
        rfid = request.form["rfid"]
        # check username and password
        return 'door opened'
    else:
        return 'invalid url'


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
