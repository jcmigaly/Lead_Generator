# Contractor Insights API

This project implements a FastAPI-based API that provides insights about contractors. While the initial goal was to scrape real contractor data using Selenium, I faced some challenges during the implementation process.

## Development Journey

### Web Scraping Attempt

Initially, I attempted to use Selenium for web scraping contractor information. While I successfully managed to extract the links, I encountered difficulties in scraping the detailed information from the target website. As a workaround, I populated the database with mock data to demonstrate the functionality of the system.

### Current Implementation

Despite the scraping challenges, I built a fully functional system that:

- Uses Supabase as the database backend
- Implements a RESTful API using FastAPI
- Provides contractor insights based on ratings and other criteria
- Demonstrates proper API structuring and error handling

## Features

- Get contractor insights with optional rating filters
- Limit results for better performance
- Error handling and proper response formatting
- CORS support for frontend integration

## Tech Stack

- FastAPI
- Supabase
- Python
- Selenium (initial attempt)

## Setup and Installation

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Create a `.env` file with:

   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at http://127.0.0.1:8000/

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Future Improvements

- Implement successful web scraping functionality
- Add more comprehensive contractor data
- Implement additional search and filter options
- Add authentication and rate limiting
