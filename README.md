# xSMTP Store Backend

This is the backend for the xSMTP store, built with FastAPI and MongoDB. It includes user management, ticket system, categories, subcategories, and support for various product types.

## Features

- User registration and authentication
- JWT-based authentication
- Ticket system for user-admin communication
- Categories and subcategories management
- Product management with various product types
- Role-based access control

## Requirements

- Python 3.8+
- MongoDB

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/faresbrayek2/xsmtp-back.git
    cd your_repository_name
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file in the root of your project** with the following content:
    ```env
    SECRET_KEY=your_secret_key
    MONGODB_URL=mongodb://localhost:27017
    ```

## Running the Application

1. **Start MongoDB** if it's not already running. You can start it using:
    ```sh
    mongod
    ```

2. **Run the FastAPI application**:
    ```sh
    uvicorn app.main:app --reload
    ```

3. **Access the application**:
    - Open your browser and go to `http://127.0.0.1:8000`
    - The automatic API documentation will be available at `http://127.0.0.1:8000/docs`

## Project Structure

```
.
├── app
│ ├── main.py
│ ├── models
│ │ └── user.py
│ ├── routes
│ │ ├── auth.py
│ │ ├── category.py
│ │ ├── ticket.py
│ │ ├── product.py
│ │ └── user.py
│ ├── schemas
│ │ ├── auth.py
│ │ ├── category.py
│ │ ├── ticket.py
│ │ ├── product.py
│ │ └── user.py
│ ├── utils.py
│ └── init.py
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── venv
```



## API Endpoints

### Authentication

- **POST** `/auth/register`: Register a new user
- **POST** `/auth/token`: Obtain a JWT token

### Users

- **GET** `/users/me`: Get the current authenticated user
- **PUT** `/users/role/{user_id}`: Update the role of a user (Admin only)

### Tickets

- **POST** `/tickets/add`: Create a new ticket
- **GET** `/tickets`: Retrieve tickets for the logged-in user
- **GET** `/tickets/all`: Retrieve all tickets (Admin and Support only)
- **PUT** `/tickets/{id}`: Update a ticket's status or content

### Categories

- **POST** `/categories`: Create a new category (Admin only)
- **GET** `/categories`: Retrieve all categories
- **PUT** `/categories/{id}`: Update a category (Admin only)
- **DELETE** `/categories/{id}`: Delete a category (Admin only)

### Products

- **POST** `/products/shells`: Add a new Shells product (Sellers only)
- **POST** `/products/cpanel`: Add a new cPanel product (Sellers only)
- **POST** `/products/sshwhm`: Add a new SSH/WHM product (Sellers only)
- **POST** `/products/rdp`: Add a new RDP product (Sellers only)
- **POST** `/products/smtp`: Add a new SMTP product (Sellers only)
- **POST** `/products/mailers`: Add a new Mailers product (Sellers only)
- **POST** `/products/leads`: Add a new Leads product (Sellers only)
- **POST** `/products/business`: Add a new Business product (Sellers only)
- **POST** `/products/accounts`: Add a new Accounts product (Sellers only)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
