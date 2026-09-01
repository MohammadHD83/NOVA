from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone

from zarinpal import ZarinPal
from zarinpal_utils.Config import Config

from .models import Payment
from orders.models import Order

config = Config(
    sandbox=True,
    merchant_id=settings.ZARINPAL_MERCHANT_ID,
    access_token=settings.ZARINPAL_ACCESS_TOKEN
)


def start_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # اگر قبلا پرداخت شده
    if order.is_paid:
        return HttpResponse("این سفارش قبلا پرداخت شده است")

    amount = int(order.get_final_price())

    # اگر پرداخت قبلا ساخته شده باشد همان استفاده می‌شود
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            "user": request.user,
            "amount": amount,
            "description": f"Payment for Order #{order.id}"
        }
    )

    # اگر قبلا authority گرفته شده باشد دوباره درگاه نساز
    if payment.authority:
        zarinpal = ZarinPal(config)
        payment_url = zarinpal.payments.generate_payment_url(payment.authority)
        return redirect(payment_url)

    zarinpal = ZarinPal(config)

    response = zarinpal.payments.create({
        "amount": amount,
        "callback_url": request.build_absolute_uri("/payments/payment/verify/"),
        "description": payment.description,
    })

    if "data" in response and "authority" in response["data"]:
        authority = response["data"]["authority"]

        payment.authority = authority
        payment.save()

        payment_url = zarinpal.payments.generate_payment_url(authority)

        return redirect(payment_url)

    payment.status = "failed"
    payment.save()

    return HttpResponse("خطا در ایجاد پرداخت")


def verify_payment(request):
    authority = request.GET.get("Authority")
    status = request.GET.get("Status")

    payment = get_object_or_404(Payment, authority=authority)
    order = payment.order

    if status != "OK":
        payment.status = "failed"
        payment.save()
        return HttpResponse("پرداخت توسط کاربر لغو شد")

    zarinpal = ZarinPal(config)

    response = zarinpal.verifications.verify({
        "amount": payment.amount,
        "authority": authority,
    })

    if response["data"]["code"] == 100:

        payment.status = "success"
        payment.ref_id = response["data"]["ref_id"]
        payment.paid_at = timezone.now()
        payment.save()

        order.is_paid = True
        order.status = "paid"
        order.save()

        return HttpResponse(f"پرداخت موفق ✅ کد رهگیری: {payment.ref_id}")

    elif response["data"]["code"] == 101:
        return HttpResponse("این تراکنش قبلا تایید شده است")

    else:
        payment.status = "failed"
        payment.save()

        return HttpResponse("پرداخت ناموفق")
