import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, json
from waitress import serve
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parent.parent))
load_dotenv()
from shared import DB_PATH, DB_AUTH_PATH, IS_SETUPED_PATH

app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY')
admin_to_all = os.getenv('ADMIN_ACCESS_TO_ALL')

def init_auth_db():
    conn = sqlite3.connect(DB_AUTH_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_auth_db()


def get_user(username):
    conn = sqlite3.connect(DB_AUTH_PATH)
    cur = conn.cursor()
    row = cur.execute('SELECT id, username, password, is_admin FROM users WHERE username=?', (username,)).fetchone()
    conn.close()
    return row


def is_first_setup():
    return not IS_SETUPED_PATH.exists()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = bool(user[3])
            return redirect(url_for('index'))
        flash('wrong login or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if not is_first_setup():
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = generate_password_hash(password)
        conn = sqlite3.connect(DB_AUTH_PATH)
        conn.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, 1)', (username, hashed))
        conn.commit()
        conn.close()
        IS_SETUPED_PATH.touch()
        flash('admin is created, you can enter')
        return redirect(url_for('login'))

    return render_template('setup.html')


from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if admin_to_all == "1":
            return f(*args, **kwargs)
        if is_first_setup():
            return redirect(url_for('setup'))
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if admin_to_all == "1":
            return f(*args, **kwargs)
        if not session.get('is_admin'):
            return 'unauthorized', 403
        return f(*args, **kwargs)
    return decorated


@app.route('/')
@login_required
def index():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    counts = {r[0]: r[1] for r in cur.execute('SELECT type, COUNT(*) FROM telemetry GROUP BY type')}
    rows = cur.execute('SELECT id, timestamp, type, device_id, data FROM telemetry ORDER BY timestamp DESC LIMIT 100').fetchall()
    conn.close()

    items = []
    for r in rows:
        try:
            data = json.loads(r[4])
        except:
            data = {}
        items.append({
            'id': r[0], 'timestamp': r[1], 'type': r[2], 'device_id': r[3], 'data': data
        })

    return render_template('index.html', counts=counts, items=items, is_admin=session.get('is_admin'))


@app.route('/inspect/<int:item_id>')
@login_required
def inspect_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute('SELECT id, timestamp, type, device_id, data FROM telemetry WHERE id=?', (item_id,)).fetchone()
    conn.close()
    if not row:
        return 'not found', 404
    try:
        data = json.loads(row[4])
    except:
        data = {}
    return render_template('inspect.html', item={'id': row[0], 'timestamp': row[1], 'type': row[2], 'device_id': row[3], 'data': data})


@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    conn = sqlite3.connect(DB_AUTH_PATH)
    users = conn.execute('SELECT id, username, is_admin FROM users').fetchall()
    conn.close()
    return render_template('admin.html', users=users)


@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = 1 if request.form.get('is_admin') else 0
        hashed = generate_password_hash(password)
        conn = sqlite3.connect(DB_AUTH_PATH)
        try:
            conn.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)', (username, hashed, is_admin))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('user already existing')
        conn.close()
        return redirect(url_for('admin_panel'))
    return render_template('add_user.html')


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=7635)
