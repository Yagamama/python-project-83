from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = os.getenv('PR_83_SECRET_KEY')


@app.route('/')
def main():
    return 'Flask app'
