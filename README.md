# Hotel Management System (MCA Cloud Computing & DevOps Project)

A complete, professional, production-style cloud-based Hotel Management and Front-Desk operations system built with **Python 3, Flask, PyMongo, MongoDB Atlas, Cloudinary, Bootstrap 5, and Chart.js**.

---

## 📌 Project Overview
This project models real-world hotel front-desk operations:
- **Staff Authentication & Role-Based Access Control (RBAC)**: Admin, Receptionist, and Manager permissions.
- **Room Inventory Management**: Single, Double, Deluxe, and Executive Suite tracking with live availability toggling (`available`, `booked`, `maintenance`).
- **Guest / Customer CRM**: Registration and Cloudinary secure ID proof document upload.
- **Double Booking Prevention**: Backend date-collision protection engine.
- **Check-In & Check-Out Workflow**: Live room status syncing and food/room service charge entry.
- **Automated Billing Engine**: Stay duration calculation, itemized food charges, strict **18% GST** tax computation, and printable Tax Invoices.
- **Analytics Dashboard**: 10 statistical counter cards and 5 dynamic Chart.js visualizations (Occupancy Doughnut, Revenue Bar, Booking Status, and Category distribution).
- **Cloud Media Management**: Cloudinary API integration for customer ID proofs, room photographs, and staff profile pictures (with automatic offline local storage fallback).

---

## 🛠️ Technology Stack

| Domain | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3, Flask 3.0 |
| **Authentication & Security** | Flask-Login, Flask-Bcrypt, Flask-WTF (CSRF) |
| **Database** | MongoDB, PyMongo (Atlas Cloud & Local supported) |
| **Cloud Storage** | Cloudinary API (with local fallback) |
| **Frontend Styling** | HTML5, CSS3, Bootstrap 5.3, FontAwesome 6 |
| **Analytics & Data Viz** | Chart.js 4.4 |
| **Template Engine** | Jinja2 |
| **Testing** | pytest, mongomock |

---

## 📁 Architecture & Directory Structure

```text
c:/Users/RAHUL/Desktop/Hotal Management System/
│
├── app.py                      # Flask App Entry Point & Factory
├── config.py                   # Environment Configuration Class
├── requirements.txt            # Python Dependencies
├── seed.py                     # Database Seeder & Admin Creator
├── .env.example                # Template for Environment Variables
├── .env                        # Local Environment Config (git-ignored)
├── .gitignore                  # Git Ignore Rules
├── README.md                   # Documentation
│
├── database/                   # Database Layer
│   ├── __init__.py
│   └── db.py                   # PyMongo Atlas connection & Indexing
│
├── models/                     # Data Access Models (MongoDB Collections)
│   ├── __init__.py
│   ├── user_model.py           # User & Auth Model
│   ├── customer_model.py       # Guests Collection
│   ├── room_model.py           # Rooms Inventory Collection
│   ├── booking_model.py        # Reservations & Stays Collection
│   └── staff_model.py          # Staff Employee Collection
│
├── services/                   # Core Business Logic Services
│   ├── __init__.py
│   ├── cloudinary_service.py   # Cloudinary Media Upload Service
│   ├── booking_service.py      # Double-Booking Prevention & Workflows
│   └── billing_service.py      # GST Tax & Bill Calculation Engine
│
├── utils/                      # Helper Functions & Decorators
│   ├── __init__.py
│   ├── helper.py               # Currency & Date Formatters
│   ├── validators.py           # RegEx & Date Range Validators
│   └── decorators.py           # Role-Based Access Control (@roles_required)
│
├── forms/                      # WTForms Specifications
│   ├── __init__.py
│   ├── auth_forms.py
│   ├── customer_forms.py
│   ├── room_forms.py
│   ├── booking_forms.py
│   └── staff_forms.py
│
├── routes/                     # Blueprint Controllers / Routes
│   ├── __init__.py
│   ├── auth.py                 # Login, Logout, Account creation
│   ├── dashboard.py            # Analytics & Chart.js API
│   ├── customer.py             # Guest CRUD & ID upload
│   ├── room.py                 # Room CRUD & Status management
│   ├── booking.py              # Booking, Check-In, Check-Out
│   ├── billing.py              # Invoices & Printing
│   └── staff.py                # Admin Staff CRUD
│
├── templates/                  # Jinja2 HTML Views
│   ├── layout.html             # Master Template with Responsive Sidebar
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── dashboard.html          # Metric Cards & Chart Canvas Elements
│   ├── customers/ (list, add, edit, details)
│   ├── rooms/ (list, add, edit, details)
│   ├── bookings/ (list, add, details, checkout)
│   ├── billing/ (list, invoice)
│   ├── staff/ (list, add, edit, details)
│   └── errors/ (403, 404, 500)
│
├── static/                     # Static Web Assets
│   ├── css/
│   │   └── style.css           # Glassmorphism & Responsive CSS
│   └── js/
│       └── script.js           # Chart.js Initializers & Live Calculators
│
└── tests/                      # Automated Test Suite
    ├── test_auth.py
    ├── test_billing.py
    ├── test_booking.py
    └── test_customer.py
```

---

## ☁️ Cloud Computing & DevOps Concepts Demonstrated

1. **MongoDB Atlas (Database as a Service - DBaaS)**:
   - Provides fully managed cloud database deployment with high availability, automated backups, and global distribution.
2. **Cloudinary (Software as a Service - SaaS / Media Storage)**:
   - Offloads file uploads (ID proofs, photos) to Cloudinary CDN, keeping the local application stateless and cloud-deployable.
3. **Twelve-Factor App Configuration**:
   - Uses `.env` and environment variables for sensitive credentials (`SECRET_KEY`, `MONGO_URI`, `CLOUDINARY_*`), ensuring zero hardcoded secrets in source code.
4. **DevOps Continuous Delivery Readiness**:
   - Clean modular architecture, unit tests via `pytest`, reproducible `requirements.txt`, and Git VCS readiness.

---

## 🔑 Default Login Credentials

After executing `python seed.py`, login with:

| Role | Username / Email | Password | Allowed Permissions |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@hotel.com` | `Admin@123` | Full access (Users, Staff, Rooms, Customers, Bookings, Billing, Analytics) |
| **Receptionist** | `receptionist@hotel.com` | `Receip@123` | Customers, Bookings, Check-In, Check-Out, Billing |
| **Manager** | `manager@hotel.com` | `Manager@123` | Analytics, Rooms, Customers, Bookings, Staff (View-only) |

---

## 🚀 Step-by-Step Installation & Running Guide

### 1. Clone or Open Project Folder
```bash
cd "c:/Users/RAHUL/Desktop/Hotal Management System"
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
.\venv\Scripts\activate.bat
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (`.env`)
Ensure `.env` exists with your MongoDB URI:
```env
SECRET_KEY=hotel_mca_cloud_devops_secret_key_2026
MONGO_URI=mongodb://127.0.0.1:27017/hotel_management
MONGO_DB_NAME=hotel_management
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```
*(For MongoDB Atlas, replace `MONGO_URI` with `mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority`)*

### 5. Seed Initial Database Records
```bash
python seed.py
```

### 6. Run Application Server
```bash
python app.py
```
Open your browser and navigate to: **http://127.0.0.1:5000**

---

## 🧪 Running Automated Tests
Run unit and functional test assertions using `pytest`:
```bash
pytest -v
```

---

## 🐳 Docker Deployment Instructions (DevOps Containerization)

### Option A: Using Docker Compose (Multi-Container Web + MongoDB)
Run the entire application stack (Flask web server + MongoDB database container) with a single command:

```bash
docker-compose up --build -d
```
- Open browser at **http://127.0.0.1:5000**
- To seed default data inside the Docker container:
  ```bash
  docker exec -it hotel_web_app python seed.py
  ```
- To stop the Docker containers:
  ```bash
  docker-compose down
  ```

### Option B: Building Single Docker Image
```bash
docker build -t hotel-management-system:latest .
docker run -d -p 5000:5000 --name hotel_app hotel-management-system:latest
```

---

## 🐙 Git & GitHub Commands

```bash
git init
git add .
git commit -m "Initial commit - Complete Cloud Hotel Management System"
# git remote add origin https://github.com/username/hotel-management-system.git
# git push -u origin main
```
