# --- ステージ1: Reactアプリのビルド (変更なし) ---
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# --- ステージ2: Nginxでの配信 (最終修正) ---
FROM nginx:1.25-alpine

# envsubst (設定ファイル用) と ca-certificates (SSL証明書検証用)
RUN apk add --no-cache gettext ca-certificates

# ビルド成果物をコピー
COPY --from=build /app/dist /usr/share/nginx/html

# デフォルトの設定ファイルを削除
RUN rm /etc/nginx/conf.d/default.conf

# 静的な設定ファイルをコピー
COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 80

# Nginxを起動
CMD ["nginx", "-g", "daemon off;"]
