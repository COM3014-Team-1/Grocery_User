from app import create_app, db
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click

# Initialize the Flask app and migrations
app = create_app()
migrate = Migrate(app, db)

# Define a custom CLI command (optional, if you need any special management commands)
@app.cli.command("db_init")
@with_appcontext
def db_init():
    """Initialize the database"""
    db.create_all()

# Run the app or migrations if needed
if __name__ == "__main__":
    app.run(debug=True)
