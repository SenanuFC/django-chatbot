from django.shortcuts import render
from django.http import JsonResponse
from openai import OpenAI
import os
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Chat
from django.utils import timezone


client = OpenAI(api_key='=== YOUR OPENAPI KEY ===')
messages = [{"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}]

def ask_openai(message):
    messages.append({'role': 'user', 'content': message})
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        answer = response.choices[0].message
        return answer
    except Exception as e:
        print(e)
        return 'Sorry, I am not able to answer your question at the moment. OpenAI limit reached.'

# Create your views here.
def chatbot_app(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        print(request)
        message = request.POST['message']
        response = ask_openai(message)
        # Save chat to database
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'response': response})
    return render(request, 'chatbot-app.html', {'chats': chats})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot-app')
        else:
            error_message = 'Invalid credentials'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def register(request): 
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot-app')
            except:
                error_message = 'Error creating user'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            print('Passwords do not match')
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')