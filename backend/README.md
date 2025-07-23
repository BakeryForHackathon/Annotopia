# Backend

## Setup

Install dependencies:

```bash
uv sync
```

## Development

Start the development server:

```bash
uv run api.py
```

## Production

Run the app in production mode (replace with your actual WSGI/ASGI server if needed):

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```