import os
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, session, request, redirect
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

@app.route('/login', methods=['POST'])
def post_login():
    connection = get_flask_database_connection(app)
    username = request.form['Username or Email']
    password = request.form['Password']
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

"""
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
    user_repo = UserRepository(connection)
""" 

if __name__ == "__main__":
    #app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
    app.run(
        debug=True, 
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5001))
        )