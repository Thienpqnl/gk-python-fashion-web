# Django backend (skeleton) for fashion-ecom-mock

This folder contains a minimal Django project `fashion_backend` and an app `shop` with a simple `Product` model and fixtures.

Quick setup (Windows PowerShell):

```powershell
# create venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# apply migrations
python manage.py migrate
# create superuser (optional)
python manage.py createsuperuser
# load sample products
python manage.py loaddata ..\fixtures\products.json
# run dev server
python manage.py runserver
```

Notes:
- Database: SQLite at `fashion_backend/db.sqlite3` by default.
- Fixtures placed in `backend/fixtures/products.json` (load with loaddata as shown).
- This is a skeleton: templates and frontend integration are not wired into Django views — the goal is to provide a backend starting point and mock data.

Static files & Tailwind:
- The frontend `assets/` have been copied into `backend/static/` (images under `backend/static/images/`, JS under `backend/static/js/`). Django will serve these under `/static/` in development.
- A Tailwind config is available at `backend/tailwind.config.js` for building CSS against the backend templates and static JS.

Next steps you might want:
- Add serializers / REST API endpoints (DRF)
- Wire templates to use the existing static HTML in project root (or use backend templates under `backend/templates/`)
- Build Tailwind (optional): run Tailwind CLI from the `backend/` folder and output CSS into `backend/static/css/` then link it in templates.
