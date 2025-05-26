# app.py
import random

from flask import Flask, render_template, request, redirect, url_for
import os
from backend.search_and_describe import search_and_describe
from backend.tts import generate_audio
from werkzeug.utils import secure_filename

from flask import send_from_directory




UPLOAD_FOLDER = 'queries'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}




app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    audio_url = None

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            
            
            
            results = search_and_describe(filepath)
            audio_path = generate_audio(results[0]['description'])
            audio_url = url_for('static', filename='audio/current_audio.mp3') + f"?v={random.randint(1000,9999)}"
            return render_template('index.html', results=results, audio_url=audio_url)
            

    return render_template('index.html', results=results, audio_url=audio_url)

@app.route('/gallery/<filename>')
def serve_gallery_image(filename):
    return send_from_directory('gallery', filename)

if __name__ == '__main__':
    app.run(debug=True)
