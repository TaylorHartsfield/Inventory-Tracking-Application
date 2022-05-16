from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)