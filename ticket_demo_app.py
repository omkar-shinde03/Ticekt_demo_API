from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Persistent SQLite path (for local dev). For hosting, use PostgreSQL URL.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "dummy_tickets.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------------------- DATABASE ---------------------------- #
class Ticket(db.Model):
    pnr = db.Column(db.String, primary_key=True)
    passenger_name = db.Column(db.String, nullable=False)
    departure_date = db.Column(db.String, nullable=False)
    departure_time = db.Column(db.String, nullable=False)
    from_location = db.Column(db.String)
    to_location = db.Column(db.String)
    bus_operator = db.Column(db.String)
    seat_number = db.Column(db.String)
    price = db.Column(db.Integer)
    status = db.Column(db.String, default="available")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------------------- API ROUTES ---------------------------- #
@app.route("/api/tickets/create", methods=["POST"])
def create_ticket():
    try:
        data = request.get_json()
        if Ticket.query.get(data["pnr"]):
            return jsonify({"message": "Ticket already exists"}), 409
        ticket = Ticket(**data)
        db.session.add(ticket)
        db.session.commit()
        return jsonify({"message": "Dummy ticket created"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tickets/verify", methods=["POST"])
def verify_ticket():
    try:
        data = request.get_json()
        ticket = Ticket.query.filter_by(
            pnr=data["pnr"],
            passenger_name=data["passenger_name"],
            departure_date=data["departure_date"],
            departure_time=data["departure_time"]
        ).first()
        if ticket:
            return jsonify({"status": "valid", "ticket": ticket_to_dict(ticket)})
        return jsonify({"status": "invalid", "message": "Ticket not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tickets", methods=["GET"])
def get_all_tickets():
    try:
        tickets = Ticket.query.all()
        return jsonify([ticket_to_dict(t) for t in tickets])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def ticket_to_dict(t):
    return {
        "pnr": t.pnr,
        "passenger_name": t.passenger_name,
        "departure_date": t.departure_date,
        "departure_time": t.departure_time,
        "from": t.from_location,
        "to": t.to_location,
        "bus_operator": t.bus_operator,
        "seat_number": t.seat_number,
        "price": t.price,
        "status": t.status,
        "updated_at": t.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    }

# ---------------------------- UI ROUTES (Same as before) ---------------------------- #
# Keep your TEMPLATE and UI routes unchanged unless you want frontend hosted separately.

@app.route("/", methods=["GET"])
def index():
    tickets = Ticket.query.order_by(Ticket.updated_at.desc()).all()
    return render_template_string(TEMPLATE, tickets=[ticket_to_dict(t) for t in tickets])

@app.route("/", methods=["POST"])
def create_ticket_ui():
    form = request.form
    ticket = Ticket(
        pnr=form["pnr"],
        passenger_name=form["passenger_name"],
        departure_date=form["departure_date"],
        departure_time=form["departure_time"],
        from_location=form["from_location"],
        to_location=form["to_location"],
        bus_operator=form["bus_operator"],
        seat_number=form["seat_number"],
        price=form["price"]
    )
    db.session.add(ticket)
    db.session.commit()
    return redirect(url_for('index'))

# ---------------------------- RUN APP ---------------------------- #
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
