from ciscoisesdk import IdentityServicesEngineAPI
import json, sys, os

if len(sys.argv) < 2:
    print("Usage: python3 get_specific_internal_user.py <username>")
    sys.exit(1)

target_username = sys.argv[1]

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

#users = api.internal_user.get_all().response['SearchResult']['resources']
#print("Usernames found in ISE:")
#for user in users:
#    print(" -", user['name'])

target_username = sys.argv[1]

resp = api.internal_user.get_all(filter=f"name.EQ.{target_username}")
users = resp.response.get('SearchResult', {}).get('resources', [])
if users:
    user_id = users[0]['id']
    print(f"{target_username} User ID is : {user_id}")
else:
    print("User not found.")

