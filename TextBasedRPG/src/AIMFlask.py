from flask import Flask, request, jsonify, Response, session, send_file
import base64
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

    # Convert the image to Base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return jsonify({"image": img_str, "name": world.name})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22555)
