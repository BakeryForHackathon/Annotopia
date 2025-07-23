#!/bin/sh

# バックエンドサービスが起動し、ネットワークに登録されるまで十分に待ちます。
echo "Waiting for 30 seconds for backend service to become available..."
sleep 30

echo "Assuming backend is now ready. Starting Nginx."

# バックエンドが見つかったと仮定して、設定ファイルを生成します。
envsubst '${BACKEND_URL}' < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Nginxを起動します。
nginx -g 'daemon off;'
