# HNG 11 Backend Stage 2 Task: User Authentication & Organisation

### Walkthrough for Testing API Endpoints

#### 1. **Register User**

- **Endpoint**: `POST /auth/register/`
- **Description**: Registers a new user and creates a default organisation for the user.
- **Request Body**:

  ```json
  {
      "firstName": "John",
      "lastName": "Doe",
      "email": "johndoe@example.com",
      "password": "password123"
  }
  ```

- **Successful Response**:

  ```json
  {
      "status": "success",
      "message": "Registration successful",
      "data": {
          "accessToken": "access_token_here",
          "user": {
              "userId": "user_id_here",
              "firstName": "John",
              "lastName": "Doe",
              "email": "johndoe@example.com"
          }
      }
  }
  ```

#### 2. **Login User**

- **Endpoint**: `POST /auth/login/`
- **Description**: Logs in a user with their email and password.
- **Request Body**:

  ```json
  {
      "email": "johndoe@example.com",
      "password": "password123"
  }
  ```

- **Successful Response**:

  ```json
  {
      "status": "success",
      "message": "Login successful",
      "data": {
          "accessToken": "access_token_here",
          "user": {
              "userId": "user_id_here",
              "firstName": "John",
              "lastName": "Doe",
              "email": "johndoe@example.com"
          }
      }
  }
  ```

#### 3. **Get User Information**

- **Endpoint**: `GET /users/:id`
- **Description**: Retrieves user information. Requires authentication.
- **Headers**:
  - `Authorization`: Bearer `access_token_here`
- **Successful Response**:

  ```json
  {
      "status": "success",
      "message": "User retrieved successfully",
      "user": {
          "userId": "user_id_here",
          "firstName": "John",
          "lastName": "Doe",
          "email": "johndoe@example.com"
      }
  }
  ```

#### 4. **Get User's Organisations**

- **Endpoint**: `GET /organisations`
- **Description**: Retrieves all organisations the authenticated user belongs to. Requires authentication.
- **Headers**:
  - `Authorization`: Bearer `access_token_here`
- **Successful Response**:

  ```json
  {
      "status": "success",
      "message": "Organisations retrieved successfully",
      "data": {
          "organisations": [
              {
                  "orgId": "organisation_id_here",
                  "name": "John's Organisation",
                  "description": "Default organisation"
              }
          ]
      }
  }
  ```

#### 5. **Get Specific Organisation**

- **Endpoint**: `GET /organisations/:orgId`
- **Description**: Retrieves details of a specific organisation. Requires authentication.
- **Headers**:
  - `Authorization`: Bearer `access_token_here`
- **Successful Response**:

  ```json
  {
      "status": "success",
      "message": "Organisation retrieved successfully",
      "data": {
          "orgId": "organisation_id_here",
          "name": "John's Organisation",
          "description": "Default organisation"
      }
  }
  ```

#### 6. **Create New Organisation**

- **Endpoint**: `POST /organisations`
- **Description**: Creates a new organisation and adds the authenticated user to it. Requires authentication.
- **Headers**:
  - `Authorization`: Bearer `access_token_here`
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
          "orgId": "organisation_id_here",
          "name": "New Organisation",
          "description": "This is a new organisation"
      }
  }
  ```

#### 7. **Add User to Organisation**

- **Endpoint**: `POST /organisations/:orgId/users`
- **Description**: Adds a user to a specific organisation. The endpoint is not protected and can be accessed publicly.
- **Request Body**:

  ```json
  {
      "userId": "user_id_here"
  }
  ```

- **Successful Response**:

  ```json
  {
      "status": "success",
      "message": "User added to organisation successfully"
  }
  ```

#### 8. **Common Error Responses**

- **Validation Error**:

  ```json
  {
      "status": "Bad request",
      "message": "Validation failed",
      "errors": [
          {
              "field": "email",
              "message": "This field is required."
          }
      ]
  }
  ```

- **Authentication Failed**:

  ```json
  {
      "status": "Bad request",
      "message": "Authentication failed",
      "statusCode": 401
  }
  ```

- **Forbidden**:

  ```json
  {
      "status": "Forbidden",
      "message": "You do not have permission to view this resource",
      "statusCode": 403
  }
  ```

- **Not Found**:

  ```json
  {
      "status": "Not found",
      "message": "Resource not found",
      "statusCode": 404
  }
  ```

### How to Use This Walkthrough

1. **Base URL**: Ensure all requests are made to the base URL `https://seyipythonian.pythonanywhere.com/`.
2. **Authentication**: For endpoints that require authentication, use the `accessToken` received from the register or login endpoints.
3. **Headers**: Include `Content-Type: application/json` in headers where applicable.
4. **Request Body**: Use the example request bodies provided for each endpoint.
5. **Handling Responses**: Check the response status codes and body to ensure the request was successful or to understand any errors.
