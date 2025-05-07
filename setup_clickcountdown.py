import os

base_dir = r"C:\Users\Andrew\OneDrive\Projects\flask\ClickCountdown"

structure = {
    "app": [
        "__init__.py", "auth.py", "routes.py", "models.py",
        os.path.join("templates", "base.html"),
        os.path.join("templates", "login.html"),
        os.path.join("templates", "register.html"),
        os.path.join("templates", "dashboard.html"),
        os.path.join("static", "style.css"),
    ],
    "": ["run.py", "config.py", "requirements.txt"]
}

contents = {
    "run.py": """from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
""",

    "config.py": """import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'yoursecretkeyhere'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/clickcountdown'
""",

    "app/__init__.py": """from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from config import Config

mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    from .routes import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app
""",

    "app/models.py": """from flask_login import UserMixin
from . import login_manager, mongo
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.email = user_data['email']

@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        return User(user_data) if user_data else None
    except:
        return None
""",

    "app/auth.py": """from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from bson.objectid import ObjectId
from .models import User
from . import mongo

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if mongo.db.users.find_one({'email': email}):
            flash('Email already registered.')
            return redirect(url_for('auth.register'))

        hashed_pw = generate_password_hash(password)
        mongo.db.users.insert_one({'email': email, 'password': hashed_pw})
        flash('Registration successful!')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_data = mongo.db.users.find_one({'email': email})

        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('main.dashboard'))

        flash('Invalid credentials')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
""",

    "app/routes.py": """from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from . import mongo

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    events = mongo.db.events.find({'user_id': current_user.id})
    return render_template('dashboard.html', events=events)
""",

    "app/templates/base.html": """<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\">
  <title>Click Countdown</title>
  <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='style.css') }}\">
</head>
<body>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <ul class=\"flashes\">
        {% for message in messages %}
          <li>{{ message }}</li>
        {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}
  {% block content %}{% endblock %}
</body>
</html>
""",

    "app/templates/login.html": """{% extends 'base.html' %}
{% block content %}
<h2>Login</h2>
<form method=\"POST\">
  <input name=\"email\" placeholder=\"Email\">
  <input name=\"password\" placeholder=\"Password\" type=\"password\">
  <button type=\"submit\">Login</button>
</form>
<a href=\"{{ url_for('auth.register') }}\">Register</a>
{% endblock %}
""",

    "app/templates/register.html": """{% extends 'base.html' %}
{% block content %}
<h2>Register</h2>
<form method=\"POST\">
  <input name=\"email\" placeholder=\"Email\">
  <input name=\"password\" placeholder=\"Password\" type=\"password\">
  <button type=\"submit\">Register</button>
</form>
<a href=\"{{ url_for('auth.login') }}\">Login</a>
{% endblock %}
""",

    "app/templates/dashboard.html": """{% extends 'base.html' %}
{% block content %}
<h2>My Events</h2>
<div class=\"grid\">
  {% for event in events %}
    <div class=\"event\">
      <strong>{{ event.name }}</strong><br>
      Time: {{ event.date }}<br>
    </div>
  {% endfor %}
</div>
<a href=\"{{ url_for('auth.logout') }}\">Logout</a>
{% endblock %}
""",

    "app/static/style.css": """body {
  font-family: Arial;
  padding: 20px;
  background: #f1f1f1;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1em;
}
.event {
  background: white;
  padding: 1em;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
""",

    "requirements.txt": "Flask\nFlask-Login\nflask-pymongo\nWerkzeug\ndnspython\n"
}

# Create folders and write files
for folder, files in structure.items():
    folder_path = os.path.join(base_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    for file in files:
        file_path = os.path.join(base_dir, folder, file) if folder else os.path.join(base_dir, file)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        key = os.path.join(folder, file).replace("\\", "/")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(contents.get(key, f"# {file}"))

print("✅ All folders and files created successfully.")
