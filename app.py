from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def index():
    """ Render a JSON response. """
    return jsonify(
        slackUsername="Pythonian",
        backend=True,
        age=27,
        bio="An introvert that likes to make things happen on the web.")

if __name__ == '__main__':
    app.run()