from flask import Flask, render_template, request, session, redirect, url_for, flash
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

    def __init__(self, name, count, date_posted, shipment):
        self.name = name
        self.count = count
        self.date = date_posted
        self.shipment = shipment

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        item = request.form['name']
        count = request.form['count']
        date = datetime.now()
        shipment = "Not Assigned"
        session['item'] = item
    
        #add item to DB and view
        flash('Item Added Successfully')
        item = Inventory(item, count, date, shipment)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('view'))
        
    return render_template("add.html")

@app.route('/edit-entry/<name>', methods=["GET", "POST"])
def edit_entry(name):
    entry = Inventory.query.filter_by(name=name).first()
    if request.method == 'POST':
        entry.name = request.form['rename']
        entry.count = request.form['recount']
        entry.date_posted = datetime.now()
        flash("Item Updated")
        db.session.commit()
        return redirect(url_for("view"))

    else:
        return render_template('edit.html')


@app.route("/delete-entry/<name>")
def delete_entry(name):
    entry = Inventory.query.filter_by(name=name).first()

    db.session.delete(entry)
    db.session.commit()

    flash("Item Deleted")
    return redirect(url_for('view'))

@app.route('/shipment/<int:_id>', methods=["GET", "POST"])
def add_to_shipment(_id):

    item = Inventory.query.filter_by(_id=_id).first()
    
    if request.method == "POST":
        current_count = item.count
        send_items = int(request.form['total_add'])
        name_of_shipment = request.form['shipment_title']

        if current_count > send_items:
            flash("Inventory Added to Shipment")
            item.count = (current_count-send_items)
            shipment_item = Inventory(item.name, send_items, datetime.now(), name_of_shipment)
            db.session.add(shipment_item)
            db.session.commit()
            return redirect(url_for('view'))

        elif current_count < send_items:
            flash('Not enough inventory. Please send only what is currently in inventory')
            return redirect(url_for('view'))

        else:
            flash('All inventory added to shipment.')
            db.session.delete(item)
            shipment_item = Inventory(item.name, send_items, datetime.now(), name_of_shipment)
            db.session.add(shipment_item)
            db.session.commit()
            return redirect(url_for('view'))

    return render_template('create_shipments.html', items=[item.name, item.count])

@app.route('/view_shipments/<shipment>')
def select_shipment(shipment):
    shipments = Inventory.query.filter_by(shipment=shipment).all()
    return render_template("view_shipments.html", shipments = Inventory.query.filter_by(shipment=shipment).all())

@app.route('/view')
def view():
    return render_template("view.html", values=Inventory.query.all())

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)