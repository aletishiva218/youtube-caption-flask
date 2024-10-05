from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, VideoNotAvailable
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/captions', methods=['POST'])
def fetch_captions():
    data = request.json
    url = data.get('url')

    # Extract video ID from URL
    if 'v=' in url:
        video_id = url.split('v=')[1].split('&')[0]
    else:
        return jsonify({'error': 'Invalid YouTube URL'}), 400

    try:
        # Fetch captions
        captions = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])  # specify language here
        return jsonify(captions)
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript available for this video.'}), 404
    except VideoNotAvailable:
        return jsonify({'error': 'The video is not available.'}), 404
    except Exception as e:
        print(f"Error fetching captions: {e}")
        return jsonify({'error': 'Failed to fetch captions'}), 500

if __name__ == '__main__':
    app.run(debug=True)
