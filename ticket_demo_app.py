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
        <head><title>🎟️ Dummy Ticket API</title></head>
        <body style="font-family:sans-serif;padding:20px">
            <h2>✅ Dummy Ticket API is running!</h2>
            <p>Use <code>/tickets</code> endpoint for GET/POST.</p>
            <hr>
            <h3>📝 Create New Ticket</h3>
            <form method="post" action="/tickets">
                PNR: <input name="pnr"><br>
                Name: <input name="name"><br>
                Age: <input name="age"><br>
                From: <input name="from_location"><br>
                To: <input name="to_location"><br>
                <button type="submit">Create Ticket</button>
            </form>
            <hr>
            <h3>🚌 All Tickets:</h3>
            <ul>
                {% for ticket in tickets %}
                    <li><b>{{ ticket['pnr'] }}</b> - {{ ticket['name'] }} ({{ ticket['age'] }}) from {{ ticket['from_location'] }} to {{ ticket['to_location'] }}</li>
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
            'to_location': data.get('to_location')
        }
        tickets.append(new_ticket)
        if request.form:
            return redirect('/')
        return jsonify({'message': 'Ticket created', 'ticket': new_ticket}), 201

# Health check route
@app.route('/ping')
def ping():
    return "pong"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
