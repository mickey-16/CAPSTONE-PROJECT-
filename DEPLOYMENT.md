# Deploying to Streamlit Cloud

## Quick Deployment Steps

1. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Click "Sign up" or "Sign in" (use your GitHub account)

2. **Deploy Your App**
   - Click "New app"
   - Select your repository: `mickey-16/CAPSTONE-PROJECT-`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Wait for Deployment**
   - Streamlit Cloud will install dependencies and start your app
   - Takes 2-5 minutes
   - You'll get a URL like: `https://your-app-name.streamlit.app`

## Your App Will Be Live!

Once deployed, anyone can access your carbon footprint prediction website at the URL provided by Streamlit Cloud.

## Alternative Deployment Options

### Option 2: Heroku
1. Install Heroku CLI
2. Create `Procfile`: `web: streamlit run app.py --server.port=$PORT`
3. Create `setup.sh` for Streamlit config
4. Deploy: `heroku create` and `git push heroku main`

### Option 3: Railway
1. Sign up at https://railway.app
2. Connect your GitHub repository
3. Railway auto-detects Streamlit apps
4. Click deploy

### Option 4: Render
1. Sign up at https://render.com
2. Connect repository
3. Select "Web Service"
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run app.py --server.port $PORT`

## Recommended: Streamlit Cloud
- Free tier available
- Easiest deployment for Streamlit apps
- Automatic HTTPS
- No configuration needed
- Direct GitHub integration
