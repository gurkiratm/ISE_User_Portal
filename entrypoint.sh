#!/bin/sh

# If DB file does not exist, initialize it
# if [ ! -f /app/instance/portal_users.db ]; then
#     echo "Database not found. Initializing..."
#     python -c "from ISE_user_portal import app, db; \
#                with app.app_context(): db.create_all()"
# fi

mkdir -p /app/instance
chmod 777 /app/instance

if [ ! -f /app/instance/portal_users.db ]; then
    echo "Database not found. Initializing..."
    python -c "
from ISE_user_portal import app, db, PortalUser
with app.app_context():
    db.create_all()
    # Add default user
    from werkzeug.security import generate_password_hash
    admin = PortalUser(
        username='gurkirat',
        password=generate_password_hash('gurkirat'),
        ise_username='gurkirat'
    )
    db.session.add(admin)
    db.session.commit()
"
fi

# Start the app
# exec flask run --host=0.0.0.0 --port=5001
python3 /app/ISE_user_portal.py
