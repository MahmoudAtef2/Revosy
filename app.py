"""Main application entry point - creates and runs the Flask app."""
from website import create_app

# Initialize the Flask application
app = create_app()

if __name__ == "__main__":
    # Run in debug mode during development
    app.run(debug=True)
