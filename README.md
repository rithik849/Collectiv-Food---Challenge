## Overview

We want you to build an API that can create and validate orders, then return those orders to a frontend.

Please document any assumptions, tradeoffs, and decisions you make along the way. We would also like you to include what you would add or improve if you had more time.

The latter is particularly important. Please spend no more than **2 hours** on this challenge. We encourage the use of AI tools, but be prepared to explain your approach, the decisions made, and demonstrate a solid understanding of the code you submit.

## Scenario

This is a client-facing order management tool. Customers should be able to submit orders and view all existing orders.

---

## The Challenge

You will be given a dataset containing customer orders in JSON format. The dataset intentionally contains a number of issues, so don't assume the data is clean.

## Provided Files

This repository contains a dataset with the following files:

### Orders
- `orders.json` contains 15 order records.
- Dates are provided as strings in `DD/MM/YYYY` format.
- An order contains one or more `items`; each item represents a product being ordered and the quantity requested.
- `productSku` links an order item to a product in `products.json`. `itemTotal` is the total price for that item, and `total` is the overall order total.

### Products
- `products.json` contains the valid products that can be ordered.
- A product's `sku` is essentially its unique identifier, similar to an `id`.
- You can assume the product data is valid and can be used as the source of truth for checking order items.

---

## Your Task

### 1. Persist Valid Orders

Process the orders in `orders.json`, storing only valid orders. Reject invalid orders and provide a clear reason for each rejection.

### 2. Build an API

Create a simple API using a language and framework of your choice. Pick whatever you're most comfortable and productive in.

As a minimum, your API should expose endpoints to:

- Create a new valid order
- Retrieve all orders

### 3. Front End

At a minimum, we'd like to see:

- A form to create a new order
- Validation on that form
- A page that retrieves and displays all valid orders

### 4. Documentation

Include a short README that explains:

- How to run the application
- Any assumptions you made
- Design decisions and tradeoffs
- What you would improve or add if given more time

### 5. Finally

Please host your work on a publicly accessible GitHub repository.

### 6. Bonus

If you find yourself with time to spare, implement or provide pseudocode for any additional features you believe might benefit the platform. For example, how might you extend order validation to account for product stock availability and stock expiry dates?
