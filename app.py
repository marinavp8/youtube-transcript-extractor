import os
from flask import Flask, request, render_template_string
from youtube_transcript import get_video_transcript

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Transcript Extractor</title>
</head>
<body>
    <h1>YouTube Transcript Extractor</h1>
    <form method="POST">
        <input type="text" name="video_id" placeholder="Enter YouTube Video ID">
        <input type="submit" value="Get Transcript">
    </form>
    {% if transcript %}
    <h2>Transcript:</h2>
    <pre>{{ transcript }}</pre>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = ''
    if request.method == 'POST':
        video_id = request.form['video_id']
        try:
            transcript = get_video_transcript(video_id)
        except Exception as e:
            transcript = f"An error occurred: {str(e)}"
    return render_template_string(HTML, transcript=transcript)

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
