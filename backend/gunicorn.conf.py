import os

# Render sets the PORT environment variable (default 10000)
# We must listen on this port for the health check to pass
port = os.getenv("PORT", "10000")
bind = f"0.0.0.0:{port}"

# Worker configuration
workers = 1
threads = 4
timeout = 120  # Increase timeout for slow AI operations
