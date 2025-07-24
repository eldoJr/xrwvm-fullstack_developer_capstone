# Uncomment the required imports before adding the code

# from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
import requests
from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
@csrf_exempt
def logout_request(request):
    logout(request) # Terminate user session
    data = {"userName":""} # Return empty username
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    # Get user information from request
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    email = data.get('email', '')
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})
    
    # Create user
    user = User.objects.create_user(username=username, 
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
    
    # Login the user
    login(request, user)
    
    # Return username in response
    return JsonResponse({"userName": username, "status": "Registered and logged in"})


# Proxy views to forward requests to the database server
from .restapis import get_dealers, get_dealers_by_state, get_dealer_by_id, get_dealer_reviews as api_get_dealer_reviews

# Proxy view for fetchDealers
def get_dealerships(request):
    try:
        dealers = get_dealers()
        return JsonResponse(dealers, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Proxy view for fetchDealers/:state
def get_dealerships_by_state(request, state):
    try:
        dealers = get_dealers_by_state(state)
        return JsonResponse(dealers, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Proxy view for fetchDealer/:id
def get_dealer_details(request, dealer_id):
    try:
        dealer = get_dealer_by_id(dealer_id)
        return JsonResponse(dealer, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Proxy view for fetchReviews/dealer/:id
def get_dealer_reviews(request, dealer_id):
    try:
        reviews = api_get_dealer_reviews(dealer_id)
        return JsonResponse(reviews, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# Proxy view for insert_review
@csrf_exempt
def add_review(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = requests.post(
                f'{DATABASE_API_URL}/insert_review',
                json=data
            )
            return JsonResponse(response.json(), safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    
    # Check if the request is coming from a browser (admin interface)
    if request.headers.get('Accept', '').find('text/html') != -1:
        from django.shortcuts import render
        car_makes = CarMake.objects.all()
        context = {
            'car_makes': car_makes,
            'car_models': car_models,
            'cars_json': cars
        }
        return render(request, 'djangoapp/cars_list.html', context)
    else:
        # Return JSON for API calls
        return JsonResponse({"CarModels":cars})
