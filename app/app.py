import os
import uuid
import subprocess
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from lxml import etree

from app.services.storage import StorageService
from app.utils.decorators import token_required

app = Flask(__name__)
CORS(app)

# --- Landing & Help ---
@app.route('/')
def index():
    html = """
    <h1>Vulnerable API Lab</h1>
    <p>Welcome to the intentionally vulnerable API environment.</p>
    <p>This application is for security testing and QA automation training.</p>
    <p>See <a href="/help">/help</a> for API documentation.</p>
    <p><strong>WARNING: NOT FOR PRODUCTION USE.</strong></p>
    """
    return render_template_string(html)

@app.route('/help')
def help_page():
    html = """
    <h1>API Help</h1>
    <ul>
        <li>POST /tokens - Auth</li>
        <li>GET /eval?s=str - String handling</li>
        <li>POST /search - XML User search</li>
        <li>GET /uptime/{flag} - Debug/Uptime</li>
        <li>POST /user - Create user (Protected)</li>
        <li>GET /user/{user} - Get user (Protected)</li>
        <li>POST /widget - Create widget (Protected)</li>
    </ul>
    <h3>Auth Header:</h3>
    <pre>X-Auth-Token: [token]</pre>
    """
    return render_template_string(html)

# --- Authentication ---
@app.route('/tokens', methods=['POST'])
def create_token():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing credentials'}), 400

    user = StorageService.find_user(data['username'])
    if user and user['password'] == data['password']:  # Vulnerability: Plain text comparison
        token = str(uuid.uuid4())
        StorageService.save_token({'username': user['username'], 'token': token})
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

# --- Vulnerable Endpoints ---

@app.route('/eval', methods=['GET'])
def eval_endpoint():
    s = request.args.get('s', '')
    # Vulnerability: Unsafe eval simulation (actually just returning the value for now as per spec, 
    # but we can make it look like it's being evaluated)
    try:
        # In a real vulnerable app, this might be eval(s)
        # For simulation, we just return the result
        result = {"received": s, "note": "Simulation of unsafe evaluation"}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['POST'])
def search_user():
    # Vulnerability: XXE (XML External Entity)
    # lxml default parser is vulnerable to XXE if not configured otherwise
    try:
        xml_data = request.data
        parser = etree.XMLParser(resolve_entities=True) # Intentionally enabling entities
        root = etree.fromstring(xml_data, parser)
        username = root.find('user').text
        
        user = StorageService.find_user(username)
        if user:
            # Mask password in search result
            return f"<root><username>{user['username']}</username><role>{user['role']}</role></root>", 200, {'Content-Type': 'application/xml'}
        return "<root><error>User not found</error></root>", 404, {'Content-Type': 'application/xml'}
    except Exception as e:
        return f"<root><error>{str(e)}</error></root>", 500, {'Content-Type': 'application/xml'}

@app.route('/uptime/<path:flag>', methods=['GET'])
def uptime_check(flag):
    # Vulnerability: Command Injection
    # Intentionally concatenating string into shell command
    try:
        # User can pass something like ";ls" as flag
        cmd = f"uptime {flag}"
        # We'll use shell=True to make it vulnerable
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return jsonify({'output': output.decode('utf-8')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- User Management ---

@app.route('/user', methods=['POST'])
@token_required
def create_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing data'}), 400
    
    if StorageService.find_user(data['username']):
        return jsonify({'error': 'User already exists'}), 409
    
    user_data = {
        'username': data['username'],
        'password': data['password'],
        'role': 'user'
    }
    StorageService.save_user(user_data)
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/user/<username>', methods=['GET'])
@token_required
def get_user(username):
    # Vulnerability: IDOR (Insecure Direct Object Reference)
    # The endpoint doesn't check if the request.current_user matches the requested username
    user = StorageService.find_user(username)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# --- Widget Management ---

@app.route('/widget', methods=['POST'])
@token_required
def create_widget():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({'error': 'Missing data'}), 400
    
    widget_data = StorageService.save_widget({'name': data['name']})
    return jsonify({'message': 'Widget created', 'widget': widget_data}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
