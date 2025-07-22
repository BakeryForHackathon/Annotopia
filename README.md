# Annotopia

## 注意点
React がローカルホストで，Flaskが別のホスト・ポートで動いているなら，CORSエラーが発生する．したがって，Flask側で以下の設定が必要．
```bash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 全てのオリジンを許可（開発中のみ推奨）

# 特定のオリジンだけ許可する場合
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
```

## memo
- Render に Flask backend をデプロイした時に割り当てられるURL
    ```bash
    https://annotopia-1jhd.onrender.com
    ```
- React からアクセスする API のエンドポイント
    ```bash
    https://annotopia-1jhd.onrender.com/api/login
    ```