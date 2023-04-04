from rest_framework import serializers
from .models import Transaction


class Transact_Serial(serializers.ModelSerializer):
    send = serializers.ReadOnlyField(source="send.name.user.username")
    receive = serializers.ReadOnlyField(source="receive.name.user.username")
    date_added = serializers.DateTimeField(format="%b %d %y, %I:%M %p")

    class Meta:
        model = Transaction
        fields = [
            "amount",
            "send",
            "receive",
            "reason",
            "date_added",
        ]
