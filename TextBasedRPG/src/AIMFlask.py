from flask import Flask, request, jsonify, Response, session, send_file
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
        number: The number to be squared
    """
    world: AIMWorld = AIMWorld(request.args.get('prompt'))

    world.generateGPTDescription()
    card: AIMCard.LandCard = world.generateLandCard()
    print(card.generateImageString(world.userDescription + '\n' +
                                   world.gptDescription))
    image: Image = card.generateImage(generator=generator,
                                      genOption=GenerationOption.SDXL)

    # Create a BytesIO object and save the image to it
    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')


if __name__ == '__main__':
    http_server = WSGIServer(('10.22.98.105', 22555), app)
    http_server.serve_forever()
