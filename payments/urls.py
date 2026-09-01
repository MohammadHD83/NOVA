from django.urls import path
from . import views

app_name = 'payments'

# urlpatterns = [
#     path('request/<int:order_id>/', views.payment_request, name='request'),
#     path('verify/', views.payment_verify, name='verify'),
# ]

urlpatterns = [
    path("payment/start/<int:order_id>/", views.start_payment, name="start_payment"),
    path("payment/verify/", views.verify_payment, name="verify_payment"),
]
