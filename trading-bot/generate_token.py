from kiteconnect import KiteConnect
import os

API_KEY = os.getenv("ZERODHA_API_KEY")
API_SECRET = os.getenv("ZERODHA_API_SECRET")

kite = KiteConnect(api_key=API_KEY)

print("\n🔗 Visit this URL to login and authorize:")
print(kite.login_url())

request_url = input("\n📥 Paste the full redirected URL after login:\n")

# Extract request token from redirected URL
try:
    request_token = request_url.split("request_token=")[1].split("&")[0]
except Exception:
    print("❌ Invalid URL. Couldn't find request_token.")
    exit(1)

# Get access token
try:
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    access_token = data["access_token"]
    print(f"\n✅ Access Token: {access_token}")
except Exception as e:
    print(f"❌ Token generation failed: {e}")
    exit(1)

# Update ~/.bashrc
bashrc_path = os.path.expanduser("~/.bashrc")

with open(bashrc_path, "r") as f:
    lines = f.readlines()

with open(bashrc_path, "w") as f:
    updated = False
    for line in lines:
        if line.startswith("export ZERODHA_ACCESS_TOKEN="):
            f.write(f"export ZERODHA_ACCESS_TOKEN='{access_token}'\n")
            updated = True
        else:
            f.write(line)
    if not updated:
        f.write(f"export ZERODHA_ACCESS_TOKEN='{access_token}'\n")

print("🔄 Updated ~/.bashrc with new access token.")

# Apply the updated .bashrc (note: this won't reflect in the current Python process)
os.system("bash -c 'source ~/.bashrc'")

print("✅ Token updated and environment reloaded. Done.")
