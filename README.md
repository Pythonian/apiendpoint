# HNG 11 Backend Stage 2 Task: User Authentication & Organisation

### Walkthrough for Testing API Endpoints

**Base URL**: All requests to be made through `https://seyipythonian.pythonanywhere.com/`

#### 1. **Register User**

- **Endpoint**: `POST /auth/register`
- **Description**: Registers a new user and creates a default organisation for the user.
- **Request Body**:

```json
{
    "firstName": "Mark",
    "lastName": "Essien",
    "email": "markessien@hng.com",
    "password": "hngelevensucks",
    "phone": "09001234567"
}
```

- **Successful Response**:

```json
{
    "status": "success",
    "message": "Registration successful",
    "data": {
        "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMzcxODgyLCJpYXQiOjE3MjAzNzE1ODIsImp0aSI6ImE2ZjBjOWE3NjM5NzQzNmM5ZmFmMTQxNzVjZWQ0OWI3IiwidXNlcklkIjoiNThlYzhiNjctYTA1Yy00NjA4LThhMjAtMzkxMGI3OTUzMDUzIn0.rbS_TFk5tQ2hz9coD5814yP8lYaypGo7h8Q-wdD-Uq4",
        "user": {
            "userId": "58ec8b67-a05c-4608-8a20-3910b7953053",
            "firstName": "Mark",
            "lastName": "Essien",
            "email": "markessien@hng.com",
            "phone": "09001234567"
        }
    }
}
```

- **Validation Error Response**:

```json
{
    "errors": [
        {
            "field": "string",
            "message": "string"
        }
    ]
}
```

#### 2. **Login User**

- **Endpoint**: `POST /auth/login`
- **Description**: Logs in a user with their email and password.
- **Request Body**:

```json
{
    "email": "markessien@hng.com",
    "password": "hngelevensucks"
}
```

- **Successful Response**:

```json
{
    "status": "success",
    "message": "Login successful",
    "data": {
        "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIwMzcxODgyLCJpYXQiOjE3MjAzNzE1ODIsImp0aSI6ImE2ZjBjOWE3NjM5NzQzNmM5ZmFmMTQxNzVjZWQ0OWI3IiwidXNlcklkIjoiNThlYzhiNjctYTA1Yy00NjA4LThhMjAtMzkxMGI3OTUzMDUzIn0.rbS_TFk5tQ2hz9coD5814yP8lYaypGo7h8Q-wdD-Uq4",
        "user": {
            "userId": "58ec8b67-a05c-4608-8a20-3910b7953053",
            "firstName": "Mark",
            "lastName": "Essien",
            "email": "markessien@hng.com",
            "phone": "09001234567"
        }
    }
}
```

#### 3. **Get User Information**

- **Endpoint**: `GET /api/users/:id`
- **Description**: Retrieves user information. Requires authentication.
- **Headers**:
  - `Authorization`: Bearer Token
- **Successful Response**:

```json
{
    "status": "success",
    "message": "User retrieved successfully",
    "user": {
        "userId": "58ec8b67-a05c-4608-8a20-3910b7953053",
        "firstName": "Mark",
        "lastName": "Essien",
        "email": "markessien@hng.com"
    }
}
```

#### 4. **Get User's Organisations**

- **Endpoint**: `GET /api/organisations`
- **Description**: Retrieves all organisations the authenticated user belongs to. Requires authentication.
- **Headers**:
  - `Authorization`: Bearer Token
- **Successful Response**:

```json
{
    "status": "success",
    "message": "Organisations retrieved successfully",
    "data": {
        "organisations": [
            {
                "orgId": "58ec8b67-b16r-4608-8a20-3910b7953099",
                "name": "Mark's Organisation",
                "description": "Default organisation"
            }
        ]
    }
}
```

#### 5. **Get Specific Organisation**

- **Endpoint**: `GET /api/organisations/:orgId`
- **Description**: Retrieves details of a specific organisation. Requires authentication.
- **Headers**:
  - `Authorization`: Bearer Token
- **Successful Response**:

```json
{
    "status": "success",
    "message": "Organisation retrieved successfully",
    "data": {
        "orgId": "58ec8b67-b16r-4608-8a20-3910b7953099",
        "name": "Mark's Organisation",
        "description": "Default organisation"
    }
}
```

#### 6. **Create New Organisation**

- **Endpoint**: `POST /api/organisations`
- **Description**: Creates a new organisation and adds the authenticated user to it. Requires authentication.
- **Headers**:
  - `Authorization`: Bearer Token
- **Request Body**:

```json
{
    "name": "New Organisation",
    "description": "This is a new organisation"
}
```

- **Successful Response**:

```json
{
    "status": "success",
    "message": "Organisation created successfully",
    "data": {
        "orgId": "58ec8b67-a5y7-4608-11a7-3910b7953011",
        "name": "New Organisation",
        "description": "This is a new organisation"
    }
}
```

#### 7. **Add User to Organisation**

- **Endpoint**: `POST /api/organisations/:orgId/users`
- **Description**: Adds a user to a specific organisation. The endpoint is not protected and can be accessed publicly.
- **Request Body**:

```json
{
    "userId": "45ec8b67-r5t7-4608-8a20-3910b7958760"
}
```

- **Successful Response**:

```json
{
    "status": "success",
    "message": "User added to organisation successfully"
}
```

### Running Tests

```python
    python manage.py test accounts/tests
```
