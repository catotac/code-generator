from flask import Flask
from app.routers.chat_routes import chat_bp
from app.routers.code_routes import code_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow CORS for all routes
app.secret_key = 'your_secret_key'

# Register blueprints for different routes
app.register_blueprint(chat_bp)
app.register_blueprint(code_bp)

if __name__ == '__main__':
    app.run(debug=True)
