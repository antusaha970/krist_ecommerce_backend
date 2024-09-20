
# Krist (T-shirt selling web application)

Krist E-commerce is a web application where users can browse, select, and purchase from a collection of 1000 t-shirt designs. It provides a seamless shopping experience with features such as product filtering, order management, and secure payments through Stripe or cash on delivery. The admin has control over product uploads, order tracking, and account management.


## API documentation
Read API documentation from here made with POSTMAN
[Documentation](https://documenter.getpostman.com/view/36480406/2sA3kRL4oA) 


## Features
### Authentication
- Account creation.
- Login and logout for registered users.
- Password reset functionality with OTP verification.
- JWT Authentication system. 

### Product Management
- Each product includes details such as title, description, price, and other relevant information.
- Admin users can upload new products.
- Products can be filtered by category, size, and color.
- Customers can leave reviews and ratings for the products they have purchased.
- Complex query-based product filtering.

### Account Management
- Each account contains personal information, a cart, and a list of favorite items.
- Users can:
  - Update or delete personal information and addresses.
  -  Add multiple delivery addresses.
  - Add items to their cart or favorites.
  - Post reviews for purchased products.
  - Place and manage orders.

### Order Management
- Users can place multiple orders.
- Payments can be made via credit card (Stripe integration) or cash on delivery.
- Users receive email notifications after account creation and order placement.

### Admin Panel
- Admins can:
  - Upload new products.
  - View and manage all placed orders.
  - Update order statuses.
  - Promote users to admin accounts.

### Email System
- Automatic email notifications are sent for account creation and order placements.


### Deployment
- The application is deployed on a secure and scalable hosting platform.


## Tech Stack

**Django:** Web framework for the backend.

**Django REST Framework:** For building APIs.

**SQLite3:** Database for storing data.

**Stripe:** Payment gateway for processing payments.


## Docker Setup

Ensure that you have Docker and Docker Compose installed on your machine.

## Building the Docker Image

```bash
  docker compose build
```

This command will build the Docker image based on the Dockerfile and configurations in docker-compose.yml.

## Running the Application

```bash
  docker compose up
```

This command will build (if not already built) and start the containers as defined in the docker-compose.yml file. The application should be accessible at http://localhost:9000.


