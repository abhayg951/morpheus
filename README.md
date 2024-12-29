---

# **Form Builder API Documentation**

## **Overview**
This API allows Admin users to create and manage forms and enables end-users to submit responses anonymously. Analytics are provided for each form and question type. The API is secured with token-based authentication for Admin endpoints.

---

## **Getting Started**

### Prerequisites
1. Python 3.9+
2. Django 4.x
3. Django Rest Framework 3.x
4. PostgreSQL (or SQLite/MySQL)

### Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Create an Admin User**:
   ```bash
   python manage.py createsuperuser
   ```

---

## **Authentication**

### Admin Login (Token Generation)

**Endpoint**: `POST /api-token-auth/`

**Description**: Authenticate an Admin user and generate an authentication token.

**Request**:
```json
{
    "username": "admin",
    "password": "password123"
}
```

**Response**:
```json
{
    "token": "your-auth-token",
    "user_id": 1,
    "username": "admin"
}
```

**Error Responses**:
- `403 Forbidden`: User is not an Admin.
- `400 Bad Request`: Invalid credentials.

---

## **Admin APIs**

All Admin APIs require the `Authorization` header with the token:
```
Authorization: Token your-auth-token
```

### Create a Form

**Endpoint**: `POST /forms/`

**Description**: Allows Admins to create a new form.

**Request**:
```json
{
    "title": "Customer Feedback",
    "description": "Collect feedback on our service",
    "questions": [
        {
            "type": "text",
            "question_text": "What is your name?",
            "order": 1
        },
        {
            "type": "checkbox",
            "question_text": "Which services did you use?",
            "order": 2,
            "options": ["Cleaning", "Laundry", "Ironing"]
        }
    ]
}
```

**Response**:
```json
{
    "id": 1,
    "title": "Customer Feedback",
    "description": "Collect feedback on our service",
    "questions": [
        {
            "id": 1,
            "type": "text",
            "question_text": "What is your name?",
            "order": 1
        },
        {
            "id": 2,
            "type": "checkbox",
            "question_text": "Which services did you use?",
            "order": 2,
            "options": ["Cleaning", "Laundry", "Ironing"]
        }
    ]
}
```

---

### View All Forms

**Endpoint**: `GET /forms/`

**Description**: Retrieve a list of all forms created by the Admin.

**Response**:
```json
[
    {
        "id": 1,
        "title": "Customer Feedback",
        "description": "Collect feedback on our service",
        "question_count": 2
    }
]
```

---

### View Analytics

**Endpoint**: `GET /forms/<form_id>/analytics/`

**Description**: Retrieve analytics for a specific form.

**Response**:
```json
{
    "total_responses": 25,
    "question_analytics": [
        {
            "id": 1,
            "question_text": "What is your name?",
            "type": "text",
            "top_words": {
                "John": 5,
                "Alice": 4,
                "Others": 16
            }
        },
        {
            "id": 2,
            "question_text": "Which services did you use?",
            "type": "checkbox",
            "top_combinations": {
                "Cleaning, Laundry": 10,
                "Cleaning": 8,
                "Others": 7
            }
        }
    ]
}
```

---

## **End-User APIs**

### Submit a Response

**Endpoint**: `POST /forms/<form_id>/responses/`

**Description**: Submit a response to a form anonymously.

**Request**:
```json
{
    "responses": [
        {"question_id": 1, "answer": "John"},
        {"question_id": 2, "answer": ["Cleaning", "Laundry"]}
    ]
}
```

**Response**:
```json
{
    "message": "Response submitted successfully!"
}
```

---

## **Error Handling**

- `401 Unauthorized`: Missing or invalid token for Admin endpoints.
- `403 Forbidden`: User lacks the necessary permissions.
- `404 Not Found`: Form or question does not exist.
- `400 Bad Request`: Validation error in the request payload.

---

## **Future Enhancements**

1. Add support for additional question types (e.g., Ranking, File Upload).
2. Implement role-based access control for advanced user roles.
3. Add pagination for large datasets in analytics.
