# 💰 Budget Tracker

A personal finance web app built with Django. Track your income and expenses, visualize spending by category, and manage separate accounts for multiple users.

---

## Features

- User authentication (sign up, log in, log out)
- Add and delete income and expense transactions
- Categorize transactions (Groceries, Rent, Salary, etc.)
- Dashboard with total income, total expenses, and current balance
- Doughnut chart showing spending breakdown by category
- Per-user data isolation — each account only sees its own transactions

---

## Tech Stack

- **Backend:** Python, Django 4.2
- **Frontend:** HTML, Bootstrap 5, Chart.js
- **Database:** SQLite (development)
- **Containerization:** Docker

---

## Project Structure

```
budgettingApp/
├── budgettracker/          # Project config
│   ├── settings.py
│   └── urls.py
├── tracker/                # Main app
│   ├── migrations/
│   ├── templates/
│   │   ├── registration/
│   │   │   ├── login.html
│   │   │   └── signup.html
│   │   └── tracker/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       └── add_transaction.html
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── dockerSettings/         # Docker configuration
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
├── manage.py
├── requirements.txt
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- Docker Desktop (optional, for containerized setup)

---

### Option 1: Run with Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/Meyer07/BudgetingApp.git
cd BudgetingApp
```

2. Make sure Docker Desktop is running, then build and start the app:
```bash
docker-compose -f dockerSettings/docker-compose.yml build
docker-compose -f dockerSettings/docker-compose.yml run web python manage.py migrate
docker-compose -f dockerSettings/docker-compose.yml up
```

3. Visit **http://127.0.0.1:8000** in your browser.

4. To create a superuser for admin access:
```bash
docker-compose -f dockerSettings/docker-compose.yml run web python manage.py createsuperuser
```

5. To stop the app:
```bash
docker-compose -f dockerSettings/docker-compose.yml down
```

---

### Option 2: Run Locally (Without Docker)

1. Clone the repository:
```bash
git clone https://github.com/Meyer07/BudgetingApp.git
cd BudgetingApp
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (for admin access):
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Visit **http://127.0.0.1:8000** in your browser.

---

## Seeding Categories

After setup, populate the database with default categories via the Django shell:

```bash
# Local
python manage.py shell

# Docker
docker-compose -f dockerSettings/docker-compose.yml run web python manage.py shell
```

Then paste:
```python
from tracker.models import Category

categories = [
    "Salary", "Freelance", "Investment", "Other Income",
    "Rent / Mortgage", "Utilities", "Groceries", "Transportation",
    "Healthcare", "Insurance", "Dining Out", "Entertainment",
    "Shopping", "Travel", "Subscriptions", "Emergency Fund", "Retirement"
]

for name in categories:
    Category.objects.get_or_create(name=name)

print("Done!")
```

Then type `exit()`.

---

## Usage

- **Sign up** at `/signup/` to create a new account
- **Log in** at `/accounts/login/`
- **Add transactions** using the "+ Add Transaction" button
- **View your dashboard** to see your balance and spending chart
- **Delete transactions** using the Delete button in the table
- **Admin panel** available at `/admin/` for superusers

---

## Future Improvements

- Monthly budget goals with progress bars
- Filter and search transactions by date or category
- Export transactions to CSV
- Recurring transaction support
- Mobile-friendly redesign