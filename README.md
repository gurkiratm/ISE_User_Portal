
# ISE User Portal

A web-based portal for managing Cisco ISE internal users, built with Flask and SQLAlchemy. This portal allows users to log in, view their ISE details, change their ISE and portal passwords, and for admins to register or remove users.

## Features
- User authentication (login/logout)
- View Cisco ISE internal user details
- Change ISE password
- Change portal password (local database)
- Admin-only user registration and removal
- Flash messages for user feedback
- Responsive UI with Bootstrap and Bootstrap Icons

## Requirements
- Python 3.12+
- Flask
- Flask-SQLAlchemy
- ciscoisesdk
- python-dotenv
- werkzeug
- Bootstrap (included in `static/`)

## Setup
1. Clone the repository:
	```bash
	git clone https://github.com/<your-username>/ISE_User_Portal.git
	cd ISE_User_Portal
	```
2. Install dependencies:
	```bash
	pip install -r requirements.txt
	```
3. Set up the database:
	```python
	from ISE_user_portal import app, db, PortalUser
	with app.app_context():
		 db.create_all()
	```
4. Configure environment variables in a `.env` file (optional):
	- `ADMIN_USER`
	- `ADMIN_PASSWORD`
	- `BASE_URL`

## Running the App
You can run the app locally with:
```bash
python ISE_user_portal.py
```
Or using Docker:
```bash
sudo docker build -t ise_user_portal:v1 .
sudo docker run --rm -p 5001:5001 ise_user_portal:v1
```

## File Structure
- `ISE_user_portal.py` - Main Flask app
- `templates/` - HTML templates
- `static/` - Bootstrap CSS/JS and icons
- `instance/portal_users.db` - SQLite database
- `requirements.txt` - Python dependencies
- `Dockerfile` - For containerization

## Usage
- Users can log in and view their ISE details.
- Users can change their ISE password and portal password.
- Admins can register new users and remove existing users.

## License
MIT

## Author
Gurkirat Singh
