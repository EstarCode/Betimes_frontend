# Deployment Guide

## Backend Deployment (Render)

### Step 1: Prepare Repository
```bash
git init
git add .
git commit -m "Initial commit: Betimes"
git push origin main
```

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up or log in
3. Connect your GitHub account

### Step 3: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure:
   - **Name:** betimes-backend
   - **Root Directory:** `backend`
   - **Environment:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application`

### Step 4: Add Environment Variables
```
PYTHON_VERSION=3.11.0
DEBUG=False
SECRET_KEY=<generate-random-secret-key>
ALLOWED_HOSTS=.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

### Step 5: Add PostgreSQL Database
1. Create PostgreSQL database in Render
   - Database Name: `betimes`
   - User: `betimes`
2. Copy `DATABASE_URL` and add to environment variables

### Step 6: Add Redis
1. Create Redis instance in Render
2. Copy `REDIS_URL` and add to environment variables
3. Add `CELERY_BROKER_URL` (same as REDIS_URL)
4. Add `CELERY_RESULT_BACKEND` (same as REDIS_URL)

### Step 7: Deploy
Click "Create Web Service" and wait for deployment

---

## Frontend Deployment (Vercel)

### Step 1: Create Vercel Account
1. Go to https://vercel.com
2. Sign up or log in
3. Connect your GitHub account

### Step 2: Import Project
1. Click "Add New..." → "Project"
2. Import your GitHub repository
3. Configure:
   - **Framework Preset:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`

### Step 3: Add Environment Variables
```
VITE_API_URL=https://your-backend.onrender.com/api
```

### Step 4: Deploy
Click "Deploy" and wait for deployment

---

## Post-Deployment Configuration

### Update CORS Settings
1. Go to Render dashboard
2. Update `CORS_ALLOWED_ORIGINS` with your Vercel URL:
   ```
   CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
   ```

### Update API URL
1. Go to Vercel dashboard
2. Update `VITE_API_URL` with your Render URL:
   ```
   VITE_API_URL=https://your-backend.onrender.com/api
   ```

### Redeploy Both Services
- Render: Click "Manual Deploy" → "Deploy latest commit"
- Vercel: Automatically redeploys on environment variable change

---

## Testing Deployment

1. Visit your Vercel URL
2. Try to register/login
3. Upload and process a document
4. Check Render logs for any errors

---

## Monitoring

### Render
- View logs: Dashboard → Your Service → Logs
- Monitor metrics: Dashboard → Your Service → Metrics

### Vercel
- View logs: Dashboard → Your Project → Deployments → View Function Logs
- Monitor analytics: Dashboard → Your Project → Analytics

---

## Troubleshooting

### Backend Issues

**Build fails:**
```bash
# Check build.sh has execute permissions
chmod +x backend/build.sh
```

**Database connection error:**
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL instance is running

**Static files not loading:**
```bash
# Ensure collectstatic runs in build.sh
python manage.py collectstatic --no-input
```

### Frontend Issues

**Build fails:**
- Check `package.json` scripts
- Verify all dependencies are listed

**API calls fail:**
- Verify `VITE_API_URL` is correct
- Check CORS settings in backend

**404 errors:**
- Ensure `vercel.json` has correct rewrites

---

## Custom Domain (Optional)

### Render
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records

### Vercel
1. Go to Settings → Domains
2. Add your domain
3. Update DNS records

---

## Continuous Deployment

Both Render and Vercel automatically deploy when you push to your main branch:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render and Vercel will automatically build and deploy your changes.
