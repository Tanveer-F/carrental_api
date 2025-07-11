# 🚗 1Now Car Rental — Backend API

This is a Django REST Framework-based backend API developed for a fictional car rental service — **LahoreCarRental.com**, a city-level partner of 1Now.
The system is designed with modular apps **(users, vehicles, bookings)** and supports full user authentication using **JWT**, 
which is configured globally through DRF settings. Authenticated users can securely manage their own cars and bookings via clean RESTful endpoints.

---

## 🔍 Project Highlights

- 🔐 JWT authentication (globally configured in `REST_FRAMEWORK`)
- 👤 User registration and login APIs
- 🚗 Vehicle CRUD (scoped to each logged-in user)
- 📅 Booking creation + listing (with overlap prevention logic)
- 🧪 5 Unit tests per module
- 🔁 Bonus: Prevents double-booking the same vehicle


---

## 🛠 How to Run the Project

```bash
git clone https://github.com/Tanveer-F/carrental_api.git
cd carrental_api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
````

## 📬 Sample Requests / Responses

### 🔐 Register

`POST /api/register/`

```json
{
  "username": "user1",
  "email": "user1@example.com",
  "password": "strongpass123"
}
```

### 🔐 Login

`POST /api/login/`

```json
{
  "username": "user1",
  "password": "strongpass123"
}
```

✅ Returns: `access` and `refresh` tokens

---

### 🚗 Vehicle Management

#### Add Vehicle

`POST /api/vehicles/`

```json
{
  "make": "Toyota",
  "model": "Corolla",
  "year": 2020,
  "plate": "ABC-123"
}
```

#### List Vehicles

`GET /api/vehicles/`

#### Update Vehicle

`PUT /api/vehicles/{id}/`

#### Delete Vehicle

`DELETE /api/vehicles/{id}/`

---

### 📅 Booking Management

#### Book a Vehicle

`POST /api/bookings/`

```json
{
  "vehicle": 1,
  "start_date": "2025-08-01",
  "end_date": "2025-08-05"
}
```

#### List Bookings

`GET /api/bookings/`

---

### ❗ Bonus: Prevent Overlapping Bookings

If a vehicle is already booked in the given range, the system blocks the new booking:

```json
{
  "non_field_errors": [
    "This car is already booked for the selected dates."
  ]
}
```

---

## ✅ Tests

Run all tests using:

```bash
python manage.py test
```

Test coverage includes:

* ✅ 5 tests in `users`
* ✅ 5 tests in `vehicles`
* ✅ 5+ tests in `bookings`
* ✅ Bonus: Overlap prevention is tested

---

## 🧠 Assumptions Made

- Only authenticated users can access vehicle and booking APIs
- Each user can only view and manage their own vehicles and bookings
- Booking module only supports `POST` and `GET` as per assignment (no update/delete)
- The `owner` field was added to the Vehicle model to scope vehicles to users
- Booking overlap prevention is implemented using a custom serializer validator
- Date overlap is checked using Django ORM (`start_date__lt` and `end_date__gt` filters)

---

## 🧾 1Now Product Overview

From my research, 1Now is a platform designed for car rental operators and Turo hosts who want more control over their business. 
Instead of relying fully on third-party apps, it gives them tools to manage bookings, verify renters, collect payments via Stripe or Square, 
And track expenses — all from a single dashboard. One thing I found interesting is that it even lets users sync with Turo 
While keeping direct bookings open, helping them keep more profit. 
Overall, it’s built to simplify operations while increasing earnings for independent fleet owners.

My backend API could connect to the frontend of LahoreCarRental.com through standard HTTP requests using JSON. The frontend (built in React, Vue, etc.) would call these REST endpoints for user login, vehicle management, and booking workflows. JWT tokens returned from login can be stored in localStorage or cookies, and sent with each request to keep the session secure. This setup allows seamless communication between the UI and backend while enforcing user-based data access and validation.



---

## 🔗 Author

* 👨‍💻 Developed by: **Tanveer Fazal**
* 🌐 GitHub: [https://github.com/Tanveer-F](https://github.com/Tanveer-F)
