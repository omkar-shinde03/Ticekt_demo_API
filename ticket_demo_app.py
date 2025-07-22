# from flask import Flask, request, jsonify, render_template_string, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS
# from datetime import datetime
# import os

# app = Flask(__name__)
# CORS(app, resources={r"/api/*": {"origins": "*"}})

# # SQLite DB setup
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# db_path = os.path.join(BASE_DIR, "dummy_tickets.db")
# app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

# # ---------------------------- DATABASE ---------------------------- #
# class Ticket(db.Model):
#     pnr = db.Column(db.String, primary_key=True)
#     passenger_name = db.Column(db.String, nullable=False)
#     departure_date = db.Column(db.String, nullable=False)
#     departure_time = db.Column(db.String, nullable=False)
#     from_location = db.Column(db.String)
#     to_location = db.Column(db.String)
#     bus_operator = db.Column(db.String)
#     seat_number = db.Column(db.String)
#     price = db.Column(db.Integer)
#     status = db.Column(db.String, default="available")
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow)

# # ---------------------------- HELPER ---------------------------- #
# def ticket_to_dict(t):
#     return {
#         "pnr": t.pnr,
#         "passenger_name": t.passenger_name,
#         "departure_date": t.departure_date,
#         "departure_time": t.departure_time,
#         "from": t.from_location,
#         "to": t.to_location,
#         "bus_operator": t.bus_operator,
#         "seat_number": t.seat_number,
#         "price": t.price,
#         "status": t.status,
#         "updated_at": t.updated_at.strftime("%Y-%m-%d %H:%M:%S")
#     }

# # ---------------------------- API ROUTES ---------------------------- #
# @app.route("/api/tickets/create", methods=["POST"])
# def create_ticket():
#     data = request.get_json()
#     if Ticket.query.get(data["pnr"]):
#         return jsonify({"message": "Ticket already exists"}), 409
#     ticket = Ticket(**data)
#     db.session.add(ticket)
#     db.session.commit()
#     return jsonify({"message": "Dummy ticket created"}), 201

# @app.route("/api/tickets/verify", methods=["POST"])
# def verify_ticket():
#     data = request.get_json()
#     ticket = Ticket.query.filter_by(
#         pnr=data["pnr"],
#         passenger_name=data["passenger_name"],
#         departure_date=data["departure_date"],
#         departure_time=data["departure_time"]
#     ).first()
#     if ticket:
#         return jsonify({"status": "valid", "ticket": ticket_to_dict(ticket)})
#     return jsonify({"status": "invalid", "message": "Ticket not found"}), 404

# @app.route("/api/tickets", methods=["GET"])
# def get_all_tickets():
#     tickets = Ticket.query.all()
#     return jsonify([ticket_to_dict(t) for t in tickets])

# # ---------------------------- UI TEMPLATE ---------------------------- #
# TEMPLATE = '''
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Ticket Demo UI</title>
#     <style>
#         body { font-family: Arial; margin: 20px; }
#         .form-section, .card { margin-bottom: 30px; }
#         .card { border: 1px solid #ddd; padding: 20px; border-radius: 10px; width: 300px; display: inline-block; margin: 10px; vertical-align: top; }
#         .card.sold { background-color: #f8d7da; }
#         .card.available { background-color: #d4edda; }
#     </style>
# </head>
# <body>
#     <h1>🎫 Dummy Ticket Creator & Viewer</h1>

#     <div class="form-section">
#         <h2>Create Dummy Ticket</h2>
#         <form method="POST" action="{{ url_for('create_ticket_ui') }}">
#             <input name="pnr" placeholder="PNR" required><br><br>
#             <input name="passenger_name" placeholder="Passenger Name" required><br><br>
#             <input name="departure_date" type="date" required><br><br>
#             <input name="departure_time" type="time" required><br><br>
#             <input name="from_location" placeholder="From" required><br><br>
#             <input name="to_location" placeholder="To" required><br><br>
#             <input name="bus_operator" placeholder="Bus Operator" required><br><br>
#             <input name="seat_number" placeholder="Seat No" required><br><br>
#             <input name="price" placeholder="Price" type="number" required><br><br>
#             <button type="submit">Create Ticket</button>
#         </form>
#     </div>

#     <hr>

#     <h2>All Tickets</h2>
#     {% for ticket in tickets %}
#     <div class="card {{ ticket.status }}">
#         <strong>PNR:</strong> {{ ticket.pnr }}<br>
#         <strong>Name:</strong> {{ ticket.passenger_name }}<br>
#         <strong>From:</strong> {{ ticket.from }} → <strong>To:</strong> {{ ticket.to }}<br>
#         <strong>Date:</strong> {{ ticket.departure_date }} @ {{ ticket.departure_time }}<br>
#         <strong>Seat:</strong> {{ ticket.seat_number }}<br>
#         <strong>Price:</strong> ₹{{ ticket.price }}<br>
#         <strong>Status:</strong> {{ ticket.status }}<br>
#     </div>
#     {% endfor %}
# </body>
# </html>
# '''

# # ---------------------------- UI ROUTES ---------------------------- #
# @app.route("/", methods=["GET"])
# def index():
#     tickets = Ticket.query.order_by(Ticket.updated_at.desc()).all()
#     return render_template_string(TEMPLATE, tickets=[ticket_to_dict(t) for t in tickets])

# @app.route("/", methods=["POST"])
# def create_ticket_ui():
#     form = request.form
#     ticket = Ticket(
#         pnr=form["pnr"],
#         passenger_name=form["passenger_name"],
#         departure_date=form["departure_date"],
#         departure_time=form["departure_time"],
#         from_location=form["from_location"],
#         to_location=form["to_location"],
#         bus_operator=form["bus_operator"],
#         seat_number=form["seat_number"],
#         price=form["price"]
#     )
#     db.session.add(ticket)
#     db.session.commit()
#     return redirect(url_for('index'))

# # ---------------------------- RUN APP ---------------------------- #
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True, host="0.0.0.0", port=5000)























from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Use /tmp directory on Render
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join("/tmp", "dummy_tickets.db")  # ✅ FIX FOR RENDER
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

# ✅ Always create tables, even in production
with app.app_context():
    db.create_all()

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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)


