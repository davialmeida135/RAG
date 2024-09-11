from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from query_data import query_rag
from populate_database import clear_database, update_embeds
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Configuration
UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return "Hello, Worle!"

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query_text = data.get('query_text')
    if not query_text:
        return jsonify({'error': 'No query text provided'}), 400
    
    response = query_rag(query_text)
    return jsonify({'response': response})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        update_embeds()
        return jsonify({'success': 'File uploaded successfully'}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.json
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'success': 'File deleted successfully'}), 200
    else:
        return jsonify({'error': 'File not found'}), 404

@app.route('/reset', methods=['POST'])
def reset_database():
    clear_database()
    return jsonify({'success': 'Database reset successfully'}), 200

@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify({'files': files}), 200

if __name__ == '__main__':
    app.run(debug=True)