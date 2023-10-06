import requests
from PIL import Image
from io import BytesIO

clipDropAPIKey: str = "1529f6d30cc7ae8444632a20a1687462f0dd50e5f95ef2369c3c5c46ea74eb51ca61fb204a5c0f6235844cd6e00a0877"


def generateClipDropImage(prompt: str):
    r = requests.post("https://clipdrop-api.co/text-to-image/v1",
                      files={
                          'prompt': (None, prompt, 'text/plain')
                      },
                      headers={
                          'x-api-key': clipDropAPIKey}

                      )
    if r.ok:
        return r.content
    else:
        r.raise_for_status()


def displayImage(imageBytes):
    image = Image.open(BytesIO(imageBytes))


displayImage(generateClipDropImage("big golden dragon"))
