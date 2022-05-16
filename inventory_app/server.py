from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Inventory(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000), nullable=False)
    count = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime, default=datetime.now())
    shipment = db.Column(db.String(1000))

    def __init__(self, name, count, date_posted, shipment="Not Assigned"):
        self.name = name
        self.count = count
        self.date = date_posted
        self.shipment = shipment
        
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)