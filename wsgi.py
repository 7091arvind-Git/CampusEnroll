"""
WSGI Entry Point for CampusEnroll – Student Course Registration System
Used for production deployments with Gunicorn, Waitress, or Cloud Platforms (Render, Railway, Heroku).
"""
import os
from app import app

# Expose WSGI application callable
application = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # In local testing or fallback, run on all interfaces
    app.run(host='0.0.0.0', port=port)
