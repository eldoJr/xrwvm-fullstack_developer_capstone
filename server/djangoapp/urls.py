# Imports for URL configuration
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for registration
    path(route='register', view=views.registration, name='register'),
    
    # path for login
    path(route='login', view=views.login_user, name='login'),
    
    # path for logout
    path(route='logout', view=views.logout_request, name='logout'),

    # Proxy paths for database API
    path(route='fetchDealers', view=views.get_dealerships, name='get_dealerships'),
    path(route='fetchDealers/<str:state>', view=views.get_dealerships_by_state, name='get_dealerships_by_state'),
    path(route='fetchDealer/<str:dealer_id>', view=views.get_dealer_details, name='get_dealer_details'),
    path(route='fetchReviews/dealer/<str:dealer_id>', view=views.get_dealer_reviews, name='get_dealer_reviews'),
    path(route='insert_review', view=views.add_review, name='add_review'),
    path(route='get_cars', view=views.get_cars, name='getcars')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
