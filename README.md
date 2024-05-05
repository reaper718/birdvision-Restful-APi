# E-commerce RESTful API

This project implements a RESTful API for managing products in an e-commerce application. It is built using Flask and Flask-JWT-Extended for authentication, with SQLite as the database.

## Requirements

- Python 3.x
- Flask
- Flask-JWT-Extended
- SQLite

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/e-commerce-api.git
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create the SQLite database file `database.db`:

    ```bash
    touch database.db
    ```

## Running the API

1. Start the Flask server:

    ```bash
    python app.py
    ```

2. The API will be accessible at `http://127.0.0.1:5000`.

## Authentication

- Use the `/login` endpoint to obtain an access token.
- Include the access token in the `Authorization` header as `Bearer <access_token>` for authenticated requests.
- Copy the access_token generted using the api and paste it in Authorization, Bearer token so that all the users are validated in postman.

## Endpoints

1. **GET /products**: Get all products.
2. **GET /products/<product_id>**: Get a specific product.
3. **POST /products**: Create a new product.
4. **PUT /products/<product_id>**: Update a product.
5. **DELETE /products/<product_id>**: Delete a product.

## Running Tests

1. Ensure the Flask server is running.
2. Run the unit tests:

    ```bash
    python test_app.py
    ```
