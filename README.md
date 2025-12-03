
# posteet

Quick summary
-------------
posteet is a small web app for creating and organizing post-it notes.

- Backend: FastAPI (folder `api/`) with basic auth endpoints. CORS is configurable via the `ALLOWED_ORIGINS` environment variable.
- Frontend: Vue 3 + Vite (folder `webapp/`). The UI is componentized: `Login.vue`, `Register.vue`, `Dashboard.vue`, `Postit.vue`.
- UX: corkboard-style dashboard; post-its are editable and draggable. Data is persisted locally in the browser (`localStorage`) for now.

Getting started (Docker Compose)
--------------------------------
This project ships with a `compose.yaml` that can start the proxy, backend and frontend. The simplest way to run everything locally is via Docker Compose:

```bash
# from the repository root
docker compose -f compose.yaml up --build
```

After the services are up:

- Open `http://localhost` in your browser (the nginx proxy will route to the frontend and backend as configured).

If you prefer to run pieces locally during development, you can run the backend and frontend separately:

Backend (optional):
```bash
cd api
# use virtualenv if you want
pip install -r requirements.txt
uvicorn app:app --reload --port 8080
```

Frontend with Vite (dev mode):
```bash
cd webapp
npm install
npm run dev
# open http://localhost:5173
```

Notes
-----
- Post-it persistence is currently client-side (`localStorage` under key `posteet_postits`). For cross-device sync you can add API endpoints to persist notes server-side and update `Dashboard.vue` to sync.
- The frontend uses a Vite proxy in development (`VITE_API_URL`) to avoid CORS; production setups should rely on the proxy/nginx configuration.
