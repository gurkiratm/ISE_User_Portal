import argparse, os
from ciscoisesdk import IdentityServicesEngineAPI
from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

ADMIN_USER = os.getenv('ADMIN_USER')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
BASE_URL = os.getenv('BASE_URL')

def main():
    parser = argparse.ArgumentParser(
        description="Change Cisco ISE internal user's password by username"
    )
    parser.add_argument(
        "--username",
        required=True,
        help="The ISE internal username to look up"
    )
    parser.add_argument(
        "--password",
        required=True,
        help="The new password for the user"
    )
    # (Optional) Add additional arguments for admin credentials or URL
    parser.add_argument(
        "--ise-host",
        default=BASE_URL,
        help="Base URL of the Cisco ISE server"
    )
    parser.add_argument(
        "--ise-admin",
        default=ADMIN_USER,
        help="ISE admin username"
    )
    parser.add_argument(
        "--ise-admin-pass",
        default=ADMIN_PASSWORD,
        help="ISE admin password"
    )
    parser.add_argument(
        "--ise-version",
        default="3.3_patch_1",
        help="Cisco ISE version"
    )
    parser.add_argument(
        "--verify-ssl",
        action="store_true",
        help="Verify SSL certificates"
    )

    args = parser.parse_args()

    # Initialize API client
    api = IdentityServicesEngineAPI(
        username=args.ise_admin,
        password=args.ise_admin_pass,
        base_url=args.ise_host,
        version=args.ise_version,
        verify=args.verify_ssl
    )

    target_username = args.username
    new_password = args.password

    # Search user by username
    resp = api.internal_user.get_all(filter=f"name.EQ.{args.username}")
    users = resp.response.get("SearchResult", {}).get("resources", [])

    if not users:
        print(f"User '{args.username}' not found in internal users.")
        return

    user_id = users[0]["id"]
    print(f"Found user '{args.username}' with ID: {user_id}")

    # Change password for the user
    try:
        user_details = api.internal_user.get_by_id(id=user_id)
        user_data = user_details.response['InternalUser']
        user_data['password'] = new_password
        user_data['name'] = target_username
        user_data['enabled'] = True
        user_data.pop('link', None) #not compulsory
        user_data.pop('dateModified', None)  #not compulsory

        updated_user_data = {
                "InternalUser": user_data
                }

        update_resp = api.internal_user.update_internal_user_by_id(
            id=user_id,
            payload=updated_user_data
        )
        if update_resp.status_code in [204, 200] :
            print(f"Password changed successfully for user '{args.username}'.")
        else:
            print(f"Failed to change password. Response code: {update_resp.status_code}")
            print(update_resp.response)
    except Exception as e:
        print(f"Error changing password: {str(e)}")

if __name__ == "__main__":
    main()
