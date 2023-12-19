import os
from flask import Flask, render_template
from lib.user_repository import UserRepository
from lib.peep_repository import PeepRepository
from lib.database_connection import get_flask_database_connection

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET'])
def get_index():
    connection = get_flask_database_connection(app)
    user_repo = UserRepository(connection)
    peep_repo = PeepRepository(connection)
    users = user_repo.all()
    peeps = peep_repo.all()
    return render_template('index.html', users=users, peeps=peeps)

if __name__ == "__main__":
    #app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))