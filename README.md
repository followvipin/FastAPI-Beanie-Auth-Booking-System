# FastAPI-Beanie-Auth-Booking-System
The FastAPI Booking System is a comprehensive application designed to streamline booking processes with robust authentication and advanced booking features. The project integrates Google sign-in alongside the existing JWT authentication, providing users with flexible authentication options. Users can authenticate using either Google sign-in or traditional JWT methods and obtain a JWT token for secure access.

## Getting Started

### Prerequisites

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic v2
- MongoDB installed in the system

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/followvipin/FastAPI-Beanie-Auth-Booking-System.git
    cd FastAPI-Beanie-Auth-Booking-System
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Running the Application. To run the application, use the following command**:
    ```sh
    python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
    ```

### Documentation

- Open SwaggerUi by this url http://localhost:8000/docs in the browser.

- Create an account by "/user/signup/" api.

- Now login by "/user/signup/" api.

- Copy the returned token string.

- Scroll to the top of the swagger and find a lock icon.

- Now click on the lock icon paste the token into the field and log in.

- Now you are authenticated for 24 hours.

- Let's retrieve all users in database by api "/user/retrieve_all_users/".

- Now scroll down and find "/booking/create_booking/" and create your booking.

- Let's retrieve all bookings of the user by api "/user/retrieve/active/bookings/".

- Let's retrieve booking history of the user by api "/user/calendar/history/bookings/".

- Let's retrieve upcoming bookings of the user by api "/user/calendar/upcoming/bookings/".

- Copy any booking id and use it for modify or cancel the booking. 

- "/booking/modify_booking/{booking_id}/" for modify the booking.

- "/booking/cancle_booking/{booking_id}/" for cancle the booking.

# Thank You!