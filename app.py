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
TOKEN = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
cred = credentials.Certificate(CONFIG)
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route('/')
def home():
    return 'Home page'


@app.route('/rfid/<rfid>')
def rfid(rfid):
    try:
        doc_ref = db.collection(u'users').document(rfid)
        doc = doc_ref.get()
        if doc.exists:
            user_email = doc.to_dict()[u'email']
            token = TOKEN.dumps(rfid, salt='rfid')
            body = 'click here to login: ' + url_for('verified_rfid', token=token, _external=True)
            kv_mail.mail(
                os.environ.get('EMAIL'),
                os.environ.get('PASSWORD'),
                user_email,
                "Verify your password",
                body,
            )
            return "Email sent to " + user_email
        else:
            return "No such user exists"
    except Exception as e:
        print(e)
        return "Error"


@app.route('/verified_rfid/<token>')
def verified_rfid(token):
    try:
        rfid = TOKEN.loads(token, salt='rfid', max_age=100)
    except SignatureExpired:
        res = {'result': 0}
        return jsonify(res)
    return render_template('index.html', rfid=rfid)


@app.route('/verify', methods=('GET', 'POST'))
def verify():
    if request.method == 'POST':
        pswd = request.form["pswd"]
        rfid = request.form["rfid"]
        doc_ref = db.collection(u'users').document(rfid)
        doc = doc_ref.get()
        if doc.exists:
            password = doc.to_dict()[u'password']
        if pswd == password:
            res = {'result': 1}
            return jsonify(res)
        else:
            res = {'result': 0}
            return jsonify(res)


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
