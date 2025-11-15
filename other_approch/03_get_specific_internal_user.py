from ciscoisesdk import IdentityServicesEngineAPI
import json, sys, argparse, os

parser = argparse.ArgumentParser(description="Get Cisco ISE internal user ID by username")
parser.add_argument("username", help="The ISE internal username to look up")
args = parser.parse_args()

target_username = args.username

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

resp = api.internal_user.get_all(filter=f"name.EQ.{target_username}")
users = resp.response.get('SearchResult', {}).get('resources', [])
if users:
    user_id = users[0]['id']
    print(f"{target_username} User ID is : {user_id}")
else:
    print("User not found.")

