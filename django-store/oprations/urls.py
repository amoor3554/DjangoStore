from django.urls import path
from . import views
urlpatterns = [
    path('/order', views.make_order, name='CheckOutOrder'),
]
