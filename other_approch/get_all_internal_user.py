from ciscoisesdk import IdentityServicesEngineAPI
import json, os
from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
BASE_URL = os.getenv('BASE_URL')

api = IdentityServicesEngineAPI(
    username=ADMIN_USER,
    password=ADMIN_PASSWORD,
    base_url=BASE_URL,
    version="3.3_patch_1",
    verify=False
)
# List all internal users
print(json.dumps(api.internal_user.get_all().response, indent=2))
# Example: Get all network devices
print(json.dumps(api.network_device.get_all().response, indent=2))

