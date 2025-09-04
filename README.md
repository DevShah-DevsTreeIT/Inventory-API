# Project_01
API Project: A Backend Development Initiative:- Inventory API is a simple inventory management API for a store. In which we can manage a list of products, their categories, prices, stock levels etc.


---

# Inventory Project API

A Django RESTful API for managing **Users, Categories, and Products** with:

* 🔐 JWT Authentication
* 🛡 CSRF Protection
* 🗑 Soft Delete

---

## 🔧 Setup

1. Clone the project and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:

   ```bash
   python manage.py migrate
   ```

3. Start the server:

   ```bash
   python manage.py runserver
   ```

---

## 🛠 API Flow (Postman / frontend)

### 1. **Get CSRF Token**

Before making POST/PUT/DELETE requests, fetch the CSRF token:

```
GET /csrf/
```

Response:

```json
{ "csrfToken": "abc123..." }
```

👉 Copy this value and send it in headers as:

```
X-CSRFToken: abc123...
```

---

### 2. **Register User**

```
POST /users/register/
```

Body (raw JSON):

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "msg": "User Successfully Registered",
  "id": {
    "id": "uuid-here",
    "name": "testuser"
  }
}
```

---

### 3. **Login User**

```
POST /users/login/
```

Body:

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

Response:

```json
{ "token": "jwt-token-here" }
```

👉 Copy this JWT and send it in headers as:

```
Authorization: Bearer jwt-token-here
```

---

### 4. **Use APIs (with CSRF + JWT)**

#### ➤ Categories

* **Get all categories (public)**

  ```
  GET /products/categories/
  ```

* **Create category (protected)**

  ```
  POST /products/categories/
  ```

  Headers:

  ```
  Authorization: Bearer <jwt>
  X-CSRFToken: <csrf>
  ```

  Body:

  ```json
  {
    "category": "Electronics",
    "category_descrip": "All electronic products"
  }
  ```

* **Update category**

  ```
  PUT /products/categories/
  ```

  Body:

  ```json
  {
    "id": 1,
    "category": "Updated Electronics"
  }
  ```

* **Soft delete category**

  ```
  DELETE /products/categories/
  ```

  Body:

  ```json
  { "id": 1 }
  ```

---

#### ➤ Products

* **Get all products (public)**

  ```
  GET /products/
  ```

* **Create product (protected)**

  ```
  POST /products/
  ```

  Body:

  ```json
  {
    "category_id": 1,
    "product_name": "Laptop",
    "product_description": "Gaming laptop",
    "available_quantity": 5,
    "product_price": 1200.50
  }
  ```

* **Update product**

  ```
  PUT /products/
  ```

  Body:

  ```json
  {
    "id": 1,
    "product_name": "Updated Laptop"
  }
  ```

* **Soft delete product**

  ```
  DELETE /products/
  ```

  Body:

  ```json
  { "id": 1 }
  ```

---

## 📝 Notes

* Always include both **JWT (`Authorization`)** and **CSRF token (`X-CSRFToken`)** for POST/PUT/DELETE.
* GET requests are **public** and don’t need authentication.
* Soft delete means items are not permanently removed; they are just marked as deleted.

---