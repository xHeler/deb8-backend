import base64
import requests
import os
from django.conf import settings
from .models import Post
from django.shortcuts import get_object_or_404


def send_image_to_openai(post_id, image_path):
    image_path = image_path.replace("media", "")
    image_path = settings.MEDIA_ROOT[:-1] + image_path

    # Function to encode the image to base64
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Get the API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    # Encode the image
    base64_image = encode_image(image_path)

    # Headers for the request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Payload with the text and image
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Opisz w maksymalnie 2-4 zdaniach co jest na obrazie. Zrób to w stylu opisu zdjęcia na social media, bez hasztagow."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    # Send the request
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    json = response.json()
    message = json["choices"][0]["message"]["content"]
    post = get_object_or_404(Post, post_id=post_id)
    post.description = message
    post.save()
    print(f"POST({post.post_id}) - Description generated({message})")

    return message
