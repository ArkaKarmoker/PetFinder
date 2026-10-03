# 🐾 PetFinder — Pet Adoption & Rescue Platform

A comprehensive full-stack web application built with **Django** and **Django REST Framework (DRF)** designed to connect rescued animals with loving families.

---

## 🚀 Key Highlights & Architectural Overview

The project is structured according to clean architecture principles with both a **Bootstrap 5 responsive template frontend** and a **robust REST API** with **JWT authentication**:

1. **Django Project Settings Directory:** Named `core` (`core/settings.py`, `core/urls.py`, `core/wsgi.py`, `core/asgi.py`).
2. **Virtual Environment Isolated:** Runs strictly within a dedicated Python virtual environment (`venv`).
3. **Environment Security:** Sensitive variables (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`) are loaded via `python-dotenv` from `.env`, with a provided `.env.sample` template.
4. **Preserved Django Integrity:** All auto-generated files and standard Django comments are retained intact without modification.
5. **Modern Mobile-Responsive UI:** Built using Bootstrap 5.3, Bootstrap Icons, responsive cards, modals, and flexible layouts optimized for mobile, tablet, and desktop screens.
6. **JWT Authentication:** SimpleJWT tokens for REST APIs (`/api/auth/token/`, `/api/auth/token/refresh/`, `/api/auth/register/`, `/api/auth/profile/`).
7. **Database Seeding:** Includes both a custom Django management command (`python manage.py seed_db`) and a standalone script (`python seed_data.py`).
8. **Automated Testing:** 20 unit and integration tests covering models, business logic rules, template views, and REST API endpoints.

---

## 📋 Features & Functionalities

### 1. 👤 User Features & Authentication
- **User Registration & Login:** Session-based authentication for web templates and JWT for REST APIs.
- **User Profile Management:** View and edit personal profile information.
- **User Dashboard:** Dedicated portal to view and monitor adoption applications with color-coded status badges (`Pending`, `Approved`, `Rejected`).
- **Favorite Pets (Bonus):** Users can save and track favorite pets with instantaneous bookmarking.

### 2. 🔍 Pet Browsing, Search & Filtering
- **Pet Catalog:** Displays name, photo, animal type, breed, age, gender, location, status, and description.
- **Multi-parameter Search & Filter:** Filter by pet name, animal type (Dog, Cat, Rabbit, Bird, Other), breed, gender, location, and adoption status.
- **Pagination:** Responsive pagination controls on web templates (6 pets per page) and PageNumberPagination on REST APIs (`/api/pets/?page=2`).

### 3. 🐾 Pet Details & Adoption Workflow
- Dedicated pet details page displaying all attributes, health notes, and application status.
- If a pet is already adopted, an alert banner is displayed: `❌ This pet has already been adopted` and application submission is disabled.
- Application form collecting address, phone, adoption reason, previous pet experience, and custom messages.

### 4. 🧠 Business Logic Enforcement
- **Rule 1 — Only available pets can be adopted:** Users cannot submit applications for pets marked as `Adopted`.
- **Rule 2 — No duplicate active requests:** A user cannot submit multiple active (`Pending`) applications for the same pet.
- **Rule 3 — Auto Status Transition:** When an admin approves an adoption request (`Pending` &rarr; `Approved`), the pet's status automatically updates to `Adopted`, and other pending requests for that same pet are automatically rejected.

### 5. 🔧 Django Admin Panel
- Accessible at `/admin/`.
- Customized branding: `PetFinder Administration` portal.
- **Pet Management:** Filter by status, animal type, gender, location; search by name/breed/location; quick status editing; inline actions to mark pets as Available or Adopted.
- **Adoption Request Management:** List view showing applicant, pet, contact, experience, and status; search by username, email, phone; custom bulk actions to **Approve** and **Reject** applications adhering to business rules.

---

## 🌐 REST API Documentation

### Authentication Endpoints (JWT)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register/` | Register new user and receive JWT access/refresh tokens |
| `POST` | `/api/auth/token/` | Obtain JWT token pair (login) |
| `POST` | `/api/auth/token/refresh/` | Refresh access token |
| `GET/PUT` | `/api/auth/profile/` | View / update authenticated user profile |

### Pet Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/pets/` | List all pets (supports `?search=`, `?animal_type=`, `?gender=`, `?location=`, `?status=`, `?page=`) |
| `GET` | `/api/pets/<id>/` | Retrieve specific pet details |
| `POST` | `/api/pets/` | Add a new pet (Admin / Staff) |
| `PUT/PATCH` | `/api/pets/<id>/` | Update pet details (Admin / Staff) |
| `DELETE` | `/api/pets/<id>/` | Remove pet (Admin / Staff) |

### Adoption Request Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/adoptions/` | List adoption requests (users see only their own requests; staff see all) |
| `POST` | `/api/adoptions/` | Submit a new adoption request (validates Rules 1 & 2) |
| `GET` | `/api/adoptions/<id>/` | Retrieve adoption request details (owner or staff only) |
| `PUT/PATCH` | `/api/adoptions/<id>/` | Update request or status |

### Favorites Endpoints (Bonus)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/favorites/` | List user's saved favorite pets |
| `POST` | `/api/favorites/` | Save a pet to favorites |
| `DELETE` | `/api/favorites/<id>/` | Remove pet from favorites |

---

## 🔑 Demo Login Credentials

| Role | Username | Password | Email |
|---|---|---|---|
| **Admin / Superuser** | `admin` | `admin123` | `admin@petfinder.local` |
| **User (Rahim)** | `rahim` | `rahim123` | `rahim@example.com` |
| **User (Sarah)** | `sarah` | `sarah123` | `sarah@example.com` |
| **User (Karim)** | `karim` | `karim123` | `karim@example.com` |

---

## 💻 Installation & Setup Guide

### 1. Prerequisites
- Python 3.10+ installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/ArkaKarmoker/PetFinder.git
cd PetFinder
```

### 3. Create & Activate Virtual Environment
On Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables
Copy `.env.sample` to `.env`:
```bash
cp .env.sample .env
```
*(Default values in `.env` are pre-configured for local development)*

### 6. Run Database Migrations
```bash
python manage.py migrate
```

### 7. Seed Demo Data
You can populate the database with demo pets, users, requests, and sample images using either:
```bash
python manage.py seed_db
```
or
```bash
python seed_data.py
```

### 8. Run the Development Server
```bash
python manage.py runserver
```
Visit the website at: **http://127.0.0.1:8000/**  
Visit the Django Admin at: **http://127.0.0.1:8000/admin/**

---

## 🧪 Running Automated Tests

Run the complete test suite:
```bash
python manage.py test
```
All 20 test cases will execute and verify model integrity, business rules, template views, and DRF JWT API endpoints.

---

## 📦 Project Structure

```text
PetFinder/
├── core/                           # Django project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Configured with .env, DRF, JWT, Static/Media
│   ├── urls.py                     # Main project URL routing
│   └── wsgi.py
├── pets/                           # Pets & Adoption App
│   ├── management/
│   │   └── commands/
│   │       └── seed_db.py          # Custom management command: python manage.py seed_db
│   ├── migrations/                 # Database migrations
│   ├── admin.py                    # Custom Django Admin configuration
│   ├── api_urls.py                 # REST API URL patterns
│   ├── api_views.py                # DRF views (JWT Auth, Pets, Adoptions, Favorites)
│   ├── forms.py                    # Bootstrap-styled Django Forms
│   ├── models.py                   # Pet, AdoptionRequest, Favorite models with logic
│   ├── seed.py                     # Reusable DB seeder logic
│   ├── serializers.py              # DRF Serializers with validation
│   ├── tests.py                    # 20 automated tests
│   ├── urls.py                     # Web template URL patterns
│   └── views.py                    # Web template views
├── static/
│   └── css/
│       └── style.css               # Responsive design & custom aesthetics
├── templates/
│   ├── base.html                   # Base layout with responsive Bootstrap navbar
│   └── pets/
│       ├── home.html               # Homepage with categories, stats & featured pets
│       ├── pet_list.html           # Browse & filter page with pagination
│       ├── pet_detail.html         # Pet details with adoption CTA
│       ├── adoption_form.html      # Adoption application submission form
│       ├── dashboard.html          # User dashboard for applications & favorites
│       ├── profile.html            # User profile edit page
│       ├── login.html              # Responsive login page
│       └── register.html           # Responsive registration page
├── media/                          # Uploaded and generated pet photos
├── .env                            # Sensitive environment variables (ignored in git)
├── .env.sample                     # Sample environment variable template
├── requirements.txt                # Pinned dependencies
├── seed_data.py                    # Standalone seed script: python seed_data.py
├── manage.py
└── README.md                       # Documentation
```
