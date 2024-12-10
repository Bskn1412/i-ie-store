import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
# pip install flask requests python-dotenv
# Load environment variables
load_dotenv()

app = Flask(__name__)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "Bskn1412"
REPO_NAME = "i-ie-store"

@app.route('/upload', methods=['POST'])
def upload_to_github():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    # Save file locally
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Read file content
    with open(file_path, 'rb') as f:
        file_content = f.read()

    # GitHub API upload
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file.filename}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    data = {
        "message": f"Add {file.filename}",
        "content": file_content.decode('latin1')  # Encode file for GitHub API
    }

    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        return jsonify({"message": "File uploaded successfully!"}), 201
    else:
        return jsonify({"error": response.json()}), response.status_code

if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)  # Ensure upload directory exists
    app.run(debug=True)
