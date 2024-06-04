from flask import *
from dotenv import load_dotenv
import os
import psycopg2
import datetime
import validators
from urllib.parse import urlparse, urlunparse

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('PR_83_SECRET_KEY')
DB_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()


@app.route('/')
def main():
    msg = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=msg)


@app.post('/urls')
def urls():
    url = request.form.get('url', '')
    errors = validate_url(url)
    if errors:
        flash(errors[0], 'alert-danger')
        return redirect(url_for('main'))
    o = urlparse(url)
    normalized_url = str(urlunparse([o.scheme, o.hostname, '', '', '', '']))
    page_id = get_id(normalized_url)
    if page_id:
        flash('Страница уже существует', 'alert-info')
        return redirect(url_for('url_id', id=page_id))
    today = datetime.datetime.now().date()
    page_id = add_to_db(normalized_url, today)
    flash('Страница успешно добавлена'+ normalized_url, 'alert-success')
    return redirect(url_for('url_id', id=page_id))


@app.get('/urls')
def urls_get():
    msg = get_flashed_messages(with_categories=True)
    return render_template('all.html', messages=msg) 


@app.get('/urls/<int:id>')
def url_id(id):
    msg = get_flashed_messages(with_categories=True)
    return render_template('edit_page.html', messages=msg) 


def validate_url(data):
    errors = []
    if not data:
        errors.append('Поле не должно быть пустым!')
    if len(data) > 255:
        errors.append('URL превышает 255 символов')
    if not validators.url(data):
        errors.append('Некорректный URL')
    return errors


def get_id(data):
    cur.execute("SELECT * FROM urls WHERE name=%s;", (data,))
    if cur.rowcount > 0:  # .fetchone() is not None:
        return cur.fetchone()[0]
    return None


def add_to_db(url, created_at):
    cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s);", (url, created_at))
    conn.commit()
    return get_id(url)

# validators = "^0.20.0"
# requests = "^2.31.0"
#https://23422222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222.kk22222.com