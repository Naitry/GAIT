from flask import Flask, request, jsonify, Response, session, send_file
from io import BytesIO
from AIMImageGeneration import GenerationOption
from AIMWorld import AIMWorld
from PIL import Image
from typing import Union
import AIMCard

app = Flask(__name__)


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
    print(card.generateImageString(world.gptDescription))
    image: Image = card.generateImage(generator=None,
                                      genOption=GenerationOption.ClipDrop)

    # Create a BytesIO object and save the image to it
    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    byte_io.seek(0)

    return send_file(byte_io, mimetype='image/png')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22555)
