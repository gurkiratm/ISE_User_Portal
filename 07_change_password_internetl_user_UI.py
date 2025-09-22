import argparse
from ciscoisesdk import IdentityServicesEngineAPI
from flask import Flask, render_template, request, flash
from flask_basicauth import BasicAuth


app = Flask(__name__)
app.secret_key = "replace-with-a-random-secret-key"

app.config['BASIC_AUTH_USERNAME'] = 'gurkirat'     # <--- set your username here
app.config['BASIC_AUTH_PASSWORD'] = 'gurkirat'     # <--- set your password here
app.config['BASIC_AUTH_FORCE'] = True              # <--- protects ALL routes by default

basic_auth = BasicAuth(app)

def change_user_password(target_username, new_password):
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
   # Find user by username
    resp = api.internal_user.get_all(filter=f"name.EQ.{target_username}")
    users = resp.response.get('SearchResult', {}).get('resources', [])
    if not users:
        print(f"User '{target_username}' not found in internal users.")
        return
    user_id = users[0]['id']
#    print(f"Found user '{target_username}' with ID: {user_id}")
    #print("checking availability",dir(api.internal_user))
    # Step 2: Change password for the user
#    try:
    user_details = api.internal_user.get_by_id(id=user_id)
#        user_data_all = user_details.response
#        print(user_data_all)
    user_data = user_details.response['InternalUser']

#        print(user_data)

    user_data['password'] = new_password
    user_data['name'] = target_username
    user_data['enabled'] = True
    user_data.pop('link', None)
    user_data.pop('dateModified', None)

    payload = {"InternalUser": user_data}
#        print(payload)
#        print(f"Name before sending: '{payload['InternalUser']['name']}'")
    update_resp = api.internal_user.update_by_id(id=user_id, payload=payload)
#        print("getting internal user details from ID",update_resp.response)
    if update_resp.status_code in [200, 204]:
        return f"Password for '{target_username}' updated successfully!", True
    else:
        return f"Failed to update password. {update_resp.response}", False
 #   except Exception as e:
 #       print(f"Error changing password: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
#@basic_auth.required
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash("Please provide both username and new password.", "danger")
        else:
            message, success = change_user_password(username, password)
            flash(message, "success" if success else "danger")
    return render_template('form.html')

if __name__ == '__main__':
#    app.run(debug=True)
    app.run(host='0.0.0.0', port=5002, debug=True)
