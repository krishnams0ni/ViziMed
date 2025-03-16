# ViziMed

ViziMed is a web application designed for medical professionals to manage patient information, track patient visits, and store medical scans and notes securely.

## Features

- User authentication (register, login, profile management)
- Patient management (add, edit, remove patients)
- Medical logs for each patient with date tracking
- Image upload capability for medical scans
- Responsive UI for desktop use

## Tech Stack

- Python 3.x
- Flask 3.1.0
- SQLAlchemy 2.0.39
- SQLite database
- HTML/CSS

## Installation

1. Navigate to the directory where you want to download the project:
   ```bash
   cd path/to/your/desired/directory
   ```

2. Clone the repository:
   ```bash
   git clone https://github.com/krishnams0ni/ViziMed.git
   cd ViziMed
   ```

3. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python run.py
   ```

6. Open your browser and navigate to:
   ```
   http://127.0.0.1:5050
   ```

## Usage

### Authentication
- Register a new account
- Login with your credentials
- Update your username or password in the profile section

### Patient Management
1. Add a new patient via the "Add Patient" link
2. View all your patients on the dashboard
3. Click on a patient's name to view and manage their logs
4. Edit patient information using the edit button

### Patient Logs
1. Click on a patient's name to access their logs
2. Add a new log with date, notes, and optional image uploads
3. Edit or delete existing logs
4. View and manage uploaded images

## Project Structure

- `/templates`: HTML templates
- `/static`: CSS files and uploaded images
- `models.py`: Database models
- `routes.py`: Application routes
- `app.py`: Flask application factory
- `run.py`: Application entry point

## Data Security

- User passwords are hashed for secure storage
- Patient data is stored locally in an SQLite database
- Images are stored in the `/static/images` directory
- User authentication is required to access any patient data

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
