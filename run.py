from app import create_app, db
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click

# Initialize the Flask app and migrations
app = create_app()
migrate = Migrate(app, db)

# (Optional Feature) Define the custom CLI command if wanting to call it manually
@app.cli.command("db_init")
@with_appcontext
def db_init():
    """Initialize the database"""
    db.create_all()

if __name__ == "__main__":
    # Automatically create all database tables on app startup
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5002)


