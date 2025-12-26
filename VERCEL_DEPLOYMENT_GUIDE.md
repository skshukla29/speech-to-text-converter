# Vercel Deployment Guide

This guide explains how to deploy your Speech-to-Text Converter to Vercel.

## Architecture Overview

- **Frontend**: React application deployed on Vercel
- **Backend**: Flask API (deploy separately on Render, Railway, or similar)
- **Communication**: Frontend uses environment variable `REACT_APP_BACKEND_URL` to connect to backend

## Prerequisites

1. Vercel account (sign up at https://vercel.com)
2. Backend deployed separately (see Backend Deployment section)
3. Git repository with your code

## Frontend Deployment Steps

### 1. Push Code to Git Repository

```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

### 2. Import Project to Vercel

1. Go to https://vercel.com/new
2. Connect your Git repository (GitHub, GitLab, or Bitbucket)
3. Select your `Speech-to-Text Converter` repository
4. Configure the project:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `build` (auto-detected)

### 3. Configure Environment Variables

In Vercel project settings, add the following environment variable:

**Key**: `REACT_APP_BACKEND_URL`  
**Value**: Your backend URL (e.g., `https://your-backend.onrender.com`)

**Important**: 
- Do NOT include a trailing slash
- Example: `https://speech-backend.onrender.com` ✅
- Not: `https://speech-backend.onrender.com/` ❌

### 4. Deploy

Click **Deploy** and Vercel will:
1. Install dependencies
2. Build your React app
3. Deploy to a global CDN
4. Provide a production URL (e.g., `your-app.vercel.app`)

## Backend Deployment

Your Flask backend needs to be deployed separately. Recommended platforms:

### Option 1: Render (Recommended)

1. Sign up at https://render.com
2. Create a new **Web Service**
3. Connect your Git repository
4. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3
5. Add environment variables if needed (API keys, etc.)
6. Deploy

### Option 2: Railway

1. Sign up at https://railway.app
2. Create a new project from your Git repository
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Deploy

### Option 3: PythonAnywhere

1. Sign up at https://www.pythonanywhere.com
2. Upload your backend code
3. Create a Flask web app
4. Configure WSGI file
5. Install requirements: `pip install -r requirements.txt`

## Important Backend Configuration

Add CORS support to your Flask backend (`backend/app.py`):

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["*"])  # In production, specify your Vercel domain
```

Install Flask-CORS if not already:

```bash
pip install flask-cors
echo "flask-cors" >> requirements.txt
```

## Testing Deployment

After deployment:

1. Visit your Vercel URL
2. Test file upload
3. Test live recording
4. Test translation feature
5. Check browser console for any API errors

## Troubleshooting

### API Calls Failing

**Problem**: API calls return 404 or CORS errors

**Solution**: 
1. Verify `REACT_APP_BACKEND_URL` in Vercel environment variables
2. Check backend CORS configuration
3. Ensure backend is running and accessible

### Environment Variable Not Working

**Problem**: Frontend still tries to connect to localhost

**Solution**:
1. Redeploy after adding environment variables
2. Check variable name is exactly `REACT_APP_BACKEND_URL`
3. Verify no typos in the backend URL

### Build Fails

**Problem**: Vercel build fails with npm errors

**Solution**:
1. Check `package.json` is valid
2. Verify all dependencies are listed
3. Ensure `frontend` directory is set as root in Vercel

### Static Assets Not Loading

**Problem**: Images or files don't load

**Solution**:
1. Check `vercel.json` routing configuration
2. Ensure assets are in `public/` folder
3. Use relative paths for imports

## Local Development

To test locally with environment variables:

1. Create `frontend/.env`:
```
REACT_APP_BACKEND_URL=http://localhost:5000
```

2. Start backend:
```bash
cd backend
python app.py
```

3. Start frontend:
```bash
cd frontend
npm start
```

## Production Checklist

- [ ] Backend deployed and accessible
- [ ] Backend URL added to Vercel environment variables
- [ ] CORS configured in backend
- [ ] Frontend deployed to Vercel
- [ ] All API endpoints tested
- [ ] File upload tested (check file size limits)
- [ ] Live recording tested
- [ ] Translation tested
- [ ] Error handling works correctly

## Custom Domain (Optional)

To use a custom domain:

1. Go to Vercel project settings
2. Navigate to **Domains**
3. Add your custom domain
4. Update DNS records as instructed
5. Update backend CORS to include your custom domain

## Cost Considerations

- **Vercel**: Free tier includes 100GB bandwidth, unlimited requests
- **Render**: Free tier includes 750 hours/month, sleeps after inactivity
- **Railway**: Free tier includes $5 credit/month
- **Whisper Model**: Running Whisper on free tiers may be slow; consider upgrading

## Security Recommendations

1. **API Keys**: Store sensitive keys in environment variables, never in code
2. **CORS**: In production, restrict CORS to your Vercel domain only
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **File Size**: Limit upload file sizes (currently 16MB in Flask)
5. **HTTPS**: Always use HTTPS in production (Vercel provides this automatically)

## Monitoring

Monitor your deployment:

1. **Vercel Dashboard**: View deployment logs and analytics
2. **Backend Logs**: Check your backend platform's logs
3. **Error Tracking**: Consider adding Sentry for error monitoring

## Support

If you encounter issues:

1. Check Vercel deployment logs
2. Check backend logs
3. Verify environment variables are set correctly
4. Test API endpoints directly using Postman or curl
5. Check browser console for frontend errors

## Next Steps

After successful deployment:

1. Share your Vercel URL with users
2. Monitor usage and performance
3. Consider adding authentication if needed
4. Implement analytics to track usage
5. Set up custom domain for professional appearance
