from django.urls import path
from. import views

urlpatterns = [
    path('', views.index, name='StoreHome'),
    path('product/<int:pid>', views.product, name='SroreProduct'),
    path('category/<int:cid>', views.category, name='StoreCategory'),
    path('category/', views.category, name='StoreCategory'),
    path('cart/', views.cart, name='StoreCart'),
    path('checkout/', views.check_out, name='StoreCheckout'),
    path('checkout/complete/', views.check_out_complete, name='StoreCheckoutComplete'),
]
