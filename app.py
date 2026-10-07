from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp, os, uuid

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    if not url: return jsonify({'error':'No URL'}), 400
    try:
        uid = str(uuid.uuid4())[:8]
        ydl_opts = {'outtmpl': f'/tmp/{uid}.%(ext)s', 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return jsonify({'download_url': f'/file/{os.path.basename(filename)}', 'title': info.get('title')})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home(): return "ClickFlick Backend Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
