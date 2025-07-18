from flask import Flask, request, jsonify
import json
import os
import time

app = Flask(__name__)

DATA_FILE = 'messages.json'

# Ensure the JSON file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

# Read messages from JSON file
def read_messages():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save messages to JSON file
def save_messages(messages):
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f)

# API: Get all messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = read_messages()
    return jsonify(messages)

# API: Post a new message
@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    message = {
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "user": data.get('user', 'unknown'),
        "message": data.get('message', '')
    }
    messages = read_messages()
    messages.append(message)
    save_messages(messages)
    return jsonify({"status": "Message saved", "message": message})

# Health Check
@app.route('/')
def home():
    return "Chat API running"

if __name__ == '__main__':
    app.run()
