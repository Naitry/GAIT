from flask import Flask, request, jsonify, Response

app = Flask(__name__)

@app.route('/square', methods=['GET'])
def squareNumber() -> Response:
    """
    Returns the square of a given number.

    Query Params:
        number: The number to be squared
    """
    num = request.args.get('number')
    try:
        squared_value = float(num) ** 2
        return jsonify({'result': squared_value})
    except:
        return jsonify({'error': 'Invalid input'})

if __name__ == '__main__':
    app.run(host='10.22.98.105', port=22555)
