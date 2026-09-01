from django.urls import path
from . import views  


urlpatterns = [
    path('', views.product_list, name='product_list'),  # لیست محصولات
    path('<int:pk>/', views.product_detail, name='product_detail'),  # جزئیات محصول بر اساس ID
    path('<int:pk>/add_review/', views.add_review, name='add_review'),


]
