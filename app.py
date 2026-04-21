from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Create a downloads folder if it doesn't exist
if not os.path.exists('downloads'):
    os.makedirs('downloads')

@app.route('/')
def index():
    # render_template looks inside the /templates/ folder
    # and sends it to the browser as a webpage
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"message": "No URL provided"}), 400

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    
    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--user-agent", user_agent,
        "-o", "downloads/%(title)s.%(ext)s",
        url
    ]

    try:
        subprocess.run(command, check=True)
        return jsonify({"message": "Download Successful! Check the downloads folder."})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)