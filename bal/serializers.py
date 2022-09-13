from rest_framework import serializers
from .models import CompayUser, FiatWallet, UsdtWallet


class BtcSerializer(serializers.HyperlinkedModelSerializer):
    # cname = CompaySerial()

    class Meta:
        model = UsdtWallet
        fields = ["balance"]


class FiatSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FiatWallet
        fields = ["balance",]


class CompaySerial(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    names = FiatSerializer(many=True)

    class Meta:
        model = CompayUser
        fields = [
            "user",
            "country",
            "currency",
            "account_number",
            "names",
        ]
