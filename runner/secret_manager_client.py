import os
from google.cloud import secretmanager
from google.auth import default
from google.oauth2 import service_account
from kiteconnect import KiteConnect

def create_secret_manager_client():
    """
    Creates a Secret Manager Client.
    If running inside GCP, uses default credentials.
    If running locally, loads Service Account credentials from a file.
    """
    try:
        # Try using default credentials (GCP VM, Cloud Run, etc.)
        credentials, project = default()
        return secretmanager.SecretManagerServiceClient(credentials=credentials)
    except Exception:
        # Fallback to local development
        key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "./keys/autotrade.json")
        credentials = service_account.Credentials.from_service_account_file(key_path)
        return secretmanager.SecretManagerServiceClient(credentials=credentials)

def access_secret(secret_id, project_id):
    """
    Accesses the latest version of the specified secret from Secret Manager.
    """
    client = create_secret_manager_client()
    name = f"projects/autotrade-453303/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

def get_kite_client():
    api_key = access_secret("ZERODHA_API_KEY")
    access_token = access_secret("ZERODHA_ACCESS_TOKEN")

    kite = KiteConnect(api_key=api_key)
    kite.set_access_token(access_token)
    return kite
