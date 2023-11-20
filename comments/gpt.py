import os
import threading
import requests
import json
from .models import Comment
from posts.models import Post
from django.shortcuts import get_object_or_404


api_key = os.getenv("OPENAI_API_KEY")

api_endpoint = 'https://api.openai.com/v1/chat/completions'
max_tokens = 500

def analize_comment(comment_id):
    print(f"Analizing comment({comment_id})")
    comment = get_object_or_404(Comment, comment_id=comment_id)
    post = get_object_or_404(Post, post_id=comment.post.post_id)
    description = post.description
    text = comment.text
    prompt = f'Oceniaj bardzo surowo. Porownaj tresc komentarza do opisu, jak bardzo dobry jest ten komentarz ocen w skali 0.0 do 10.00. Zwroc json z polem rating float: 0.0 do 10.0. Gdzie 10.0 to bardzo dobry i wartosciowy komentarz, a 0 to bardzo niestotna informacja do opisu. Dlugosc komentarza tez jest istotna. Dane descirption:{description}, comment:{text}'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'gpt-3.5-turbo-1106',
        'messages': [{
            'role': 'system',
            'content': 'You are a helpful assistant that return only json as output.'
        }, {
            'role': 'user',
            'content': prompt
        }],
        'max_tokens': max_tokens,
    }

    response = requests.post(api_endpoint, headers=headers, json=data)

    if response.status_code == 200:
        response = response.json()['choices'][0]['message']['content']
        json_start = response.find('{')
        json_end = response.rfind('}')
        json_content = response[json_start:json_end+1]
        data = json.loads(json_content)
        rating = data["rating"]
        comment.rating = rating
        comment.save()
        print(f"Comment({comment.comment_id}) - Rating({rating})")
        return True
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None


def validate_comment_by_ai(comment_id):
    print(f"Validating comment({comment_id})")
    comment = get_object_or_404(Comment, comment_id=comment_id)
    prompt = f'Sprawdz czy komentarz jest wulgarny lub nieodpowiedni. Jako odpowiedz zwroc json z polem validate: bool. Gdy jest poprawny True, gdy jest wylgarny lub nieodpowiedni False. Komentarz: {comment.text}'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'gpt-3.5-turbo-1106',
        'messages': [{
            'role': 'system',
            'content': 'You are a helpful assistant that return only json as output.'
        }, {
            'role': 'user',
            'content': prompt
        }],
        'max_tokens': max_tokens,
    }

    response = requests.post(api_endpoint, headers=headers, json=data)
    print(response)
    if response.status_code == 200:
        response = response.json()['choices'][0]['message']['content']
        json_start = response.find('{')
        json_end = response.find('}')
        json_content = response[json_start:json_end+1]
        data = json.loads(json_content)
        validate = data["validate"]
        print(f"Comment({comment.comment_id}) - Validate({validate})")
        if not validate:
            comment.delete()
            print(f"Comment({comment.comment_id}) is deleted!")
        else:
            threading.Thread(target=analize_comment, args=(comment.comment_id,)).start()

        return True
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None