import re

from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=''

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            mydb = pymysql.connect(
                host="centerbeam.proxy.rlwy.net",
                port=46007,
                user="root",
                password="bKKQyuceYkJyDZOqHHDTyAbJBrAprcZE",
                database="railway",
                ssl={"ssl": {}}
            )

        except Exception as e:
            return f"Database connection failed: {str(e)}"

        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT * FROM userdata WHERE username = %s AND password = %s",
            (username, password)
        )

        account = mycursor.fetchone()

        if account:
            print('Login Successful')
            name = account[0]
            msg = 'Login Successful'
            return render_template('welcome.html', name=name, msg=msg)
        else:
            msg = 'Incorrect Credentials / Kindly Check'
            return render_template('login.html', msg=msg)

    return render_template('login.html')

@app.route('/logout')
def logout():
    name = ''
    id = ''
    msg = "Logged Out Successfully"
    return render_template('login.html', msg=msg, name=name, id=id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ""
    if request.method == "POST" and "username" in request.form and "password" in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        mydb = pymysql.connect(
            host="centerbeam.proxy.rlwy.net",
            port=46007,
            user="root",
            password="bKKQyuceYkJyDZOqHHDTyAbJBrAprcZE",
            database="railway",
            ssl={"ssl": {}}
        )

        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT * FROM userdata WHERE username=%s AND email=%s",
            (username, email)
        )

        account = mycursor.fetchone()

        if account:
            msg = "account already exists"

        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            msg = "invalid email address"

        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = "username must contain only characters and numbers"

        elif not username or not password or not email:
            msg = "kindly fill all the details"
        else:
            mycursor.execute(
                'INSERT INTO userdata VALUES (%s,%s,%s)', (username, password, email)
            )

            mydb.commit()

            msg = "ur registration is succesful"

            name = username

            return render_template("welcome.html", name=name, msg=msg)

        return render_template("register.html", msg=msg)

    return render_template("register.html")


@app.route('/')
def home():
    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)