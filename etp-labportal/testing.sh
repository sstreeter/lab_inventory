python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install Flask
flask run


# 1. Set your app environment
export FLASK_APP=run.py   # (use `set` instead of `export` on Windows)

# 2. Initialize migrations folder (only if not already created)
flask db init

# 3. Generate migration scripts from your models
flask db migrate -m "initial"

# 4. Apply the migrations to create tables
flask db upgrade


# OR
pip3 install Flask SQLAlchemy
pip3 install Flask-Migrate

python3 setup_db.py
