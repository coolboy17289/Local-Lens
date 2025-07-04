from flask import Flask, request, send_file, jsonify
import os
import datetime
import json

app = Flask(__name__)
STORY_FOLDER = "stories"

# Auto-create folder
if not os.path.exists(STORY_FOLDER):
    os.makedirs(STORY_FOLDER)

@app.route('/')
def index():
    return send_file("index.html")  # This will serve the index.html in the same folder

@app.route('/submit-story', methods=['POST'])
def submit_story():
    data = request.get_json()
    story = data.get('story')
    lat = data.get('lat')
    lng = data.get('lng')

    if not story or lat is None or lng is None:
        return jsonify({"error": "Missing data"}), 400

    filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt"
    filepath = os.path.join(STORY_FOLDER, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(json.dumps({
            "story": story,
            "latitude": lat,
            "longitude": lng,
            "timestamp": datetime.datetime.now().isoformat()
        }, indent=2))

    return jsonify({"success": True, "file": filename})

if __name__ == '__main__':
    app.run(debug=True)
