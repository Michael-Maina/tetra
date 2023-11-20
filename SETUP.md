# Project Setup Guide

## Prerequisites

Before starting, ensure you have the following installed on your system:

- Python (version 3.8 or higher)
- MongoDB (version 6.0 or higher)

## Setting Up a Virtual Environment

To maintain project isolation and manage dependencies, we use a virtual environment. Follow these steps to create and activate a virtual environment:

1. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment:**
   ```bash
   source venv/bin/activate
   ```

## Installing Dependencies

After activating the virtual environment, install project dependencies using `pip` and the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Configuring Environment Variables

The project utilizes the `dotenv` package for managing environment variables. Create a `.env` file in the root directory of the project and add your environment variables:

```plaintext
# Example .env file
FLASK_APP=app.py
FLASK_ENV=development
MONGO_URI=<your-mongodb-uri>
SECRET_KEY=<your-secret-key>
# Add other environment variables as required
```
These are loaded automatically by the `python-dotenv` library into the application.

Ensure you replace `<your-mongodb-uri>` and `<your-secret-key>` with your actual MongoDB connection URI and a secret key for Flask.

## Running the Application

To start the Flask application, execute the following command in the root directory of the repository:

```bash
flask run
```

This will launch the application locally, and you should be able to access it in your web browser at `http://localhost:5000`.

## Additional Notes

- **Database Setup:** Ensure your MongoDB server is running and accessible with the provided connection URI.
- **File Structure:** The Flask app files and folders should be organized according to your project's structure, with the main Python file typically named `app.py`.
- **Debug Mode:** The application will run in debug mode by default when using `flask run`. This mode enables automatic reloading on code changes and provides helpful debug information in the browser.
