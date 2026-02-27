import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
ANTHROPIC_URL = 'https://api.anthropic.com/v1/messages'


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    if not ANTHROPIC_API_KEY:
        return jsonify({
            'error': {'message': 'ANTHROPIC_API_KEY environment variable is not set.'}
        }), 500

    body = request.get_json(silent=True)
    if not body:
        return jsonify({'error': {'message': 'Request body must be JSON.'}}), 400

    resp = requests.post(
        ANTHROPIC_URL,
        headers={
            'x-api-key': ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json',
        },
        json=body,
        timeout=120,
    )

    return jsonify(resp.json()), resp.status_code


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
