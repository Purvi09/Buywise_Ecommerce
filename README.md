# Ecommerce Application using Django and Razorpay

## Overview

This is an ecommerce application developed using Django, a high-level Python web framework, and integrated with Razorpay for payment processing (please note that no real money transactions occur). The application allows users to browse products, add items to their cart, proceed to the checkout page for a simulated payment experience using Razorpay, and also implements user authentication using email verification.

## Features

- Browse products: Users can view a list of available products with details like name, price, description, and an image representation.

- Add to Cart: Users can add products to their cart to keep track of items they wish to purchase.

- Checkout: Users can proceed to the checkout page where a simulated Razorpay payment process is initiated.

- Razorpay Integration: The application is connected to Razorpay's API to provide a seamless payment experience. Again, it's important to note that no real money is transferred in this demo application.

- User Authentication: The application implements user registration and login using email verification.
  - Users can register using their email addresses.
  - An email is sent to the user's registered email address with a verification link.
  - Clicking the verification link confirms the user's email and allows them to log in.
  - Users can log out when they are done with their session.
