from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from bal.models import FiatWallet, CompayUser
from pay.models import PayLinks
import json

# webhook function
@csrf_exempt
@require_POST
def pay_hook(request):
    bod = request.body
    resp = json.loads(bod)
    event = resp["data"]["status"]
    if event == "success":
        amount = int((resp["data"]["amount"]))
        # fetch reference code to fund account
        ref = PayLinks.objects.get(reference=resp["data"]["reference"])
        gee, created = FiatWallet.objects.get_or_create(name=ref.user)
        bal = int(gee.balance) + amount
        ref.id_no = resp["data"]["id"]
        ref.success = True
        ref.save()
        gee.balance = bal
        gee.save()
    #    print(request.META)
    else:
        print(None)

    return HttpResponse(status=200)
