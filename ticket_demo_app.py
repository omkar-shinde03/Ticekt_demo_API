from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Use /tmp for Render deployment
db_path = os.path.join("/tmp", "dummy_tickets.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Ticket model
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

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head>
        <title>Dummy Ticket API</title>
        <style>
            body { font-family: Arial; background: #f5f5f5; padding: 20px; }
            h1, h2 { color: #333; }
            form { margin-bottom: 30px; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            input, button { display: block; margin: 10px 0; padding: 8px; width: 100%; }
            .ticket { background: #fff; padding: 15px; margin: 10px 0; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <h1>✅ Dummy Ticket API is running!</h1>
        <p>Use <code>/tickets</code> endpoint for GET/POST from backend or use the form below.</p>

        <h2>📝 Create a Ticket</h2>
        <form id="ticketForm">
            <input type="text" name="pnr" placeholder="PNR" required />
            <input type="text" name="passenger_name" placeholder="Passenger Name" required />
            <input type="text" name="departure_date" placeholder="Departure Date (YYYY-MM-DD)" required />
            <input type="text" name="departure_time" placeholder="Departure Time (HH:MM)" required />
            <input type="text" name="from_location" placeholder="From" required />
            <input type="text" name="to_location" placeholder="To" required />
            <input type="text" name="bus_operator" placeholder="Bus Operator" required />
            <input type="text" name="seat_number" placeholder="Seat Number" required />
            <input type="number" step="0.01" name="price" placeholder="Price" required />
            <button type="submit">Create Ticket</button>
        </form>

        <h2>🚌 All Tickets</h2>
        <div id="ticketList"></div>

        <script>
            const form = document.getElementById("ticketForm");
            const ticketList = document.getElementById("ticketList");

            form.addEventListener("submit", async (e) => {
                e.preventDefault();
                const formData = new FormData(form);
                const data = Object.fromEntries(formData.entries());
                const response = await fetch("/tickets", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    form.reset();
                    loadTickets();
                } else {
                    alert("Ticket creation failed.");
                }
            });

            async function loadTickets() {
                const res = await fetch("/tickets");
                const tickets = await res.json();
                ticketList.innerHTML = "";
                tickets.forEach(t => {
                    const div = document.createElement("div");
                    div.className = "ticket";
                    div.innerHTML = `
                        <strong>${t.pnr}</strong> - ${t.passenger_name}<br>
                        ${t.from_location} ➜ ${t.to_location}<br>
                        Date: ${t.departure_date} @ ${t.departure_time}<br>
                        Seat: ${t.seat_number}, ₹${t.price}<br>
                        Status: <b>${t.status}</b>
                    `;
                    ticketList.appendChild(div);
                });
            }

            loadTickets();
        </script>
    </body>
    </html>
    """)

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
        price=float(data["price"]),
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
