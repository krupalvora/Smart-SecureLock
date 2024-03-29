from flask import Flask, render_template, request, url_for, jsonify
import kv_mail
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_config import CONFIG

load_dotenv()

app = Flask(__name__)
TOKEN = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
cred = credentials.Certificate(CONFIG)
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/rfid/<rfid>')
def rfid(rfid):
    try:
        doc_ref = db.collection(u'users').document(rfid)
        doc = doc_ref.get()
        if doc.exists:
            user_email = doc.to_dict()[u'email']
            token = TOKEN.dumps(rfid, salt='rfid')
            doc_ref = db.collection(u'users').document(rfid)
            doc = doc_ref.get()
            blocked = doc.to_dict()[u'blocked']
            if blocked:
                body = 'Alert some one is using your blocked card'
                kv_mail.mail(
                    os.getenv('EMAIL'),
                    os.getenv('PASSWORD'),
                    user_email,
                    "Alert ",
                    body,
                )
                res = {'result': -1, 'message': 'Card has been blocked'}
                return jsonify(res)
            else:
                body = (
                    'click here to login: '
                    + url_for('verified_rfid', token=token, _external=True)
                    + '\n \n \nTo block this card click here: '
                    + url_for('block', token=token, _external=True)
                )
            kv_mail.mail(
                os.getenv('EMAIL'),
                os.getenv('PASSWORD'),
                user_email,
                "Verify your password",
                body,
            )
            res = {'result': 1, 'message': 'Email sent to : ' + user_email}
            return jsonify(res)
        else:
            res = {'result': 0, 'message': 'User not found'}
            return jsonify(res)
    except Exception as e:
        # print(e)
        return "Error"


@app.route('/verified_rfid/<token>')
def verified_rfid(token):
    try:
        rfid = TOKEN.loads(token, salt='rfid', max_age=100)
    except SignatureExpired:
        res = {'result': 0}
        return jsonify(res)
    return render_template('unlock.html', rfid=rfid)


@app.route('/block/<token>')
def block(token):
    try:
        rfid = TOKEN.loads(token, salt='rfid', max_age=500)
        doc_ref = db.collection(u'users').document(rfid)
        doc = doc_ref.get()
        username = doc.to_dict()[u'username']
        doc_ref.update({u'blocked': True})
        res = {'result': -1, 'message': 'User ' + username + ' has been blocked'}
        return jsonify(res)
    except SignatureExpired:
        res = {'result': 0, 'message': 'block link expired'}
        return jsonify(res)
    

@app.route('/verify', methods=('GET', 'POST'))
def verify():
    if request.method == 'POST':
        pswd = request.form["pswd"]
        rfid = request.form["rfid"]
        doc_ref = db.collection(u'users').document(rfid)
        doc = doc_ref.get()
        blocked =  doc.to_dict()[u'blocked']
        if blocked is True:
            res = {'result': -1, 'message': 'User is blocked'}
            return jsonify(res)
        if doc.exists:
            password = doc.to_dict()[u'password']
        if pswd == password:
            res = {'result': 1, 'message': 'User verified'}
            doc_ref.update({u'status': True})
            return jsonify(res)
        else:
            res = {'result': 0, 'message': 'Wrong password'}
            return jsonify(res)
    elif request.method == 'GET':
        pswd = request.args.get('pswd')
        rfid = request.args.get('rfid')
        doc_ref = db.collection(u'users').document(rfid)
        doc = doc_ref.get()
        blocked =  doc.to_dict()[u'blocked']
        if blocked is True:
            res = {'result': -1, 'message': 'User is blocked'}
            return jsonify(res)
        if doc.exists:
            password = doc.to_dict()[u'password']
        if pswd == password:
            res = {'result': 1, 'message': 'User verified'}
            return jsonify(res)
        else:
            res = {'result': 0, 'message': 'Wrong password'}
            return jsonify(res)

@app.route('/open/<rfid>')
def open(rfid):
    doc_ref = db.collection(u'users').document(rfid)
    doc = doc_ref.get()
    if doc.exists:
        status = doc.to_dict()[u'status']
        if status is True:
            doc_ref.update({u'status': False})
            res = {'result': 1, 'message': 'User verified'}
            return jsonify(res)
        else:
            res = {'result': 0, 'message': 'Please dont make direct calls to this url'}
            return jsonify(res)
    else:
        res = {'result': 0, 'message': 'User not found attempt to login directly'}
        return jsonify(res)   
if __name__ == '__main__':
    app.run("0.0.0.0", debug=False)
