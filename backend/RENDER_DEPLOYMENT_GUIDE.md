# Render Deployment Guide for Flask + Whisper Backend

## Prerequisites
- GitHub repository with your code pushed
- Render account (free tier works)

## Deployment Configuration

### 1. Create New Web Service

1. Go to https://render.com/dashboard
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Select your `Speech-to-Text Converter` repository

### 2. Service Settings

Configure with these exact settings:

| Setting | Value |
|---------|-------|
| **Name** | `speech-to-text-backend` (or your choice) |
| **Region** | Choose closest to your users |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `apt-get update && apt-get install -y ffmpeg && pip install --upgrade pip && pip install setuptools wheel Cython && pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |

### 3. Environment Variables

Add these in Render dashboard under **Environment**:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.10.8` | Stable version for Whisper |
| `PORT` | (auto-set by Render) | Don't modify |

### 4. Plan Selection

- **Free Tier**: 
  - 750 hours/month
  - Spins down after 15 min inactivity
  - First request takes 30-60s after spin-down
  - Good for testing
  
- **Starter ($7/month)**:
  - Always on
  - Faster performance
  - Recommended for production

## Detailed Build Command Explanation

```bash
# Update package manager
apt-get update && 

# Install FFmpeg (required for audio processing)
apt-get install -y ffmpeg && 

# Upgrade pip
pip install --upgrade pip && 

# Install build dependencies first (prevents wheel errors)
pip install setuptools wheel Cython && 

# Install all requirements
pip install -r requirements.txt
```

**Why this order?**
- FFmpeg must be installed at system level for audio processing
- setuptools, wheel, Cython must be installed before openai-whisper
- This prevents "Getting requirements to build wheel: error"

## Detailed Start Command Explanation

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**Parameters:**
- `app:app` - Your Flask app instance
- `--bind 0.0.0.0:$PORT` - Listen on all interfaces, use Render's PORT
- `--workers 2` - 2 worker processes (good for free tier)
- `--timeout 120` - 2-minute timeout for large file uploads

## Expected Build Time

- **First deploy**: 15-20 minutes
  - Installing FFmpeg: 2-3 min
  - Installing PyTorch: 8-10 min
  - Installing Whisper: 3-5 min
  - Installing other packages: 2-3 min

- **Subsequent deploys**: 5-10 minutes (cached dependencies)

## Deployment Process

### 1. Initial Push

```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

### 2. Watch Build Logs

In Render dashboard:
1. Click on your service
2. Go to **Logs** tab
3. Watch for successful deployment

**Success indicators:**
```
==> Installing dependencies
==> Build successful
==> Starting service
Loading Whisper model...
[INFO] Booting worker with pid: 123
```

### 3. Test Deployment

Once deployed, Render provides a URL like:
`https://speech-to-text-backend.onrender.com`

**Test health endpoint:**
```bash
curl https://your-backend.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Speech-to-Text API is running"
}
```

## Common Deployment Issues

### Issue 1: "Failed to build wheel for openai-whisper"

**Cause**: Build dependencies not installed first

**Solution**: Use the exact build command provided above with setuptools, wheel, Cython installed before requirements.txt

### Issue 2: "FFmpeg not found"

**Cause**: FFmpeg not installed at system level

**Solution**: Include `apt-get install -y ffmpeg` in build command

### Issue 3: Build times out after 15 minutes

**Cause**: PyTorch is large (500MB+)

**Solution**: 
- Use the stable torch version in requirements.txt (2.0.1, not 2.1.0)
- Or use CPU-only version: `torch==2.0.1+cpu -f https://download.pytorch.org/whl/torch_stable.html`

### Issue 4: Service crashes on startup

**Cause**: Whisper model too large for free tier RAM

**Solution**: In `app.py`, use smaller model:
```python
transcriber = WhisperTranscriber(model_size="tiny")  # Uses less RAM
```

### Issue 5: First request takes forever

**Cause**: Free tier spins down after inactivity

**Solutions**:
1. Accept 30-60s first load (expected on free tier)
2. Upgrade to Starter plan ($7/month) for always-on service
3. Use a cron-job service to ping your backend every 14 minutes

### Issue 6: CORS errors from frontend

**Cause**: CORS not properly configured

**Solution**: Already fixed in app.py with `CORS(app)`

## Performance Optimization

### For Free Tier:

1. **Use smallest Whisper model:**
```python
transcriber = WhisperTranscriber(model_size="tiny")  # 39MB
# Instead of "base" (74MB) or "small" (244MB)
```

2. **Limit file sizes:**
```python
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max
```

3. **Reduce workers:**
```bash
gunicorn app:app --workers 1  # Less memory usage
```

### For Paid Tier:

1. **Use better model:**
```python
transcriber = WhisperTranscriber(model_size="small")  # Better accuracy
```

2. **More workers:**
```bash
gunicorn app:app --workers 4  # Handle more concurrent requests
```

## Monitoring

After deployment, monitor:

1. **Logs**: Check for errors in Render dashboard
2. **Metrics**: View CPU, memory usage in Render
3. **Health check**: Set up monitoring service to ping `/api/health`

## Update Frontend

After backend is deployed, update your Vercel environment variable:

```
REACT_APP_BACKEND_URL=https://your-backend.onrender.com
```

Then redeploy frontend on Vercel.

## Cost Estimate

- **Free Tier**: $0/month (750 hours, spins down)
- **Starter**: $7/month (always on, 512MB RAM)
- **Standard**: $25/month (2GB RAM, better for larger models)

## Next Steps

1. ✅ Deploy backend to Render with provided settings
2. ✅ Test health endpoint
3. ✅ Test transcription with small audio file
4. ✅ Update Vercel environment variable
5. ✅ Redeploy frontend
6. ✅ Test full application flow

## Support

If deployment fails:
1. Check Render logs for specific error
2. Verify build command is exactly as provided
3. Ensure `backend/` folder has all required files
4. Try deleting service and recreating with exact settings

## Files Checklist

Ensure these files exist in `backend/` folder:

- [x] requirements.txt (with setuptools at top)
- [x] app.py (with CORS and health endpoint)
- [x] Procfile (for Render)
- [x] All Python modules (transcribe_whisper.py, etc.)
