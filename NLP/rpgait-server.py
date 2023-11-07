# Required libraries
from flask import Flask, request, jsonify, send_from_directory
import base64
import requests
import openai
from PIL import Image
from io import BytesIO
from config import OPENAI_API_KEY, CLIPDROP_API_KEY, CHATGPT_RPG_MESSAGES, CHATGPT_IMAGEPROMPT_MESSAGES

# API Keys
openai.api_key = OPENAI_API_KEY

# Initialize global variables
user_input = "begin"
game_running = True

# Function to send user input to the ChatGPT instance for RPG responses
def send_user_input_to_chatgpt_instance_1(user_input):

    # Append user's input to the message list
    CHATGPT_RPG_MESSAGES.append(
        {
            "role" : "user",
            "content" : user_input
        }
    )

    # Make an API call to get a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=CHATGPT_RPG_MESSAGES,
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the message from the response and append to the message list
    message = response['choices'][0]['message']
    CHATGPT_RPG_MESSAGES.append(message)
    message_content = message['content']
    return message_content

# Function to send the ChatGPT RPG response to another ChatGPT instance for image prompts
def send_chatgpt_response_to_chatgpt_instance_2(chatgpt_response):

    # Append the response to the image prompt message list
    CHATGPT_IMAGEPROMPT_MESSAGES.append(
        {
            "role" : "user",
            "content" : chatgpt_response
        }
    )

    # Make an API call to get an image prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=CHATGPT_IMAGEPROMPT_MESSAGES,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Extract the message from the response and append to the message list
    message = response['choices'][0]['message']
    CHATGPT_IMAGEPROMPT_MESSAGES.append(message)
    message_content = message['content']
    return message_content

# Function to generate an image based on the image prompt using the ClipDrop API
def generate_image(image_prompt):
    r = requests.post('https://clipdrop-api.co/text-to-image/v1',
        files = {
            'prompt': (None, image_prompt, 'text/plain')
        },
        headers = { 'x-api-key': CLIPDROP_API_KEY}
        )
    if (r.ok):
        # r.content contains the bytes of the returned image
        image_bytes = r.content
        return image_bytes
    else:
        r.raise_for_status()

app = Flask(__name__)

@app.route('/')
def root():
    return send_from_directory('public', 'index.html')

# Serve static files from the public folder
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

@app.route('/genTurn', methods=['POST'])
def gen_turn():

    user_input = request.json.get('userInput', '')
    print('User input: ', user_input)

    # Get a game-related response from the ChatGPT RPG instance
    chatgpt_response = send_user_input_to_chatgpt_instance_1(user_input)
    print("GPT1: ", chatgpt_response)

    # Get an image prompt based on the game response
    image_prompt = send_chatgpt_response_to_chatgpt_instance_2(chatgpt_response)
    print("GPT2: ", image_prompt)

    # Generate an image based on the image prompt
    generated_image_bytes = generate_image(image_prompt)
    print("Image Received.")

    # Convert the image bytes to a base64 string
    base64_encoded_image = base64.b64encode(generated_image_bytes).decode("utf-8")
    print("Image Converted.")

    return jsonify({
        "chatgpt_response": chatgpt_response,
        "image_prompt": image_prompt,
        "generated_image_bytes": base64_encoded_image
    })

if __name__ == '__main__':
    app.run(debug=True)
