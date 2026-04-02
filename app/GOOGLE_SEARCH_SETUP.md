# Google Custom Search API Setup Guide

This guide will help you integrate Google Custom Search API as a tool for your AI tutoring agent.

## Why Use Google Search?

The AI agent can use Google Search to:
- Look up specific math theorems and proofs
- Find worked examples of problems
- Verify formulas and mathematical concepts
- Access current educational resources
- Search for specific problem-solving techniques

## Setup Steps

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Give it a name (e.g., "MathHelper Search")
4. Click "Create"

### 2. Enable Custom Search API

1. In the Google Cloud Console, go to **APIs & Services** → **Library**
2. Search for "Custom Search API"
3. Click on it and press **Enable**

### 3. Create API Key

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **API Key**
3. Copy your API key (it will look like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)
4. (Optional but recommended) Click **Restrict Key**:
   - Under "API restrictions", select "Restrict key"
   - Choose "Custom Search API"
   - Click "Save"

### 4. Create Custom Search Engine

1. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. Click **Add** (or "Get started")
3. Configure your search engine:
   - **Search engine name**: MathHelper Search
   - **What to search**: Select "Search the entire web"
   - Or enter `*` in "Sites to search" to search entire web
4. Click **Create**
5. On the next page, click **Customize**
6. Find your **Search Engine ID** (also called CX)
   - It looks like: `1234567890abcdef:xxxxxxx`
7. Copy this ID

### 5. Update Your .env File

Add your credentials to `app/.env`:

```bash
# ── Google Custom Search ─────────────────────────────
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
GOOGLE_SEARCH_ENGINE_ID=1234567890abcdef:xxxxxxx
```

**Replace** the placeholder values with your actual:
- API Key from step 3
- Search Engine ID from step 4

### 6. Install Dependencies

Install the Google API Python client:

```bash
cd app
pip install -r requirements.txt
```

Or install just the Google package:

```bash
pip install google-api-python-client>=2.100.0
```

### 7. Test the Integration

Restart your backend server:

```bash
cd app
python main.py
```

The agent will now be able to use the `math_web_search` tool powered by Google!

## How the Agent Uses It

When you ask the AI tutor a question, it can automatically decide to use Google Search:

**Example queries that might trigger search:**
- "What's the proof of the Pythagorean theorem?"
- "Show me examples of integration by parts"
- "What are trigonometric identities?"
- "How do you derive the quadratic formula?"

The agent will:
1. Recognize it needs external information
2. Call the `math_web_search` tool
3. Get results from Google
4. Use those results to formulate a better answer

## Search Result Format

The tool returns:
```json
{
  "query": "proof of Pythagorean theorem",
  "results": [
    {
      "title": "Pythagorean theorem - Wikipedia",
      "snippet": "In mathematics, the Pythagorean theorem...",
      "link": "https://en.wikipedia.org/wiki/Pythagorean_theorem",
      "displayLink": "en.wikipedia.org"
    }
  ],
  "total_results": 1240000,
  "error": null
}
```

## Pricing & Quotas

**Google Custom Search API Pricing:**
- **Free tier**: 100 queries per day
- **Paid tier**: $5 per 1,000 queries (after free tier)

**To increase quota:**
1. Go to Google Cloud Console → **APIs & Services** → **Enabled APIs**
2. Click on **Custom Search API**
3. Click **Quotas & System Limits**
4. Request a quota increase if needed

## Troubleshooting

### Error: "Google Search not configured"
- Make sure `GOOGLE_API_KEY` and `GOOGLE_SEARCH_ENGINE_ID` are set in `.env`
- Restart the backend server after updating `.env`

### Error: "API key not valid"
- Double-check your API key in Google Cloud Console
- Make sure Custom Search API is enabled
- Verify API key restrictions allow Custom Search API

### Error: "Invalid search engine ID"
- Verify your Search Engine ID in Programmable Search Engine
- Make sure it's the full ID including the `:` character

### No search results
- Check that your search engine is set to "Search the entire web"
- Try searching manually at https://programmablesearchengine.google.com/

## Alternative: Keep OpenAI Search

If you prefer to keep using OpenAI's built-in search instead of Google:
1. Don't add the Google credentials to `.env`
2. Revert `app/tools/math/web_search.py` to use OpenAI's search
3. The agent will fall back gracefully

## Security Notes

⚠️ **Never commit your .env file to git!**
- Your `.gitignore` should include `.env`
- Keep API keys secret
- Rotate keys if accidentally exposed

## Next Steps

Once configured, the agent will automatically use Google Search when appropriate. You can monitor usage in:
- Google Cloud Console → APIs & Services → Dashboard
- View query counts and errors
