import argparse, os
from ciscoisesdk import IdentityServicesEngineAPI

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Change Cisco ISE internal user's password by username")
    parser.add_argument("username", help="The ISE internal username to look up")
    # parser.add_argument("password", help="The new password for the user")
    args = parser.parse_args()

    target_username = args.username
    # new_password = args.password

    # Initialize API client (adjust credentials accordingly)
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

    # print("Printing ISE api request data", api, "\n")

    # Step 1: Search user by username using filter
    resp = api.internal_user.get_all(filter=f"name.EQ.{target_username}")
    users = resp.response.get('SearchResult', {}).get('resources', [])

    if not users:
        print(f"User '{target_username}' not found in internal users.")
        return

    user_id = users[0]['id']
    print(f"Found user '{target_username}' with ID: {user_id}")

#    print("checking methord availability for api",dir(api))
#    print("checking methord availability for api.internal_user",dir(api.internal_user))

    # Step 2: Change password for the user
    try:
        user_details = api.internal_user.get_by_id(id=user_id)
#        user_data_all = user_details.response
#        print(user_data_all)
        user_data = user_details.response['InternalUser']

        print(user_data)
        print("\nBelow is the user data:-")
        print("Username:", user_data.get('name', 'N/A'))
        print("enabled:", user_data.get('enabled', 'N/A'))
        print("First Name:", user_data.get('firstName', 'N/A'))
        print("Last Name:", user_data.get('lastName', 'N/A'))
        print("Email:", user_data.get('email', 'N/A'))
        print("Description:", user_data.get('description', 'N/A'))
        print("Date Modified:", user_data.get('dateModified', 'N/A'))
        print("ExpirtyDateEnabled:", user_data.get('expiryDateEnabled', 'N/A'))
        print("Expiry Date:", user_data.get('expiryDate', 'Not Set'))

        print("Do you want to change the password for this user? (yes/no)")
        confirmation = input().strip().lower()
        if confirmation != 'yes':
            print("Password change aborted.")
            return
        new_password = input("Enter the new password: ").strip()
        if not new_password:
            print("Password cannot be empty. Aborting.")
            return
        # Update user data with new password
        print(f"Changing password for user '{target_username}'...")
        user_data['password'] = new_password
        # user_data['name'] = target_username
        user_data['enabled'] = True
        user_data.pop('link', None)
        user_data.pop('dateModified', None)

        payload = {
                "InternalUser": user_data
                }
        print(f"Name before sending: '{payload['InternalUser']['name']}'")

        #update_resp = api.internal_user.update_internal_user_by_id(
        #update_resp = api.internal_user.get_internal_user_by_id(
        update_resp = api.internal_user.update_by_id(
            id=user_id,
            #internal_user=payload
            payload=payload
        )
        print(update_resp.response)  # See what ISE returns

        #print("getting internal user details from ID",update_resp.response)
        #if update_resp.status_code == 204:
        if update_resp.status_code in [200, 204]:
            print(f"Password changed successfully for user '{target_username}'.")
        else:
            print(f"Failed to change password. Response code: {update_resp.status_code}")
    except Exception as e:
        print(f"Error changing password: {str(e)}")

if __name__ == "__main__":
    main()
