from flask import Blueprint, render_template, request, redirect, session
from extensions import mysql, bcrypt

auth_bp = Blueprint('auth', __name__)

# REGISTER

# -------------------------
# -------------------------

# HOME

# -------------------------

@auth_bp.route('/')
def home():


    if 'user_id' in session:
        return redirect('/dashboard')

    return redirect('/login')


# -------------------------

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():


    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        # Check if email already exists
        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            return "Email already registered"

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cur.execute(
            """
            INSERT INTO users(name,email,password_hash)
            VALUES(%s,%s,%s)
            """,
            (name, email, hashed_password)
        )

        mysql.connection.commit()
        cur.close()

        return redirect('/login')

    return render_template('register.html')


# -------------------------

# LOGIN

# -------------------------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():


    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            """
            SELECT user_id,name,email,password_hash
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cur.fetchone()

        cur.close()

        if user:

            stored_hash = user[3]

            if bcrypt.check_password_hash(stored_hash, password):

                session['user_id'] = user[0]
                session['name'] = user[1]

                return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')


# LOGOUT

# -------------------------

@auth_bp.route('/logout')
def logout():

    session.clear()

    return redirect('/login')