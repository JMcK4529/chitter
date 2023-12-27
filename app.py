import os, hashlib
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, session, request, redirect
from lib.user import User
from lib.user_repository import UserRepository
from lib.peep_repository import PeepRepository
from lib.database_connection import get_flask_database_connection
load_dotenv(override=True)

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = os.getenv('SESSION_KEY')

@app.route('/', methods=['GET'])
def get_index():
    connection = get_flask_database_connection(app)
    user_repo = UserRepository(connection)
    peep_repo = PeepRepository(connection)
    users = user_repo.all()
    peeps = peep_repo.all()
    if 'user_id' in session:
        return render_template(
            'index.html', 
            current_user=user_repo.find(session['user_id']).username, 
            users=users, 
            peeps=peeps
            )
    else:
        return render_template(
            'index_with_login_prompt.html', 
            users=users, 
            peeps=peeps
            )

@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.html', error=None)

def login_user(connection, username, password):
    """Logic for logging in a user"""
    user_repo = UserRepository(connection)
    try:
        if user_repo.check_password(username, password):
            try:
                user = user_repo.find_by_email(username)
                session['user_id'] = user.id
                return redirect(url_for('get_index'))
            except:
                try:
                    user = user_repo.find_by_username(username)
                    session['user_id'] = user.id
                    return redirect(url_for('get_index'))
                except:
                    return render_template(
                        'login.html', 
                        error="Something went wrong with your login.")
        else:
            raise Exception()
    except:
        return render_template(
            'login.html', 
            error="Username or password was incorrect.")

@app.route('/login', methods=['POST'])
def post_login():
    connection = get_flask_database_connection(app)
    username = request.form['Username or Email']
    password = request.form['Password']
    return login_user(connection, username, password)
    
    
@app.route("/logout", methods=['POST'])
def post_logout():
    if session['user_id']:
        del session['user_id']
        if 'user_id' not in session:
            return redirect(url_for('get_index'))
    else:
        return None
    
@app.route("/signup", methods=['GET'])
def get_signup():
    return render_template("signup.html", error=None)

@app.route("/signup", methods=['POST'])
def post_signup():
    connection = get_flask_database_connection(app)
    email = request.form['Email']
    username = request.form['Username']
    password = request.form['Password']
    verify_password = request.form['Verify']
    if password != verify_password:
        return render_template(
            'signup.html', 
            error="Passwords did not match.")
    elif password in ["", None,] \
        or (type(password) == str and password.strip() == "") \
            or len(password) < 8:
        return render_template(
            'signup.html', 
            error="Password must contain at least 8 characters.")
    hash_pass = hashlib.sha256(password.encode('utf-8')).hexdigest()
    new_user = User(None, username, email, hash_pass)
    if not new_user.is_valid():
        return render_template("signup.html",
                               error=new_user.generate_errors())
    user_repo = UserRepository(connection)
    current_users = user_repo.all()
    current_emails = [user.email for user in current_users]
    if email in current_emails:
        return render_template("signup.html",
                    error="Email address already has an associated account.")
    current_usernames = [user.username for user in current_users]
    if username in current_usernames:
        return render_template("signup.html",
                               error="Username is already in use.")
    
    user_repo.create(new_user)
    return login_user(connection, username, password)

if __name__ == "__main__":
    #app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5001))
        )