from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib import messages
from bal.models import FiatWallet, CompayUser
from trans.models import Transaction
from rest_framework.authentication import TokenAuthentication
from pay.models import MultiPay
from rest_framework import status


# sending money to your frnd using username api
@api_view(["post"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def api_algo(request):
    logged = request.user
    com_user = CompayUser.objects.get(user=logged.id)
    sender = FiatWallet.objects.get(name=com_user)

    """to check current user account number"""
    mine_bal = int(sender.balance)

    # post request from frontend to grab details such as amount,reason and the username tag
    if request.method == "POST":
        try:
            amount = int(request.data.get("amount"))
            charges_all = (amount * 100) + 1000
            reason = request.data.get("reason")
            receive = str(request.data.get("tag"))

            try:
                v = User.objects.get(username=receive)
                try:
                    x = CompayUser.objects.get(user=v.id)
                    if (
                        (charges_all) > (mine_bal)
                        or charges_all == 1000
                        or com_user == x
                    ):
                        return Response(
                            {
                                "status": False,
                                "message": "insuffient funds, funds your account frnd or you can't send money to yourself",
                            },
                            status=status.HTTP_417_EXPECTATION_FAILED,
                        )

                    # where the transcation been processed and send
                    else:
                        receiver, created = FiatWallet.objects.get_or_create(name=x)
                        remit = int(receiver.balance) + (amount * 100)
                        receiver.balance = remit
                        receiver.save()
                        deduct = mine_bal - charges_all
                        sender.balance = deduct
                        sender.save()
                        info = Transaction.objects.create(
                            amount=amount, send=sender, receive=receiver, reason=reason
                        )
                    return Response(
                        {
                            "status": True,
                            "message": "transfer successful",
                            "data": request.data,
                        },
                        status=status.HTTP_202_ACCEPTED,
                    )
                except CompayUser.DoesNotExist:
                    return Response(
                        {"status": False, "message": "user have not created profile"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
            except User.DoesNotExist:
                return Response(
                    {"status": False, "message": "username does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except ValueError:
            return Response(
                {"status": False, "message": "the amount is not a number"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )


# this the MultiPayment function to send money to multiple people with one click
@api_view(["post"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def multipay_algo(request, access):
    logged = request.user
    current_form = MultiPay.objects.get(access_no=str(access))
    com_user = CompayUser.objects.get(user=logged.id)
    if current_form.user == com_user:
        sender = FiatWallet.objects.get(name=com_user)
        mine_bal = int(sender.balance)

        # this post request collect amount to be shared to among the user

        if request.method == "POST":
            try:
                amount = int(request.data.get("amount"))
                each_amount = (amount * 100) / int(current_form.pay_user.count())
                charges = int(current_form.pay_user.count()) * 1000
                charges_all = (amount * 100) + charges
                reason = current_form.title
                if (charges_all) > (mine_bal) or charges_all == 1000:
                    return Response(
                        {
                            "status": False,
                            "message": "insuffient funds, funds your account frnd",
                        },
                        status=status.HTTP_417_EXPECTATION_FAILED,
                    )
                else:
                    for user in current_form.pay_user.all():
                        receiver, created = FiatWallet.objects.get_or_create(name=user)
                        remit = int(receiver.balance) + int(each_amount)
                        receiver.balance = remit
                        receiver.save()
                        deduct = mine_bal - charges_all
                        sender.balance = deduct
                        sender.save()
                        info = Transaction.objects.create(
                            amount=each_amount,
                            send=sender,
                            receive=receiver,
                            reason=reason,
                        )
                return Response(
                    {
                        "status": True,
                        "message": "transfer successful",
                        "data": request.data,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            except ValueError:
                return Response(
                    {"status": False, "message": "the amount is not a number"},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
    else:
        return Response(
            {
                "status": False,
                "message": "error: not your form or account",
                "data": request.data,
            },
            status=status.HTTP_403_FORBIDDEN,
        )
