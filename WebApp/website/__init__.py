from flask import Flask
import sys
from os.path import dirname,abspath
d=dirname(dirname(abspath(__file__)))
sys.path.append(d)

def create_app():
    app= Flask(__name__)
    app.config['SECRET_KEY'] = 'kfjshflakjhflkj'
    return app

