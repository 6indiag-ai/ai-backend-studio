from flask import Flask, send_from_directory, request, jsonify, redirect
from flask_cors import CORS
import os, uuid, shutil, subprocess

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)   # CORS FIX

BASE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = os.path.join(BASE, 'uploads')
RESULTS = os.path.join(BASE, 'results')

if not os.path.exists(UPLOADS): os.makedirs(UPLOADS)
if not os.path.exists(RESULTS): os.makedirs(RESULTS)

# ---------- FRONTEND ROUTE ----------
@app.route('/frontend/<path:p>')
def frontend_files(p):
    return send_from_directory(os.path.join(BASE, '..', 'frontend'), p)

@app.route('/')
def index():
    return redirect('/frontend/index.html')

# ---------- HEALTH CHECK ----------
@app.route('/api/ping')
def ping():
    return jsonify({'ok': True, 'msg': 'AI Studio backend alive'})

# ---------- AUTH ----------
USERS = {}

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message':'email+password required'}), 400
    if email in USERS:
        return jsonify({'message':'User exists'}), 400
    USERS[email] = {'password':password, 'id':str(uuid.uuid4()), 'email':email}
    return jsonify({'message':'Registered'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    u = USERS.get(email)
    if not u or u['password'] != password:
        return jsonify({'message':'Invalid credentials'}), 400
    token = str(uuid.uuid4())
    u['token'] = token
    return jsonify({'token': token})

def require_auth(req):
    auth = req.headers.get('Authorization', '')
    if auth.startswith('Bearer '):
        token = auth.split(' ',1)[1]
        for u in USERS.values():
            if u.get('token') == token:
                return u
    return None

# ---------- PROCESSOR ----------
@app.route('/api/process/<action>', methods=['POST'])
def process(action):
    u = require_auth(request)
    if not u:
        return jsonify({'message':'Unauthorized'}), 401
    if 'file' not in request.files:
        return jsonify({'message':'file required'}), 400

    f = request.files['file']
    fname = str(uuid.uuid4()) + '_' + f.filename.replace(' ', '_')
    inpath = os.path.join(UPLOADS, fname)
    f.save(inpath)

    svc = os.path.join(BASE, 'services', action + '.py')
    outname = 'res_' + fname
    outpath = os.path.join(RESULTS, outname)

    if os.path.exists(svc):
        try:
            p = subprocess.run(['python3', svc, inpath, outpath], capture_output=True, timeout=120)
            if p.returncode != 0:
                return jsonify({'message':'service error','stderr': p.stderr.decode()}), 500
        except Exception as e:
            return jsonify({'message':'service run failed','error': str(e)}), 500
    else:
        shutil.copy(inpath, outpath)

    return jsonify({'message': 'processed', 'result': '/results/' + outname})

# ---------- RESULT FILES ----------
@app.route('/results/<path:p>')
def results(p):
    return send_from_directory(RESULTS, p)

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
