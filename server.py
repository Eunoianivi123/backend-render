from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route('/extract-audio', methods=['POST'])
def extract_audio():
    data = request.json
    video_url = data.get('videoUrl')
    audio_format = data.get('format', 'mp3')  # Default format is MP3

    if not video_url:
        return jsonify({"error": "Invalid URL"}), 400

    unique_id = str(uuid.uuid4())
    audio_file = f"static/{unique_id}.{audio_format}"

    try:
        # Get direct audio stream URL
        command = ["yt-dlp", "-f", "bestaudio", "-g", video_url]
        audio_url = subprocess.check_output(command).decode().strip()

        if not audio_url:
            return jsonify({"error": "Failed to get audio URL"}), 500

        # Convert audio to requested format using FFmpeg
        conversion_command = [
            "ffmpeg", "-i", audio_url, "-vn", f"-acodec {audio_format}", audio_file
        ]
        subprocess.run(conversion_command, check=True)

        return jsonify({"audioUrl": f"https://backend-render-2mbg.onrender.com/{audio_file}"})
    except subprocess.CalledProcessError:
        return jsonify({"error": "Audio extraction failed"}), 500

if __name__ == '__main__':
    os.makedirs("static", exist_ok=True)
    app.run(host="0.0.0.0", port=10000)  # Render uses dynamic ports
