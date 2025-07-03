# ClickCountdown

A mobile-friendly Flask web application for creating and managing countdown timers to important events.

## Features

- **User Authentication**: Secure login and registration system
- **Event Management**: Create, edit, and delete countdown events
- **Live Countdowns**: Real-time countdown timers that update every second
- **Mobile-First Design**: Responsive design optimized for mobile devices
- **Event Details Modal**: Click any event to view detailed information
- **Clean UI**: Modern, clean interface with smooth animations

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB with PyMongo
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with mobile-first responsive design

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd ClickCountdown
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MongoDB:
   - Install MongoDB or use MongoDB Atlas
   - Update the MongoDB connection string in `config.py`

5. Run the application:
```bash
python run.py
```

The app will be available at `http://127.0.0.1:5000`

## Usage

1. **Register/Login**: Create an account or log in to access your events
2. **Add Events**: Click "+ Add New Event" to create a new countdown
3. **View Events**: See all your countdown events on the dashboard
4. **Event Details**: Click any event to open a modal with detailed information
5. **Edit Events**: Use the "Edit Event" button in the modal to modify events
6. **Delete Events**: Use the trash icon to remove events

## Deployment

This app is ready for deployment on platforms like:
- PythonAnywhere
- Heroku
- Railway
- DigitalOcean App Platform

Make sure to:
- Set up environment variables for production
- Configure MongoDB connection for production
- Set `DEBUG = False` in production

## Project Structure

```
ClickCountdown/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── auth.py              # Authentication routes
│   ├── main.py              # Main application routes
│   ├── models.py            # User model
│   ├── static/
│   │   └── style.css        # Main stylesheet
│   └── templates/
│       ├── base.html        # Base template
│       ├── login.html       # Login page
│       ├── register.html    # Registration page
│       ├── dashboard.html   # Main dashboard
│       ├── add_event.html   # Add event form
│       └── edit_event.html  # Edit event form
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # This file
```

## License

This project is open source and available under the [MIT License](LICENSE). 