# Google Geolocation API Setup Guide

To use Google's accurate geolocation services in your bot, you need to set up a Google Cloud Project and enable the Geolocation API.

## Steps to set up Google Geolocation API:

1. **Go to Google Cloud Console**:
   - Visit https://console.cloud.google.com/
   - Create a new project or select an existing one

2. **Enable the Geolocation API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Geolocation API"
   - Click on "Geolocation API" and press "Enable"

3. **Create an API Key**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key

4. **Set up the API key in your environment**:
   - On Windows: `set GOOGLE_API_KEY=your_api_key_here`
   - On Linux/Mac: `export GOOGLE_API_KEY=your_api_key_here`
   - Or add it to your system environment variables

5. **Restrict the API key (recommended for security)**:
   - In the Credentials page, click on your API key
   - Under "Application restrictions", select "HTTP referrers" or "IP addresses" 
   - Add your server's IP address if possible
   - Under "API restrictions", select "Restrict key" and choose "Geolocation API"

## Important Notes:

- The Geolocation API is not free - check current pricing at https://cloud.google.com/maps-platform/pricing/
- The bot will fall back to other geolocation services if the Google API key is not configured or fails
- Make sure to keep your API key secure and never share it publicly

## Usage in the Bot:

Once configured, the bot will automatically use Google's Geolocation API first (if available) and fall back to other services if needed. The `/geolocate` command will provide more accurate location information when the Google API is properly configured.