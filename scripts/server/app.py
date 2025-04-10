from flask import Flask, jsonify, send_from_directory, request
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json
import subprocess
app=Flask(__name__, static_folder='../../frontend/react_app/build', static_url_path='')

def fetch_data_periodically():
    # Call the fetch_data.py script using subprocess
    try:
        subprocess.run(['python', os.path.join(os.path.dirname(__file__), '../data_collection/fetch_data.py')], check=True)
        print("Data fetched successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error fetching data: {e}")

scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_data_periodically, trigger="interval", minutes=60)  # Fetch data every 60 minutes
scheduler.start()

@app.route('/api/executive-orders', methods=['GET'])
def get_executive_orders():
    json_path = os.path.join(os.path.dirname(__file__), '../data_collection/executive_orders.json')
    with open(json_path, 'r') as json_file:
        executive_orders = json.load(json_file)
    return jsonify(executive_orders)
@app.route('/api/wordcloud', methods=['GET'])
def get_wordcloud():
    wordcloud_path=os.path.join(os.getcwd(), 'wordcloud.png')
    
    return send_from_directory('../data_collection', 'wordcloud.png')
"""@app.route('/api/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400"""

@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def serve_react_app(path):
    if path!="" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__=='__main__':
    app.run(debug=True, port=5000)  # Run the Flask app on port 5000
    # Note: In a production environment, you would typically use a WSGI server like Gunicorn or uWSGI instead of the built-in Flask server.