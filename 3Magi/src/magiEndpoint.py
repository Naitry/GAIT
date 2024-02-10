from flask import Flask, request, jsonify
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from Blu.Core.Persona import Persona
from Blu.Core.Information import InformationFragment

app = Flask(__name__)
CORS(app)

# Initialize and load the model
magi = Persona()
magi.loadFromFile("/home/naitry/Dev/GAIT/3Magi/markdown/personalities/Caspar2023-12-12 02:24:22.md")

@app.route('/get_self_image_embedding', methods=['GET'])
def getSelfImageEmbedding():
    """
    Endpoint to retrieve the self-image embedding vector.
    """
    embedding = magi.selfImage.embedding

    print("sending " + str(len(embedding)))
    # Return the embedding as JSON
    return jsonify({"embedding": embedding})

@app.route('/sayto', methods=['POST'])
def sayTo():
    """
    Endpoint to interact with the Persona model.
    """
    data = request.json
    user_input = data.get('text', '')
    name = data.get('name', '')


    # Use the model to generate a response
    response = magi.sayTo(name=name, inputFragment=InformationFragment(user_input)).body

    # Return the response
    return jsonify({"reply": response,
                    "name": magi.name})

if __name__ == '__main__':
    # Define the IP address and the port where the server will run
    http_server = WSGIServer(('10.22.98.105', 22757), app)
    http_server.serve_forever()