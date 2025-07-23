from flask import Flask, request, jsonify, render_template_string, redirect
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

# In-memory ticket store
tickets = []

# Home page with UI
@app.route('/')
def index():
    return render_template_string('''
        <html>
        <head><title>🎟️ Travel Ticket API</title></head>
        <body style="font-family:sans-serif;padding:20px">
            <h2>🚌 Dummy Travel Ticket API is Running</h2>
            <p>Use <code>/tickets</code> endpoint to view/create tickets.</p>
            <hr>
            <h3>📝 Create New Ticket</h3>
            <form method="post" action="/tickets">
                PNR: <input name="pnr"><br>
                Name: <input name="name"><br>
                Age: <input name="age"><br>
                From: <input name="from_location"><br>
                To: <input name="to_location"><br>
                Travel Date: <input name="travel_date" type="date"><br>
                Departure Time: <input name="departure_time" type="time"><br>
                Arrival Time: <input name="arrival_time" type="time"><br>
                Operator: <input name="operator"><br>
                Seat No: <input name="seat_number"><br>
                <button type="submit">Create Ticket</button>
            </form>
            <hr>
            <h3>📋 All Tickets</h3>
            <ul>
                {% for t in tickets %}
                    <li>
                        <b>{{ t['pnr'] }}</b>: {{ t['name'] }} ({{ t['age'] }} yrs) — 
                        {{ t['from_location'] }} → {{ t['to_location'] }} on {{ t['travel_date'] }}<br>
                        ⏰ {{ t['departure_time'] }} - {{ t['arrival_time'] }} | 🪑 Seat {{ t['seat_number'] }} | 🏢 {{ t['operator'] }}
                    </li>
                {% endfor %}
            </ul>
        </body>
        </html>
    ''', tickets=tickets)

# API endpoint to get or create tickets
@app.route('/tickets', methods=['GET', 'POST'])
def manage_tickets():
    if request.method == 'GET':
        return jsonify(tickets)

    if request.method == 'POST':
        data = request.form if request.form else request.json
        new_ticket = {
            'id': str(uuid.uuid4()),
            'pnr': data.get('pnr'),
            'name': data.get('name'),
            'age': data.get('age'),
            'from_location': data.get('from_location'),
            'to_location': data.get('to_location'),
            'travel_date': data.get('travel_date'),
            'departure_time': data.get('departure_time'),
            'arrival_time': data.get('arrival_time'),
            'operator': data.get('operator'),
            'seat_number': data.get('seat_number')
        }
        tickets.append(new_ticket)
        if request.form:
            return redirect('/')
        return jsonify({'message': 'Ticket created', 'ticket': new_ticket}), 201

@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

