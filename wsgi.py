from app import app  # Import the Flask app from your app.py file
import logging
from logging.handlers import RotatingFileHandler

# Set up logging for the WSGI server
if not app.debug:
    # Create a rotating file handler that logs error messages
    file_handler = RotatingFileHandler('wsgi_errors.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.ERROR)
    
    # Define the log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Add the file handler to the app's logger
    app.logger.addHandler(file_handler)

if __name__ == "__main__":
    # Run the Flask app in development mode
    app.run()

# For production, run the app using a WSGI server (e.g., Gunicorn, uWSGI)
