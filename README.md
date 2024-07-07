# Game Analytics Web Service

This web service allows data analysts to upload a CSV file containing game data and run analyses on it. The service is built with FastAPI and uses SQLite for the database. It supports filtering and querying game data based on various fields.

## Features

- Upload CSV data via an API endpoint
- Query game data based on filters
- Simple authentication (optional)
- Dockerized deployment

## Requirements

- Python 3.8+
- SQLite (for local deployment)
- Docker (for Dockerized deployment)


## Running Locally

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/game-analytics-service.git
    cd game-analytics-service
    ```

2. Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Start the FastAPI server:
    ```sh
    uvicorn app.main:app --reload
    ```


## Running with Docker

### Setup

1. Clone the repository:
  ```sh
  git clone https://github.com/yourusername/game-analytics-service.git
  cd game-analytics-service
  ```

2. Build the Docker image:
  ```sh
  docker build -t game-analytics-service .
  ```

3. Run the Docker container:
  ```sh
  docker run -p 8000:8000 game-analytics-service
  ```


## Example Queries

### Upload CSV

POST /upload

Request Body:
- `file_url`: The URL to the Google Sheets to be uploaded.

### Query Data

GET /query

Query Parameters:
- `filters`: A dictionary string passed as a query parameter.
  ```sh
  {"SupportedLanguages": "French"}
  ```

## Cost of Running

Assuming one file upload and 100 queries a day, the cost on a free-tier cloud provider (like Heroku) should be minimal, leveraging the free plan for small projects.
