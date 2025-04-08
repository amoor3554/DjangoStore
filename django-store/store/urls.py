from django.urls import path
from. import views

urlpatterns = [
    path('', views.index, name='StoreHome'),
    path('product/<int:pid>/', views.product, name='StoreProduct'),
    path('category/<int:cid>/', views.category, name='StoreCategory'),
    path('category/', views.category, name='StoreCategory'),
    path('search/', views.search_product, name='SearchProduct'),
    path('cart/', views.cart, name='StoreCart'),
    path('cart/update/<int:pid>/', views.cart_update, name='StoreCartUpdate'),
    path('cart/remove/<int:pid>/', views.cart_remove, name='StoreCartRemove'),
]
