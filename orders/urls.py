from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('<int:order_id>/address/', views.add_order_address, name='add_address'),
    path('<int:order_id>/discount/', views.apply_discount, name='apply_discount'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
