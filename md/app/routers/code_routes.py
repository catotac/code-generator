from flask import send_file, session, Blueprint, jsonify
import os

code_bp = Blueprint('code_bp', __name__)

GENERATED_CODE_DIR = 'models/generated_code'

@code_bp.route('/api/download_code', methods=['GET'])
def download_code():
    """Combine generated code blocks and return a single code file."""
    chat_id = session.get('chat_id')

    if not chat_id or not os.path.exists(os.path.join(GENERATED_CODE_DIR, f'{chat_id}.txt')):
        return jsonify({"error": "No code to download."}), 400

    return send_file(os.path.join(GENERATED_CODE_DIR, f'{chat_id}.txt'), as_attachment=True)
