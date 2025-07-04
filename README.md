# Django Expense Tracker API

A RESTful API for personal expense/income tracking with JWT-based authentication and user-level data access control. Built using **Django** and **Django REST Framework**.

## Features

- JWT Authentication (register, login, token refresh)
- Role-based access: Regular users & superusers
- Expense and income tracking
- Automatic tax calculations (flat or percentage)
- Paginated API responses
- Full CRUD operations
- Permissions to ensure data privacy

---

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Authentication:** djangorestframework-simplejwt (JWT)
- **Database:** SQLite (development)
- **Language:** Python 

---

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Sudhir4500/Expense_Tracker_API.git
   cd expense-tracker-api

2. **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate # On Windows
    source env/bin/activate # on linux

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Apply Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate

5. **Create Superuser**
    ```bash
    python manage.py createsuperuser
6. **Run the Server:**
    ```bash
    python manage.py runserver

---

# API Documentation
## Authentication Endpoints
| Method | Endpoint              | Description            |
| ------ | --------------------- | ---------------------- |
| POST   | `/api/auth/register/` | Register new user      |
| POST   | `/api/auth/login/`    | Login & get JWT tokens |
| POST   | `/api/auth/refresh/`  | Refresh access token   |

# Expense/Income Endpoints
| Method | Endpoint              | Description                     |
| ------ | --------------------- | ------------------------------- |
| GET    | `/api/expenses/`      | List user's records (paginated) |
| POST   | `/api/expenses/`      | Create a new record             |
| GET    | `/api/expenses/{id}/` | Retrieve a specific record      |
| PUT    | `/api/expenses/{id}/` | Update a specific record        |
| DELETE | `/api/expenses/{id}/` | Delete a specific record        |

# Tax Calculation Logic
## Flat Tax: total = amount + tax
## Percentage Tax: total = amount + (amount * tax / 100)

# Sample Responses
## Single Record
```bash
{
  "id": 1,
  "title": "Grocery Shopping",
  "description": "Weekly groceries",
  "amount": 100.00,
  "transaction_type": "debit",
  "tax": 10.00,
  "tax_type": "flat",
  "total": 110.00,
  "created_at": "2025-07-04T15:02:35.958606Z",
  "updated_at": "2025-07-04T15:02:35.958606Z"
}
```

# Paginated List
```bash
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Updated Grocery",
            "description": "Updated desc",
            "amount": "120.00",
            "transaction_type": "debit",
            "tax": "10.00",
            "tax_type": "percentage",
            "total": 132.0,
            "created_at": "2025-07-04T15:02:35.958606Z",
            "updated_at": "2025-07-04T15:02:35.958606Z"
        }
    ]
}
```



# Project Structure
# Below is the directory structure for the Django Expense Tracker API:
   ```bash
├── expenses/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── expense_tracker/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt

```
## License
This project is for educational purposes







