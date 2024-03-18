from . import views
from django.urls import path
from .views import UserWithProfileCreationView, CustomLoginView, ContactWizard, FORMS
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('register/', UserWithProfileCreationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('order/', ContactWizard.as_view(FORMS, initial_dict={"0": {"some": "data"}, "1": {"never": "mind"}})),
    path('payment/', views.pay, name='pay'),
    path('notify/', views.handle_post_request, name='handle_post'),
]