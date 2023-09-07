from datetime import datetime
from datetime import timezone
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/', methods=['GET'])
def api():
    """ Render a JSON response. """
    slack_name = request.args.get('slack_name', None)
    track = request.args.get('track', None)

    current_day_of_week = datetime.utcnow().strftime('%A')
    utc_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    return jsonify(
        slack_name=slack_name,
        current_day=current_day_of_week,
        utc_time=utc_time,
        track=track,
        github_file_url="https://github.com/Pythonian/apiendpoint/blob/main/app.py",
        github_repo_url="https://github.com/Pythonian/apiendpoint",
        status_code=200)


if __name__ == '__main__':
    app.run()