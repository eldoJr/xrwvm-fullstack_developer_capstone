# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        # If any error occurs
        print("Network exception occurred")

# def analyze_review_sentiments(text):
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        response = requests.get(request_url)
        return response.json()
    except:
        print("Network exception occurred")
        return {'sentiment': 'neutral'}

# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments

# def post_review(data_dict):
def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")

def get_dealers():
    """
    Get all dealers from the backend
    """
    endpoint = '/fetchDealers'
    dealers = get_request(endpoint)
    return dealers

def get_dealer_by_id(dealer_id):
    """
    Get dealer by id from the backend
    """
    endpoint = f'/fetchDealer/{dealer_id}'
    dealer = get_request(endpoint)
    return dealer

def get_dealers_by_state(state):
    """
    Get dealers by state from the backend
    """
    endpoint = f'/fetchDealers/{state}'
    dealers = get_request(endpoint)
    return dealers

def get_dealer_reviews(dealer_id):
    """
    Get reviews for a specific dealer from the backend
    """
    endpoint = f'/fetchReviews/dealer/{dealer_id}'
    reviews = get_request(endpoint)
    return reviews
