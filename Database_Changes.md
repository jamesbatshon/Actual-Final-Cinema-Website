# Database Changes — Cinema Website

# What changed

- Removed `seed.py` and the sample-data seeding command. The website no longer adds example movies, screenings, food or bookings.
- Changed the database connection from local SQLite to the UC3M **MariaDB** server.
- Added **PyMySQL** to connect to MariaDB and **python-dotenv** to read settings from `.env`.
- Kept the existing SQLAlchemy models and cinema booking features.

# How it works

The `.env` file stores the database connection details (and Flask secret key) outside the Python code. Flask-SQLAlchemy reads `SQLALCHEMY_DATABASE_URI`, connects through PyMySQL, and uses the existing models to save and retrieve records from MariaDB.

Example `.env` setting:

```dotenv
SQLALCHEMY_DATABASE_URI=mysql+pymysql://27_webapp_03:MY_PASSWORD@mysql.lab.it.uc3m.es/27_webapp_03a
```

The `.env` file is excluded from GitHub by `.gitignore`.

# First-time setup

On an authorised UC3M lab computer, install requirements and run:

```cmd
python -m pip install -r requirements.txt
python main.py init
python main.py create-admin --admin-email your-email@example.com
python app.py
```

- `init` creates the database tables **without inserting sample data**.
- `create-admin` securely prompts for a staff password and creates a management login.
- Staff then add movies, screens, ticket prices and showtimes through the website.

The university database is only accessible from approved lab computers or authorised virtual machines. This setup does not automatically copy old SQLite data into MariaDB.
