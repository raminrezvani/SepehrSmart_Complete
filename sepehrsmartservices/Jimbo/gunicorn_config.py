import os

# Get the APP_PORT from environment variable or set a default
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
workers = 1  # Adjust the number of workers as needed
