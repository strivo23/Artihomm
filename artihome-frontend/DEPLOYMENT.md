# Frontend Deployment

This app is built to deploy as a static Vite site on Vercel.

Required production setting:

- `VITE_API_URL=https://artihome-backend.onrender.com/api`

Vercel config:

- Build command: `npm run build`
- Output directory: `artihome-frontend/dist`

Notes:

- The frontend does not fall back to a relative `/api` URL in production.
- If `VITE_API_URL` is missing, the app will fail fast with a clear error.