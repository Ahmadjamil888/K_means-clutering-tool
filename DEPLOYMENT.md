# 🚀 Deployment Guide

This guide covers multiple deployment options for the AI-Powered K-Means Clustering Tool.

## Quick Deploy Options

### 1. 🐳 Docker (Recommended for Local/Server)

**Prerequisites:** Docker installed

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t clustering-tool .
docker run -p 5000:5000 clustering-tool
```

Access at: `http://localhost:5000`

### 2. ☁️ Vercel (Free, Easy)

**Prerequisites:** Vercel account

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**Or use Vercel Dashboard:**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Deploy automatically

### 3. 🚂 Railway (Free Tier Available)

**Prerequisites:** Railway account

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

**Or use Railway Dashboard:**
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Deploy with one click

### 4. 🎨 Render (Free Tier Available)

**Prerequisites:** Render account

1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Choose "Web Service"
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

### 5. 💜 Heroku

**Prerequisites:** Heroku account and CLI

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-clustering-tool

# Deploy
git push heroku main
```

### 6. 🌐 PythonAnywhere

**Prerequisites:** PythonAnywhere account

1. Upload files to PythonAnywhere
2. Install requirements in console:
   ```bash
   pip3.9 install --user -r requirements.txt
   ```
3. Configure web app to use `app.py`

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

## Environment Variables

For production deployments, set these environment variables:

- `FLASK_ENV=production`
- `PORT=5000` (or your preferred port)

## File Storage Considerations

**Important:** Most cloud platforms have ephemeral file systems. Uploaded files and generated plots may not persist between deployments.

**Solutions:**
- Use cloud storage (AWS S3, Google Cloud Storage)
- Store files in memory for temporary processing
- Use database for persistent storage

## Performance Tips

1. **Memory Usage:** Large datasets may hit memory limits on free tiers
2. **Processing Time:** Complex clustering may timeout on some platforms
3. **File Size:** Limit CSV uploads to reasonable sizes (< 10MB)

## Troubleshooting

### Common Issues:

**Port Binding Error:**
- Ensure app binds to `0.0.0.0` and uses `PORT` environment variable

**Memory Errors:**
- Reduce dataset size or upgrade to paid tier

**Module Import Errors:**
- Check `requirements.txt` includes all dependencies
- Verify Python version compatibility

**File Upload Issues:**
- Check upload directory permissions
- Verify file size limits

## Security Considerations

For production use:
- Add file type validation
- Implement rate limiting
- Add user authentication if needed
- Sanitize file uploads
- Set proper CORS headers

## Monitoring

Add these for production monitoring:
- Error logging
- Performance metrics
- Health check endpoints
- User analytics

## Cost Estimates

**Free Tiers:**
- Vercel: Good for light usage
- Railway: 500 hours/month free
- Render: 750 hours/month free
- Heroku: 550-1000 hours/month free

**Paid Options:**
- Start around $5-10/month for basic hosting
- Scale based on usage and performance needs

Choose the deployment option that best fits your needs and technical comfort level!