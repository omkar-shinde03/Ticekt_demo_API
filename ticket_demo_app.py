# from flask import Flask, request, jsonify, render_template_string, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dummy_tickets.db"
# db = SQLAlchemy(app)

# # ---------------------------- DATABASE ---------------------------- #
# class Ticket(db.Model):
#     pnr = db.Column(db.String, primary_key=True)
#     passenger_name = db.Column(db.String, nullable=False)
#     departure_date = db.Column(db.String, nullable=False)  # "YYYY-MM-DD"
#     departure_time = db.Column(db.String, nullable=False)  # "HH:MM"
#     from_location = db.Column(db.String)
#     to_location = db.Column(db.String)
#     bus_operator = db.Column(db.String)
#     seat_number = db.Column(db.String)
#     price = db.Column(db.Integer)
#     status = db.Column(db.String, default="available")
#     buyer_name = db.Column(db.String, nullable=True)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow)

# # @app.before_first_request
# # def create_tables():
# #     db.create_all()

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

# @app.route("/api/tickets/<pnr>/transfer", methods=["PUT"])
# def transfer_ticket(pnr):
#     data = request.get_json()
#     ticket = Ticket.query.get(pnr)
#     if not ticket:
#         return jsonify({"message": "Ticket not found"}), 404
#     if ticket.status == "sold":
#         return jsonify({"message": "Ticket already sold"}), 409

#     ticket.buyer_name = data["buyer_name"]
#     ticket.passenger_name = data["buyer_name"]
#     ticket.status = "sold"
#     ticket.updated_at = datetime.utcnow()
#     db.session.commit()
#     return jsonify({"message": "Ticket transferred", "ticket": ticket_to_dict(ticket)})

# @app.route("/api/tickets", methods=["GET"])
# def get_all_tickets():
#     tickets = Ticket.query.all()
#     return jsonify([ticket_to_dict(t) for t in tickets])

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
#         "buyer_name": t.buyer_name,
#         "updated_at": t.updated_at.strftime("%Y-%m-%d %H:%M:%S")
#     }

# # ---------------------------- UI ROUTES ---------------------------- #

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
#         {% if ticket.status == 'available' %}
#         <form method="POST" action="{{ url_for('transfer_ticket_ui', pnr=ticket.pnr) }}">
#             <input name="buyer_name" placeholder="Buyer Name" required><br><br>
#             <button type="submit">Transfer</button>
#         </form>
#         {% else %}
#         <strong>Buyer:</strong> {{ ticket.buyer_name }}
#         {% endif %}
#     </div>
#     {% endfor %}
# </body>
# </html>
# '''

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

# @app.route("/transfer/<pnr>", methods=["POST"])
# def transfer_ticket_ui(pnr):
#     buyer_name = request.form["buyer_name"]
#     ticket = Ticket.query.get(pnr)
#     if ticket and ticket.status == "available":
#         ticket.buyer_name = buyer_name
#         ticket.passenger_name = buyer_name
#         ticket.status = "sold"
#         ticket.updated_at = datetime.utcnow()
#         db.session.commit()
#     return redirect(url_for('index'))

# # ---------------------------- RUN APP ---------------------------- #
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#         app.run(debug=True)






























from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dummy_tickets.db"
db = SQLAlchemy(app)

# ---------------------------- DATABASE ---------------------------- #
class Ticket(db.Model):
    pnr = db.Column(db.String, primary_key=True)
    passenger_name = db.Column(db.String, nullable=False)
    departure_date = db.Column(db.String, nullable=False)  # "YYYY-MM-DD"
    departure_time = db.Column(db.String, nullable=False)  # "HH:MM"
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
    data = request.get_json()
    if Ticket.query.get(data["pnr"]):
        return jsonify({"message": "Ticket already exists"}), 409
    ticket = Ticket(**data)
    db.session.add(ticket)
    db.session.commit()
    return jsonify({"message": "Dummy ticket created"}), 201

@app.route("/api/tickets/verify", methods=["POST"])
def verify_ticket():
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

@app.route("/api/tickets", methods=["GET"])
def get_all_tickets():
    tickets = Ticket.query.all()
    return jsonify([ticket_to_dict(t) for t in tickets])

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

# ---------------------------- UI ROUTES ---------------------------- #

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Ticket Demo UI</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .form-section, .card { margin-bottom: 30px; }
        .card { border: 1px solid #ddd; padding: 20px; border-radius: 10px; width: 300px; display: inline-block; margin: 10px; vertical-align: top; }
        .card.sold { background-color: #f8d7da; }
        .card.available { background-color: #d4edda; }
    </style>
</head>
<body>
    <h1>🎫 Dummy Ticket Creator & Viewer</h1>

    <div class="form-section">
        <h2>Create Dummy Ticket</h2>
        <form method="POST" action="{{ url_for('create_ticket_ui') }}">
            <input name="pnr" placeholder="PNR" required><br><br>
            <input name="passenger_name" placeholder="Passenger Name" required><br><br>
            <input name="departure_date" type="date" required><br><br>
            <input name="departure_time" type="time" required><br><br>
            <input name="from_location" placeholder="From" required><br><br>
            <input name="to_location" placeholder="To" required><br><br>
            <input name="bus_operator" placeholder="Bus Operator" required><br><br>
            <input name="seat_number" placeholder="Seat No" required><br><br>
            <input name="price" placeholder="Price" type="number" required><br><br>
            <button type="submit">Create Ticket</button>
        </form>
    </div>

    <hr>

    <h2>All Tickets</h2>
    {% for ticket in tickets %}
    <div class="card {{ ticket.status }}">
        <strong>PNR:</strong> {{ ticket.pnr }}<br>
        <strong>Name:</strong> {{ ticket.passenger_name }}<br>
        <strong>From:</strong> {{ ticket.from }} → <strong>To:</strong> {{ ticket.to }}<br>
        <strong>Date:</strong> {{ ticket.departure_date }} @ {{ ticket.departure_time }}<br>
        <strong>Seat:</strong> {{ ticket.seat_number }}<br>
        <strong>Price:</strong> ₹{{ ticket.price }}<br>
        <strong>Status:</strong> {{ ticket.status }}<br>
    </div>
    {% endfor %}
</body>
</html>
'''

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
    app.run(debug=True)
