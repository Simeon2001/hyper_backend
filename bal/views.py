from django.shortcuts import render
from rest_framework import generics
from bal.serializers import CompaySerial, BtcSerializer, FiatSerializer
from bal.models import CompayUser, FiatWallet, UsdtWallet
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from trans.models import Transaction
from trans.serializers import Transact_Serial

# Create your views here.

# post request toadd user to compay user to collect more info
@api_view(["post"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def post_profilex(request):
    if request.method == "POST":
        user = request.user
        country = request.data.get("country")
        account_no = request.data.get("account_number")
        account_name = request.data.get("account_name")
        bank = request.data.get("bank_name")
        mobile_no = request.data.get("mobile_number")
        create, created = CompayUser.objects.get_or_create(user=user)
        create.country = country
        create.account_number = int(account_no)
        create.account_name = account_name
        create.bank_name = bank
        create.mobile_number = int(mobile_no)
        create.save()
        serializer_class = CompaySerial(create)
        return Response(serializer_class.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer_class.errors, status=status.HTTP_401_UNAUTHORIZED)


# profile
@api_view(["get"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def profile(request):
    logged = request.user
    user = CompayUser.objects.get(user=logged)
    serializer_class = CompaySerial(user)
    return Response(serializer_class.data)


# check your balance
@api_view(["get"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def checker(request):
    logged = request.user
    try:
        user = CompayUser.objects.get(user=logged)
        bal, created = FiatWallet.objects.get_or_create(name=user)
        balance = int(bal.balance) / int(100)
        return Response({"status": True, "balance": balance}, status=status.HTTP_200_OK)
    except CompayUser.DoesNotExist:
        return Response(
            {
                "status": False,
                "message": "Create your profile account",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


# crypto balance
@api_view(["get"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def crypto_balance(request):
    logged = request.user
    user = CompayUser.objects.get(user=logged)
    coin, created = UsdtWallet.objects.get_or_create(cname=user)
    serializer_class = BtcSerializer(coin)
    return Response(serializer_class.data)


# this function get transcation notification/user
@api_view(["get"])
@permission_classes([IsAuthenticated])
def notification(request):
    logged = request.user
    try:
        user = CompayUser.objects.get(user=logged)
        wallet = FiatWallet.objects.get(name=user)
        notify_user = Transaction.objects.extra(
            where=["send_id=%s OR receive_id=%s"], params=[wallet.id, wallet.id]
        ).order_by("-date_added")
        serializer_class = Transact_Serial(notify_user, many=True)
        return Response(serializer_class.data)
    except CompayUser.DoesNotExist:
        return Response(
            {
                "status": False,
                "message": "Create your profile account",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
