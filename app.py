from flask import Flask, render_template, request, redirect, url_for, flash
import kv_mail

app = Flask(__name__)


@app.route('/')
def home():
    return 'Home page'


@app.route('/rfid/<rfid>')
def rfid(rfid):
    # generate url mail to specific user
    hash = 'adahgl09-9dgdfg-dbd-fg9-34'  # demo hash
    url = 'http://localhost:5000/verified_rfid/' + hash
    body = 'click here to login: ' + url
    user_email = 'krupal.vora@sakec.ac.in'
    kv_mail.mail('mg9417054@gmail.com', 'eHi3mohwier', user_email, "Verify your password", body)
    return 'Hello world!'


@app.route('/verified_rfid/<url>')
def verified_rfid(url):
    # open unique url and ask for inputs
    return render_template('index.html')


@app.route('/verify', methods=('GET', 'POST'))
def verify():
    if request.method == 'POST':
        pswd = request.form["pswd"]
        # check username and password
        return 'door opened'
    else:
        return 'invalid url'


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
