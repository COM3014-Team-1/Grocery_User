create db name called "Grocery_User" in posgres
--inorder to connect postgres from application
pip install psycopg2
--or 
pip install psycopg2-binary

--can set your relateddb parameter with belows command, otherwise need to update manually inside config.py based on your local db set up
set DB_USER=your_username
set DB_PASSWORD=your_password
set DB_NAME=grocery_db
set DB_HOST=localhost
set DB_PORT=5432

--run python
python -m venv venv
venv\Scripts\activate

--install dependencies on VM
pip install Flask Flask-SQLAlchemy Flask-Migrate psycopg2-binary
pip install Flask-Migrate
pip install Flask-Script

--to run application 
python run.py runserver

--to run migration
flask db init      # Initialize the migrations folder
flask db migrate   # Create a migration script
flask db upgrade   # Apply migrations to the database
