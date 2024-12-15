from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
import json
from .forms import CustomUserCreationForm

@csrf_protect
def signup(request):
    """
    Handle user signup with CSRF protection.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON data from the request

            # Initialize the form with user data
            form = CustomUserCreationForm({
                'username': data.get('username'),
                'email': data.get('email'),
                'password1': data.get('password1'),
                'password2': data.get('password2'),
            })

            # Validate the form
            if form.is_valid():
                form.save()  # Save the new user to the database
                return JsonResponse({'message': 'Account created successfully!'}, status=201)
            else:
                # Return validation errors from the form
                return JsonResponse({'errors': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def csrf_token_view(request):
    """
    Provide CSRF token for frontend requests.
    """
    return JsonResponse({'csrfToken': get_token(request)})


