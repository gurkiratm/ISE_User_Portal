# ISE_User_Portal

For ISE internal users to view account details and update their own password.

## Overview

Small Python/Flask web application that provides a simple web UI for internal ISE users to view account details and change passwords. The app uses the Cisco ISE SDK (`ciscoisesdk`) to call Identity Services Engine APIs, stores portal users in a local SQLite DB, and includes Docker support for containerized deployment.

## Working snapshots

***Login Page***

<img width="829" height="400" alt="{04521439-84B6-480B-AC7C-AF3FFBAA8B61}" src="https://github.com/user-attachments/assets/9e2dda65-9eed-4288-92de-9dca7bd31508" />

***Main Page***

<img width="1351" height="602" alt="image" src="https://github.com/user-attachments/assets/48e12d42-13fd-42a4-ad10-7ac50c2b60f9" />

***Add and remove user pages***

<img width="436" height="329" alt="{04F8A12B-D24D-4F91-95DA-B0A5B2EB32CC}" src="https://github.com/user-attachments/assets/cc78df56-450a-4fb5-aba5-73e3213c77c6" />
<img width="881" height="150" alt="{9ABE16F2-88AE-432B-BC1E-1EBC4DBDE202}" src="https://github.com/user-attachments/assets/c78e13be-4138-43d5-ba6c-98828b942585" />

---
## Key details 

- App framework: Flask
- Auth / SDK: `ciscoisesdk`
- DB: SQLite stored at `instance/portal_users.db`
- Default app port (Docker / entrypoint): `5001`
- App entrypoint: `ISE_user_portal.py`
- Docker configuration: `Dockerfile`, `entrypoint.sh`
- Environment variables (used by the app):
  - `ADMIN_USER` — ISE API username (used by `IdentityServicesEngineAPI`)
  - `ADMIN_PASSWORD` — ISE API password
  - `BASE_URL` — ISE API base URL
- Requirements (from `requirements.txt`): `ciscoisesdk`, `Flask`, `Flask-BasicAuth`, `Flask-SQLAlchemy`, `dotenv`
- The container's `entrypoint.sh` will initialize the SQLite DB and add a default admin user (`gurkirat` / `gurkirat`) if the DB does not exist.

## Repository layout

- `ISE_user_portal.py` — main application
- `requirements.txt` — Python dependencies
- `templates/` — HTML templates for the UI
- `static/bootstrap/` — static assets
- `Dockerfile` — docker image build
- `entrypoint.sh` — container entrypoint and DB init
- `instance/portal_users.db` — (created at runtime) SQLite DB
- `Utility and supporting scripts` - (e.g., `01_get_specific_internal_user.py`, `get_all_internal_user.py`)
- `Notes.txt` — instructions for DB creation and troubleshooting
  
## Configuration

Before running, set the following environment variables:

- `ADMIN_USER` — Cisco ISE user
- `ADMIN_PASSWORD` — Cisco ISE password
- `BASE_URL` — Cisco ISE base URL (e.g. `https://ise.example.internal`)

Note: The app loads `.env` via `dotenv` if present. Prefer a `.env` file.

## Run with Docker

**Clone repo**
```
git clone https://github.com/gurkiratm/ISE_User_Portal.git
cd ISE_User_Portal
```
**Create .env or set environment variables:**
```
set ADMIN_USER=ise_api_user
set ADMIN_PASSWORD=ise_api_password
set BASE_URL=https://ise.example.internal
```
**Build the image:**
```
docker build -t ise_user_portal .
```
**Run (example):**
```
docker run --rm -p 5001:5001 \
  -e ADMIN_USER="ise_api_user" \  ##can skip if .env is created
  -e ADMIN_PASSWORD="ise_password" \ ##can skip if .env is create
  -e BASE_URL="https://ise.example.internal" \ ##can skip if .env is created
  ise_user_portal
```
