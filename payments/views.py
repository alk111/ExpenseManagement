from django.shortcuts import render
from django.conf import settings
# Create your views here.
import stripe
import razorpay
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt

stripe.api_key=settings.STRIPE_SECRET_KEY


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context 

def charge(request):
    if request.method == "POST":
        charge = stripe.Charge.create(
            amount=500,
            currency='inr',
            description='Payment Gateway',
            source=request.POST['stripeToken']
        )
        return render(request,'templates/payments/charge.html')

def index(request):
    
    return render(request, 'paypal.html')

def razor(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 50000

        client = razorpay.Client(
            auth=("rzp_test_m30XCwqkiKbdx6", "YWwKU2QRiqgeLIMcfuGNNhuX"))

        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
    return render(request, 'razor.html')

@csrf_exempt
def success(request):
    return render(request, "success.html")



