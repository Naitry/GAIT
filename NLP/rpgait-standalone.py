# Required libraries
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

# Function to display the generated image
def display_image(image_bytes):

    # Convert the bytes to an image format
    byte_stream = BytesIO(image_bytes)
    image = Image.open(byte_stream)

    # Display the image using the default image viewer
    image.show()

# Main loop for the game
while game_running:

    # Get a game-related response from the ChatGPT RPG instance
    chatgpt_response = send_user_input_to_chatgpt_instance_1(user_input)
    print(chatgpt_response)

    # Get an image prompt based on the game response
    image_prompt = send_chatgpt_response_to_chatgpt_instance_2(chatgpt_response)
    print(image_prompt)

    # Generate an image based on the image prompt
    generated_image_bytes = generate_image(image_prompt)

    # Display the generated image
    display_image(generated_image_bytes)

    # Get the next user input
    user_input = input("User: ")

    # End the game if the user types "exit"
    if user_input.lower() == "exit":
        game_running = False

# Game loop ends
print("Game over. Thanks for playing!")
