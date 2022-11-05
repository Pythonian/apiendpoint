from flask import Flask, jsonify, request
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


@app.route('/calculate/', methods=['POST'])
def calculate():
    x = request.json.get('x', None)
    y = request.json.get('y', None)
    operation_type = request.json.get('operation_type', None)

    if operation_type is not None and x is not None and y is not None:
        if operation_type == "addition":
            result = x + y
        elif operation_type == "subtraction":
            result = x - y
        elif operation_type == "multiplication":
            result = x * y
        else:
            result = None
    else:
        return None

    return jsonify(
        slackUsername="Pythonian",
        operation_type=operation_type,
        result=result)


if __name__ == '__main__':
    app.run()