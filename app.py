from flask import Flask, request, jsonify
import json
import os
import time

app = Flask(__name__)

DATA_FILE = 'messages.json'

# Ensure messages.json exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

def read_messages():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_messages(messages):
    with open(DATA_FILE, 'w') as f:
        json.dump(messages, f)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = read_messages()
    return jsonify(messages)

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

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "Server is awake!"})

@app.route('/')
def home():
    return "Chat API is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
