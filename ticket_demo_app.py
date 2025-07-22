from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Use /tmp for SQLite on Render
db_path = os.path.join("/tmp", "dummy_tickets.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Ticket(db.Model):
    pnr = db.Column(db.String(10), primary_key=True)
    passenger_name = db.Column(db.String(100))
    departure_date = db.Column(db.String(20))
    departure_time = db.Column(db.String(20))
    from_location = db.Column(db.String(100))
    to_location = db.Column(db.String(100))
    bus_operator = db.Column(db.String(100))
    seat_number = db.Column(db.String(10))
    price = db.Column(db.Float)
    status = db.Column(db.String(20), default="available")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Auto-create DB tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "<h2>✅ Dummy Ticket API is running!</h2><p>Use <code>/tickets</code> endpoints.</p>"

@app.route("/tickets", methods=["POST"])
def create_ticket():
    data = request.json
    ticket = Ticket(
        pnr=data["pnr"],
        passenger_name=data["passenger_name"],
        departure_date=data["departure_date"],
        departure_time=data["departure_time"],
        from_location=data["from_location"],
        to_location=data["to_location"],
        bus_operator=data["bus_operator"],
        seat_number=data["seat_number"],
        price=data["price"],
        status=data.get("status", "available")
    )
    db.session.add(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket created"}), 201

@app.route("/tickets", methods=["GET"])
def get_tickets():
    tickets = Ticket.query.order_by(Ticket.updated_at.desc()).all()
    return jsonify([{
        "pnr": t.pnr,
        "passenger_name": t.passenger_name,
        "departure_date": t.departure_date,
        "departure_time": t.departure_time,
        "from_location": t.from_location,
        "to_location": t.to_location,
        "bus_operator": t.bus_operator,
        "seat_number": t.seat_number,
        "price": t.price,
        "status": t.status,
        "updated_at": t.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    } for t in tickets])

@app.route("/tickets/<pnr>", methods=["GET"])
def get_ticket(pnr):
    ticket = Ticket.query.get(pnr)
    if ticket:
        return jsonify({
            "pnr": ticket.pnr,
            "passenger_name": ticket.passenger_name,
            "departure_date": ticket.departure_date,
            "departure_time": ticket.departure_time,
            "from_location": ticket.from_location,
            "to_location": ticket.to_location,
            "bus_operator": ticket.bus_operator,
            "seat_number": ticket.seat_number,
            "price": ticket.price,
            "status": ticket.status,
            "updated_at": ticket.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify({"message": "Ticket not found"}), 404

@app.route("/tickets/<pnr>/transfer", methods=["POST"])
def transfer_ticket(pnr):
    ticket = Ticket.query.get(pnr)
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    data = request.json
    ticket.passenger_name = data.get("passenger_name", ticket.passenger_name)
    ticket.status = "sold"
    db.session.commit()

    return jsonify({"message": "Ticket ownership transferred"})

# Render uses gunicorn, this is only for local
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host="0.0.0.0", port=port)


