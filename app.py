import email
from flask import Flask, render_template, request, redirect, url_for, jsonify
import kv_mail
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
app = Flask(__name__)
s=URLSafeTimedSerializer('Thisisasecret!')

@app.route('/')
def home():
    return 'Home page'


@app.route('/rfid/<rfid>')
def rfid(rfid):
    res={'result':1}
    token=s.dumps(rfid, salt='rfid')
    body = 'click here to login: ' + url_for('verified_rfid', token=token, _external=True)
    user_email = 'krupal.vora@sakec.ac.in'
    kv_mail.mail('mg9417054@gmail.com', 'eHi3mohwier', user_email, "Verify your password", body)
    return jsonify(res)


@app.route('/verified_rfid/<token>')
def verified_rfid(token):
    try:
        rfid=s.loads(token, salt='rfid', max_age=100)
    except SignatureExpired:
        res={'result':0}
        return jsonify(res)
    return render_template('index.html',rfid=rfid)


@app.route('/verify', methods=('GET', 'POST'))
def verify():
    if request.method == 'POST':
        pswd = request.form["pswd"]
        rfid = request.form["rfid"]
        # check username and password
        rfid='rfid'
        pswd='pswd'
        if rfid == 'rfid' and pswd == 'pswd':
            res={'result':1}
            return jsonify(res)
        else:
            res={'result':0}
            return jsonify(res)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
