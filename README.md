# 🧾 Booking System – Ahoum Backend Assignment

A RESTful Flask API for booking sessions and retreats.  
Implements user auth, session booking, CRM notifications.

---

## ✅ Features

- JWT-based user authentication
- View list of events/sessions
- Book an event (auth required)
- CRM webhook notification
- View user bookings
- Input validation with Marshmallow

---

## 🛠 Tech Stack

- Python 3.10+
- Flask
- SQLite (dev)
- JWT (via `flask-jwt-extended`)
- Marshmallow (validation)
- Postman / Hoppscotch (testing)

---

## 🚀 Getting Started

### Clone repo & install dependencies
```bash
git clone https://github.com/vaishnavv04/Ahoum-Backend
cd booking-system
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate
pip install -r requirements.txt
