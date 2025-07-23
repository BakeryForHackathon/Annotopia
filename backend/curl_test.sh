#!/bin/bash

USERNAME="Taro"
PLAINTEXT_PASSWORD="Password123!"
USER_AGENT="curl-script"
BASE_URL="http://127.0.0.1:5001"
COOKIE_JAR="./cookies.txt"

# 1. CSRFトークン取得 (cookie保存)
CSRF_TOKEN=$(curl -s -c $COOKIE_JAR "$BASE_URL/api/csrf-token" | jq -r '.csrfToken')

# 2. ソルト取得
SALT=$(curl -s -X POST "$BASE_URL/api/get-salt" \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"$USERNAME\"}" | jq -r '.salt')

# 3. ハッシュ生成
HASHED_PASSWORD=$(/Users/yoneyama/workspace/github/Annotopia/Annotopia@nishida/backend/.venv/bin/python3 -c "
import hashlib
pwd = '$PLAINTEXT_PASSWORD'
salt = '$SALT'
h = hashlib.pbkdf2_hmac('sha256', pwd.encode(), salt.encode(), 10000).hex()
print(h)
")

# 4. ログイン (cookie送信)
LOGIN_RESPONSE=$(curl -s -b $COOKIE_JAR -X POST "$BASE_URL/api/login" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$USERNAME\",
    \"password\": \"$HASHED_PASSWORD\",
    \"csrfToken\": \"$CSRF_TOKEN\",
    \"userAgent\": \"$USER_AGENT\",
    \"timestamp\": $(date +%s)
  }")

echo "Login Response:"
echo "$LOGIN_RESPONSE"

ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.token')
SESSION_ID=$(echo "$LOGIN_RESPONSE" | jq -r '.sessionId')

# 5. プロファイル取得
curl -s -X GET "$BASE_URL/api/user/profile" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
