import environ
import os

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# reading .env file
environ.Env.read_env('.env')

APP_PORT = env('APP_PORT')
APP_WORKERS = env('APP_WORKERS')

# Get the APP_PORT from environment variable or set a default
bind = f"0.0.0.0:{os.environ.get('APP_PORT', 5000)}"
workers = int(APP_WORKERS)  # Adjust the number of workers as needed

def post_fork(server, worker):
    worker_id = len(server.WORKERS)
    os.environ['WORKER_ID'] = str(worker_id)