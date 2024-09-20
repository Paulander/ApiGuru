```markdown
# API Guru

API Guru is a web-based API call management tool created with help from Replit. It allows users to make, save, and manage API calls, as well as view call history and statistics.

## Features

- Make API calls (GET and POST methods supported)
- Save and load predefined API calls
- Verify API keys
- View API call history
- Dashboard with API usage statistics
- Export and import predefined calls

## Technologies Used

- Python 3.11
- Flask 3.0.3
- PostgreSQL (via psycopg2-binary 2.9.9)
- Requests 2.32.3
- Chart.js (for dashboard visualizations)

## Setup and Installation

1. Clone this repository to your local machine or Replit environment.
2. Ensure you have Python 3.11 installed.
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   Or if using Poetry:
   ```
   poetry install
   ```
4. Set up your PostgreSQL database and update the environment variables with your database credentials:
   - PGHOST
   - PGPORT
   - PGDATABASE
   - PGUSER
   - PGPASSWORD

## Running the Application

To run the application, execute:

```
python main.py
```

The application will start and be accessible at `http://localhost:5000` or the URL provided by your Replit environment.

## Development

This project was developed with the help of Replit, an online IDE that makes it easy to write and deploy code. The project structure and configuration files are set up to work seamlessly with Replit's environment.

## Contributing

Contributions to API Guru are welcome! Please feel free to submit a Pull Request.

```
