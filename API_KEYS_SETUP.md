# API Keys Setup

## Important: Do NOT commit your API keys to GitHub!

This project requires two API keys:

1. **FRED API Key** (for economic data)
2. **Polygon.io API Key** (for intraday stock data)

## Setup Instructions

### 1. Copy the template file
```bash
cp config.py.template config.py
```

### 2. Get your FRED API Key
1. Go to https://fred.stlouisfed.org/docs/api/api_key.html
2. Create a free account
3. Request an API key
4. Copy your API key

### 3. Get your Polygon.io API Key
1. Go to https://polygon.io/
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy your API key

### 4. Update config.py
Open `config.py` and replace the placeholder values:

```python
FRED_API_KEY = 'your_actual_fred_api_key_here'
POLYGON_API_KEY = 'your_actual_polygon_api_key_here'
```

## Security Notes

- `config.py` is in `.gitignore` and will NOT be committed to git
- `config.py.template` is the public template without real keys
- Never share your API keys publicly
- Never commit `config.py` with real keys

## If You Accidentally Committed Keys

If you accidentally committed your API keys:

1. **Immediately revoke them** at the API provider's website
2. Generate new API keys
3. Update your local `config.py` with new keys
4. Use `git filter-branch` or BFG Repo-Cleaner to remove keys from git history (advanced)

## Environment Variables (Alternative)

Instead of using config.py, you can set environment variables:

```bash
export FRED_API_KEY='your_key_here'
export POLYGON_API_KEY='your_key_here'
```

Then update the code to read from environment variables:
```python
import os
FRED_API_KEY = os.environ.get('FRED_API_KEY', 'your_api_key_here')
POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY', 'your_api_key_here')
```
