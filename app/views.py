from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import os


client = OpenAI(api_key='=== YOUR OPENAPI KEY ===')
messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

def ask_openai(message):
    messages.append({'role': 'user', 'content': message})
    try:
        response = client.chat.completions.create(
            model="whisper-1",
            messages=messages
        )
        print(messages)
        print(response)
        answer = response.choices[0].message
        return answer
    except Exception as e:
        print(e)
        return 'Sorry, I am not able to answer your question at the moment. OpenAI limit reached.'

# Create your views here.
def chatbot_app(request):
    if request.method == 'POST':
        print(request)
        message = request.POST['message']
        response = ask_openai(message)
        return JsonResponse({'response': response})
    return render(request, 'chatbot-app.html')