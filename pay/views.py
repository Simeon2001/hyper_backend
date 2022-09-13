from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from hook.payapi import charge, customer, total_transcation, nuban, transfer_cash, transfer_code
from django.contrib.auth.models import User
from .models import CustomerInfo
from bal.models import CompayUser, FiatWallet
from pay.models import PayLinks, MultiPay
from rest_framework.authentication import TokenAuthentication
from pay import hash
from rest_framework import status


# to generate link to deposit money in your HYPER account
@api_view(["post"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def generate(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    c_user = CompayUser.objects.get(user=user)
    if request.method == "POST":
        email = user.email
        partial_amount = int(request.data.get("amount"))
        amount = partial_amount * 100
        link = charge(email, amount)
        print(link)
        pay_ref = PayLinks.objects.create(
            user=c_user,
            reference=link["data"]["reference"],
            access_no=link["data"]["access_code"],
        )

        return Response(
            {"status": True, "message": link["data"]["authorization_url"]},
            status=status.HTTP_201_CREATED,
        )


# register your user as a paystack customer
# create customer
@api_view(["get"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_customer(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    c_user = CompayUser.objects.get(user=user)
    print(user.email)
    print(c_user)
    if request.method == "GET":
        email = user.email
        first_name = user.first_name
        last_name = user.last_name
        phone = "+2349036625937"
        link = customer(email, first_name, last_name, phone)
        print(link)
        print(email, first_name, last_name)
        c_id = link["data"]["customer_code"]
        info = CustomerInfo.objects.create(user=c_user, customer_no=c_id)
        info.save()

        return Response({"status": True}, status=status.HTTP_201_CREATED)


# to deposit m0oney by generating account number
@api_view(["get"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def generate_nuban(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    c_user = CompayUser.objects.get(user=user)
    customer_id = CustomerInfo.objects.get(user=c_user)
    if request.method == "GET":

        link = nuban(customer_id.customer_no)
        print(link)

        return Response(
            {
                "status": True,
            }
        )


# get all form info nd create a form for user to add there name
@api_view(["get", "post"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def multi_payinfo(request):
    current_user = request.user
    c_user = CompayUser.objects.get(user=current_user)
    if request.method == "GET":
        m_user = MultiPay.objects.filter(user=c_user)

        return Response(
            {
                "id": {i.id for i in m_user},
                "title": {i.title for i in m_user},
                "access_no": {i.access_no for i in m_user},
            },
            status=status.HTTP_200_OK,
        )
    if request.method == "POST":
        title = request.data.get("title")
        closing_no = request.data.get("closing_no")
        access_no = hash.hashes
        try:
            create_MultiPay = MultiPay.objects.create(
                user=c_user,
                title=title,
                closing_no=int(closing_no),
                access_no=access_no,
            )

            return Response(
                {
                    "status": True,
                    "title": title,
                    "closing_no": "after {0} username stored no username can be added".format(
                        closing_no
                    ),
                    "message": "successfully saved",
                },
                status=status.HTTP_201_CREATED,
            )
        except MultiPay.DoesNotExist:
            return Response(
                {"status": False, "message": "error"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# form to add your username
@api_view(["post"])
@permission_classes([AllowAny])
def multi_post(request, pk):
    if request.method == "POST":
        username = request.data.get("username")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"status": False, "message": "username does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            c_user = CompayUser.objects.get(user=user)
            add_user = MultiPay.objects.get(access_no=str(pk))
            if add_user.user != c_user:
                add_user.pay_user.add(c_user)
                add_user.save()
                return Response(
                    {"status": True, "message": "sucessfully save"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"status": False, "message": "you can't add your username"},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except CompayUser.DoesNotExist:
            return Response(
                {"status": False, "message": "username does not have profile"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# to withdraw money in your hyper wallet
@api_view(["get", "post"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def withdraw_funds(request):
    user = request.user
    user_info = CompayUser.objects.get(user=user)
    wallet = FiatWallet.objects.get(name=user_info)
    if request.method == "POST":
        amount = request.data.get("amount")
        real_amount = 100 * amount
        if real_amount > wallet.balance:
            return Response(
                {"status": False, "message": "insufficient funds"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            bank_code = "hello"
            code = transfer_code(user_info.account_name,user_info.account_number,bank_code)
            if code["status"]:
                ex_code = code["data"]["recipient_code"]
                cash_out = transfer_cash(ex_code,real_amount)
                msg = "{0} transferred to {1}, {2}".format(amount,user_info.account_name,user_info.account_number)
                return Response(
                    {"status": False, "message": msg},
                    status=status.HTTP_202_ACCEPTED,
                )
            return Response(
                {"status": False, "message": "invalid account details"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

