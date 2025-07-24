# Pythonの公式イメージをベースとして使用
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt .

# pipで依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# アプリケーションを起動。ワーカー数、種類、ログレベルを明示的に指定します。
CMD gunicorn --workers 1 --worker-class gevent --bind "0.0.0.0:$PORT" --timeout 120 --log-level=debug app:app
