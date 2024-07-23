# FastAPI-Beanie-Auth-Booking-System
This repository contains a comprehensive project demonstrating the creation of a web application using FastAPI, Beanie ORM, and MongoDB. The project is divided into three parts, each progressively increasing in complexity.

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

### Running the Application
    To run the application, use the following command:
        ```sh
        python3 -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
        ```