from kiteconnect import KiteConnect
import os
import urllib.parse

API_KEY = os.getenv("ZERODHA_API_KEY")
API_SECRET = os.getenv("ZERODHA_API_SECRET")

kite = KiteConnect(api_key=API_KEY)

print("🔗 Open this URL in browser and login to get request_token:")
print(kite.login_url())

# Accept full URL or just token
raw_input = input("\n📥 Paste full redirect URL or just request_token: ").strip()

# Try to parse the request_token from URL
if "request_token=" in raw_input:
    parsed = urllib.parse.urlparse(raw_input)
    request_token = urllib.parse.parse_qs(parsed.query).get("request_token", [""])[0]
else:
    request_token = raw_input

# Now generate the access_token
try:
    session = kite.generate_session(request_token, api_secret=API_SECRET)
    print(f"\n✅ Your ACCESS_TOKEN is:\n{session['access_token']}")
except Exception as e:
    print(f"❌ Error: {e}")
