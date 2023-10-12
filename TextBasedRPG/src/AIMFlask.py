from flask import Flask, request, jsonify, Response, session, send_file
import base64
from flask_cors import CORS  # <-- Add this import
from gevent.pywsgi import WSGIServer
from io import BytesIO
from AIMImageGeneration import GenerationOption
from AIMWorld import AIMWorld
from PIL import Image
from typing import Union
import AIMCard
from AIMImageGeneration import SDXLGenerator
from AIMImageGeneration import GenerationOption

app = Flask(__name__)
CORS(app)  # <-- Add this line to enable CORS

generator: SDXLGenerator = SDXLGenerator()


@app.route('/land', methods=['GET'])
def getLand() -> Union[Response, str]:
    """
    Returns the square of a given number.

    Query Params:
        number: The nuIn this modified code, fetchImage now also updates a description variable, which holds the text to be displayed. I also added a new Svelte conditional block to display this text centered above the image.
mber to be squared
    """
    world: AIMWorld = AIMWorld(request.args.get('prompt'))

    world.generateGPTDescription()
    card: AIMCard.LandCard = world.generateLandCard()
    print(card.generateImageString(world.userDescription + '\n' +
                                   world.gptDescription))
    image: Image = card.generateImage(generator=generator,
                                      genOption=GenerationOption.SDXL)

    # Convert the image to Base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return jsonify({"image": img_str, "name": world.name})


if __name__ == '__main__':
    http_server = WSGIServer(('10.22.98.105', 22555), app)
    http_server.serve_forever()
