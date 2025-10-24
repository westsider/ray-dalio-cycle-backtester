# Deploying to Streamlit Community Cloud

This guide will help you deploy your Ray Dalio Economic Cycle Backtester to Streamlit Community Cloud for free.

## Prerequisites

- ✅ GitHub repository (you have this!)
- ✅ Streamlit app code (app.py)
- ✅ requirements.txt
- 🔑 Your API keys (FRED and Polygon.io)

## Step-by-Step Deployment

### 1. Sign Up for Streamlit Community Cloud

1. Go to https://share.streamlit.io/
2. Click "Sign up" or "Continue with GitHub"
3. Authorize Streamlit to access your GitHub account

### 2. Create a New App

1. Click the **"New app"** button
2. Fill in the deployment form:
   - **Repository**: `westsider/ray-dalio-cycle-backtester`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Click **"Advanced settings"** (very important!)

### 3. Configure Secrets (CRITICAL!)

In the "Secrets" section, add your API keys in TOML format:

```toml
# .streamlit/secrets.toml format
FRED_API_KEY = "your_fred_api_key_here"
POLYGON_API_KEY = "your_polygon_api_key_here"
```

**Replace the placeholder values with your actual API keys!**

### 4. Deploy

1. Click **"Deploy!"**
2. Wait 2-5 minutes for the app to build and deploy
3. Your app will be live at: `https://share.streamlit.io/westsider/ray-dalio-cycle-backtester/main/app.py`

## How Secrets Work

The app is configured to:
1. **First**: Try to read from Streamlit secrets (for cloud deployment)
2. **Fallback**: Use environment variables or local config.py (for local development)

This means:
- ✅ **Local development**: Works as before (uses config.py)
- ✅ **Streamlit Cloud**: Uses secrets you configure in the dashboard
- ✅ **Secure**: API keys are never exposed in your code

## Managing Your Deployed App

### Update Your App
Any push to the `main` branch will automatically redeploy your app!

### View Logs
Click on your app in the Streamlit dashboard → "Manage app" → "Logs"

### Update Secrets
Streamlit dashboard → Your app → "⋮" menu → "Settings" → "Secrets"

### Reboot App
If something goes wrong: "⋮" menu → "Reboot app"

## Free Tier Limits

Streamlit Community Cloud free tier includes:
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ Share with unlimited viewers
- ⚠️ App goes to sleep after inactivity (wakes up when accessed)

## Troubleshooting

### App Won't Start
- Check logs for errors
- Verify secrets are set correctly
- Make sure requirements.txt has all dependencies

### API Errors
- Double-check your API keys in secrets
- Verify keys are valid at fred.stlouisfed.org and polygon.io

### Out of Memory
- Reduce backtest period
- Clear cache: Add `?clear_cache=true` to URL

### App is Slow
- Free tier apps sleep after inactivity
- First load after sleep takes ~30 seconds
- Consider upgrading to paid tier for always-on apps

## Privacy Considerations

⚠️ **Important**:
- Your app will be **publicly accessible** by default
- Anyone with the URL can use your app
- Your API usage counts against YOUR API limits
- Consider setting up authentication if needed

### Limiting Access

To make your app private (paid feature):
1. Upgrade to Streamlit Teams ($250/month for teams)
2. Or: Add password protection in your code
3. Or: Use IP whitelisting

## Cost Considerations

**Free Tier:**
- ✅ Hosting: Free
- ⚠️ FRED API: Free (500 requests/day)
- ⚠️ Polygon.io: Free tier has rate limits

**If you get popular:**
- Monitor your API usage
- May need to upgrade Polygon.io to paid tier
- FRED is generally sufficient for most use cases

## Alternative Deployment Options

If Streamlit Cloud doesn't work for you:

1. **Heroku** (free tier available)
2. **Railway.app** (free tier available)
3. **Render** (free tier available)
4. **AWS EC2** (pay-as-you-go)
5. **DigitalOcean** ($5/month droplet)

## Questions?

- Streamlit docs: https://docs.streamlit.io/streamlit-community-cloud
- Streamlit forum: https://discuss.streamlit.io/
- GitHub issues: https://github.com/westsider/ray-dalio-cycle-backtester/issues
