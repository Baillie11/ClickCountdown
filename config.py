import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'yoursecretkeyhere'
    MONGO_URI = os.environ.get('MONGO_URI') or "mongodb+srv://andrew:aB2TizhFa2FXkF@click.ahmkf2e.mongodb.net/clickcountdown?retryWrites=true&w=majority&appName=Click"
