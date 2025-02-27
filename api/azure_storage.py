from storages.backends.azure_storage import AzureStorage
import os

class AzureMediaStorage(AzureStorage):
    account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
    account_key = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
    azure_container = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
    expiration_secs = None  # Optional: disables URL expiry