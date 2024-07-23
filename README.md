# FastAPI-Beanie-Auth-Booking-System
The FastAPI Booking System is a comprehensive application designed to streamline booking processes with robust authentication and advanced booking features. The project integrates Google sign-in alongside the existing JWT authentication, providing users with flexible authentication options. Users can authenticate using either Google sign-in or traditional JWT methods and obtain a JWT token for secure access.

## Getting Started

### Prerequisites

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic v2

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