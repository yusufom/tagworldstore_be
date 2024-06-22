from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
# Create your views here.


import stripe

stripe.api_key = 'sk_test_51PToko2MhBsxnjfBB2l9FXzrFyJJKDRI4BtwE2MJwACUDysEHSInJ0F52vf5DHtOCVrtt84bwZz3BoJazeHiV4oS00VpJL9sch'



YOUR_DOMAIN = 'http://localhost:3000/checkout'


def create_checkout_session(request):
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1PTpUM2MhBsxnjfBQwbMJRgR',
                    'quantity': 1,
                },
                {
                    'price': 'price_1PTpUM2MhBsxnjfBQwbMJRgR',
                    'quantity': 3,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '?success=true',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
        
        print(checkout_session.url)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return redirect(checkout_session.url)