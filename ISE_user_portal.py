from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from ciscoisesdk import IdentityServicesEngineAPI
from werkzeug.security import generate_password_hash, check_password_hash
import os

# admin_user = "gurkirat"
admin_user = ['gurkirat', 'sricharan', 'naba']

# print(__name__)
app = Flask(__name__)
app.secret_key = 'your_secret_key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'portal_users.db')}"
db = SQLAlchemy(app)

class PortalUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    ise_username = db.Column(db.String(80), nullable=False)

# To create the DB, run once in Python shell:
# from ISE_user_portal import app, db, PortalUser
# with app.app_context():
#     db.create_all()
#     user = PortalUser(username='gurkirat', password='password', ise_username='gurkirat')
#     db.session.add(user)
#     db.session.commit()

from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
BASE_URL = os.getenv('BASE_URL')

ISE_API = IdentityServicesEngineAPI(
    username=ADMIN_USER,
    password=ADMIN_PASSWORD,
    base_url=BASE_URL,
    version="3.3_patch_1",
    verify=False
)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = PortalUser.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid portal username or password.", 'danger')
            return redirect(url_for('login'))
        session['portal_username'] = user.username
        session['ise_username'] = user.ise_username
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'portal_username' not in session:
        return redirect(url_for('login'))
    ise_username = session['ise_username']
    resp = ISE_API.internal_user.get_all(filter=f"name.EQ.{ise_username}") # type: ignore
    users = resp.response.get('SearchResult', {}).get('resources', [])
    user_data = None
    if users:
        user_id = users[0]['id']
        user_details = ISE_API.internal_user.get_by_id(id=user_id) # type: ignore
        user_data = user_details.response['InternalUser']
        session['user_id'] = user_id
    return render_template('index.html', user=user_data, admin_user=admin_user)

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'portal_username' not in session:
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    new_password = request.form['new_password']
    if not new_password or not user_id:
        flash("Password cannot be empty.", 'danger')
        return redirect(url_for('index'))
    user_details = ISE_API.internal_user.get_by_id(id=user_id) # type: ignore
    user_data = user_details.response['InternalUser']
    user_data['password'] = new_password
    user_data['enabled'] = True
    user_data.pop('link', None)
    user_data.pop('dateModified', None)
    payload = {"InternalUser": user_data}
    update_resp = ISE_API.internal_user.update_by_id(id=user_id, payload=payload) # type: ignore
    if update_resp.status_code in [200, 204]:
        flash("Password changed successfully.", 'success')
    else:
        flash(f"Failed to change password. Response code: {update_resp.status_code}", 'danger')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Only allow if admin user is logged in
    if 'portal_username' not in session or session['portal_username'] not in admin_user:
        flash('Only admin users can register new users.', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ise_username = request.form['ise_username']
        if PortalUser.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password)
        user = PortalUser(username=username, password=hashed_pw, ise_username=ise_username)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        # return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/remove_user', methods=['GET', 'POST'])
def remove_user():
    if 'portal_username' not in session or session['portal_username'] not in admin_user:
        flash('Only admin users can remove users.', 'danger')
        return redirect(url_for('index'))
    users = PortalUser.query.filter(PortalUser.username != 'gurkirat').all()
    # users = PortalUser.query.filter().all()
    if request.method == 'POST':
        username = request.form['username']
        user = PortalUser.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash(f'User {username} removed successfully.', 'success')
            return redirect(url_for('remove_user'))
        else:
            flash('User not found.', 'danger')
    return render_template('remove_user.html', users=users)

if __name__ == '__main__':
    # app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)
