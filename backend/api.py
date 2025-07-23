from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from functools import wraps
import re
import os
from collections import defaultdict

app = Flask(__name__)
CORS(app, 
     origins=["http://localhost:5173", "http://127.0.0.1:5173"],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization", "X-CSRF-Token"],
     methods=["GET", "POST", "OPTIONS"])

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-super-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per hour"]
)
limiter.init_app(app)

login_attempts = defaultdict(lambda: {'count': 0, 'last_attempt': None, 'locked_until': None})
failed_attempts = defaultdict(int)

csrf_tokens = {}
active_sessions = {}

DUMMY_USERS = {
    "Taro": {
        "id": 3,
        "username": "Taro",
        "email": "taro@example.com",
        "role": "user",
        "salt": "taro_unique_salt_123",
        "password_hash": generate_password_hash("Password123!"),
        "is_locked": False,
        "created_at": "2024-01-01T00:00:00Z"
    },
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com", 
        "role": "admin",
        "salt": "admin_unique_salt_456",
        "password_hash": generate_password_hash("AdminPass123!"),
        "is_locked": False,
        "created_at": "2024-01-01T00:00:00Z"
    }
}

def generate_jwt_token(user_data, expires_in=3600):
    payload = {
        'user_id': user_data['id'],
        'username': user_data['username'],
        'role': user_data['role'],
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow(),
        'jti': secrets.token_hex(16)
    }
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_csrf_token():
    token = secrets.token_hex(32)
    csrf_tokens[token] = {
        'created_at': time.time(),
        'used': False
    }
    return token

def verify_csrf_token(token):
    if not token or token not in csrf_tokens:
        return False
    
    token_data = csrf_tokens[token]
    if time.time() - token_data['created_at'] > 600:
        del csrf_tokens[token]
        return False
    
    if token_data['used']:
        return False
    
    token_data['used'] = True
    return True

def is_account_locked(username):
    if username in login_attempts:
        attempt_data = login_attempts[username]
        if attempt_data['locked_until'] and datetime.now() < attempt_data['locked_until']:
            return True
        elif attempt_data['locked_until'] and datetime.now() >= attempt_data['locked_until']:
            login_attempts[username] = {'count': 0, 'last_attempt': None, 'locked_until': None}
    return False

def record_login_attempt(username, success=False):
    current_time = datetime.now()
    
    if success:
        if username in login_attempts:
            del login_attempts[username]
        return
    
    attempt_data = login_attempts[username]
    attempt_data['count'] += 1
    attempt_data['last_attempt'] = current_time
    
    if attempt_data['count'] >= 5:
        attempt_data['locked_until'] = current_time + timedelta(minutes=15)

def validate_password_strength(password):
    if len(password) < 8:
        return False, "パスワードは8文字以上である必要があります"
    if len(password) > 128:
        return False, "パスワードは128文字以下である必要があります"
    if not re.search(r'[a-z]', password):
        return False, "パスワードは小文字を含む必要があります"
    if not re.search(r'[A-Z]', password):
        return False, "パスワードは大文字を含む必要があります"
    if not re.search(r'\d', password):
        return False, "パスワードは数字を含む必要があります"
    return True, ""

def validate_username(username):
    if not username or len(username.strip()) == 0:
        return False, "ユーザー名は必須です"
    if len(username) < 3 or len(username) > 50:
        return False, "ユーザー名は3-50文字である必要があります"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "ユーザー名は英数字とアンダースコアのみ使用可能です"
    return True, ""

def hash_password_client_side(password, salt):
    import hashlib
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 10000).hex()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'success': False, 'message': '無効なトークン形式'}), 401
        
        if not token:
            return jsonify({'success': False, 'message': 'トークンが必要です'}), 401
        
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({'success': False, 'message': '無効または期限切れのトークンです'}), 401
            
        request.current_user = payload
        return f(*args, **kwargs)
    
    return decorated

@app.route('/api/csrf-token', methods=['GET'])
def get_csrf_token():
    token = generate_csrf_token()
    return jsonify({'csrfToken': token}), 200

@app.route('/api/get-salt', methods=['POST'])
@limiter.limit("10 per minute")
def get_user_salt():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400
    
    username = data.get('username', '').strip()
    
    is_valid, error_message = validate_username(username)
    if not is_valid:
        return jsonify({"success": False, "message": error_message}), 400
    
    user_data = DUMMY_USERS.get(username)
    if user_data:
        salt = user_data['salt']
    else:
        salt = hashlib.sha256(f"dummy_salt_{username}".encode()).hexdigest()[:32]
    
    return jsonify({'salt': salt}), 200

@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login_user():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')
    csrf_token = data.get('csrfToken')
    user_agent = data.get('userAgent', '')
    timestamp = data.get('timestamp')

    if not verify_csrf_token(csrf_token):
        return jsonify({"success": False, "message": "無効なCSRFトークンです"}), 403

    is_valid_username, username_error = validate_username(username)
    if not is_valid_username:
        return jsonify({"success": False, "message": username_error}), 400

    if not password:
        return jsonify({"success": False, "message": "パスワードは必須です"}), 400

    if is_account_locked(username):
        return jsonify({
            "success": False, 
            "message": "アカウントがロックされています。しばらく待ってから再試行してください。"
        }), 423

    user_data = DUMMY_USERS.get(username)
    if not user_data:
        record_login_attempt(username, success=False)
        return jsonify({
            "success": False,
            "message": "ユーザー名またはパスワードが正しくありません"
        }), 401

    if user_data.get('is_locked', False):
        return jsonify({
            "success": False,
            "message": "アカウントがロックされています。管理者にお問い合わせください。"
        }), 423

    expected_hash = hash_password_client_side("Password123!" if username == "Taro" else "AdminPass123!", user_data['salt'])
    
    if password != expected_hash:
        record_login_attempt(username, success=False)
        return jsonify({
            "success": False,
            "message": "ユーザー名またはパスワードが正しくありません"
        }), 401

    record_login_attempt(username, success=True)

    access_token = generate_jwt_token(user_data, expires_in=3600)  # 1時間
    refresh_token = generate_jwt_token(user_data, expires_in=7*24*3600)  # 7日間

    session_id = secrets.token_hex(32)
    active_sessions[session_id] = {
        'user_id': user_data['id'],
        'username': username,
        'created_at': datetime.now(),
        'user_agent': user_agent,
        'last_activity': datetime.now()
    }

    response_data = {
        "success": True,
        "token": access_token,
        "refreshToken": refresh_token,
        "expiresIn": 3600,
        "user": {
            "id": user_data["id"],
            "username": user_data["username"],
            "email": user_data["email"],
            "role": user_data["role"]
        },
        "sessionId": session_id
    }

    response = jsonify(response_data)
    
    response.set_cookie('session_id', session_id, 
                       httponly=True, 
                       secure=True,
                       samesite='Lax',
                       max_age=3600)

    return response, 200

@app.route('/api/verify-session', methods=['GET'])
@token_required
def verify_session():
    user_id = request.current_user['user_id']
    username = request.current_user['username']
    
    user_data = None
    for user in DUMMY_USERS.values():
        if user['id'] == user_id:
            user_data = user
            break
    
    if not user_data:
        return jsonify({'valid': False, 'message': 'ユーザーが見つかりません'}), 404
    
    return jsonify({
        'valid': True,
        'user': {
            'id': user_data['id'],
            'username': user_data['username'],
            'email': user_data['email'],
            'role': user_data['role']
        }
    }), 200

@app.route('/api/refresh-token', methods=['POST'])
@limiter.limit("10 per minute")
def refresh_token():
    data = request.get_json()
    refresh_token = data.get('refreshToken')
    
    if not refresh_token:
        return jsonify({'success': False, 'message': 'リフレッシュトークンが必要です'}), 400
    
    payload = verify_jwt_token(refresh_token)
    if not payload:
        return jsonify({'success': False, 'message': '無効なリフレッシュトークンです'}), 401
    
    user_data = None
    for user in DUMMY_USERS.values():
        if user['id'] == payload['user_id']:
            user_data = user
            break
    
    if not user_data:
        return jsonify({'success': False, 'message': 'ユーザーが見つかりません'}), 404
    
    new_access_token = generate_jwt_token(user_data, expires_in=3600)
    
    return jsonify({
        'success': True,
        'token': new_access_token,
        'expiresIn': 3600
    }), 200

@app.route('/api/logout', methods=['POST'])
@token_required
def logout():
    session_id = request.cookies.get('session_id')
    
    if session_id and session_id in active_sessions:
        del active_sessions[session_id]
    
    response = jsonify({'success': True, 'message': 'ログアウトしました'})
    response.set_cookie('session_id', '', expires=0)
    
    return response, 200

@app.route('/api/user/profile', methods=['GET'])
@token_required
def get_user_profile():
    user_id = request.current_user['user_id']
    
    user_data = None
    for user in DUMMY_USERS.values():
        if user['id'] == user_id:
            user_data = user
            break
    
    if not user_data:
        return jsonify({'success': False, 'message': 'ユーザーが見つかりません'}), 404
    
    return jsonify({
        'success': True,
        'user': {
            'id': user_data['id'],
            'username': user_data['username'],
            'email': user_data['email'],
            'role': user_data['role'],
            'created_at': user_data['created_at']
        }
    }), 200

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'success': False, 'message': 'リクエストが多すぎます。しばらく待ってから再試行してください。'}), 429

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'message': 'サーバー内部エラーが発生しました'}), 500

@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

if __name__ == '__main__':
    print("利用可能なテストユーザー:")
    for username, user_data in DUMMY_USERS.items():
        test_password = "Password123!" if username == "Taro" else "AdminPass123!"
        print(f"  ユーザー名: {username}")
        print(f"  パスワード: {test_password}")
        print(f"  ロール: {user_data['role']}")
        print()
    
    app.run(debug=True, port=5001, host='127.0.0.1')