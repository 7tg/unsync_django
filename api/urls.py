from .views import ParseView
from django.urls import path

urlpatterns = [
    path('parse/', ParseView.as_view()),
]
