import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://andrew:v79i18OGZMCvmOl2@click.ahmkf2e.mongodb.net/clickcountdown?retryWrites=true&w=majority&appName=Click'
    REMEMBER_COOKIE_DURATION = timedelta(days=365)
